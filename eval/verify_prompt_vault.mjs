#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(name);
  if (i < 0 || i + 1 >= args.length) throw new Error(`Missing ${name}`);
  return args[i + 1];
};
const vaultFile = path.resolve(getArg('--vault'));
const outputDir = path.resolve(getArg('--output-dir'));
fs.mkdirSync(outputDir, { recursive: true });
const vault = JSON.parse(fs.readFileSync(vaultFile, 'utf8'));
const expectedTitles = vault.prompts.map((p) => p.title);
const profileDir = path.join(outputDir, 'isolated-browser-profile');

const report = {
  schema_version: '0.2',
  target: 'https://appliedaihub.org/tools/prompt-vault/',
  isolated_profile: true,
  vault_file: path.basename(vaultFile),
  vault_title_expected: vault.vaultTitle,
  prompt_titles_expected: expectedTitles,
  imported: false,
  verified: false,
  page_url: null,
  navigation_warning: null,
  visible_buttons: [],
  visible_links: [],
  indexeddb: [],
  error: null,
};

let context;
try {
  context = await chromium.launchPersistentContext(profileDir, {
    headless: true,
    viewport: { width: 1440, height: 1000 },
    acceptDownloads: true,
  });
  let page = context.pages()[0] || await context.newPage();
  page.on('dialog', async (dialog) => {
    try { await dialog.accept(); } catch {}
  });

  try {
    await page.goto(report.target, { waitUntil: 'domcontentloaded', timeout: 120000 });
  } catch (error) {
    report.navigation_warning = error instanceof Error ? error.message : String(error);
    if (!(await page.locator('body').count())) throw error;
  }
  await page.waitForTimeout(5000);
  report.page_url = page.url();
  await page.screenshot({ path: path.join(outputDir, '01-before-import.png'), fullPage: true });

  const collectUi = async (activePage) => {
    report.visible_buttons = await activePage.locator('button, [role="button"]').evaluateAll((els) => els.map((e) => ({
      text: (e.innerText || '').trim(),
      title: e.getAttribute('title'),
      aria: e.getAttribute('aria-label'),
    })).slice(0, 150));
    report.visible_links = await activePage.locator('a').evaluateAll((els) => els.map((e) => ({
      text: (e.innerText || '').trim(),
      href: e.href,
      title: e.getAttribute('title'),
      aria: e.getAttribute('aria-label'),
    })).slice(0, 150));
  };
  await collectUi(page);

  const initialPageCount = context.pages().length;
  const launchCandidate = page.getByText(/start organizing now|open prompt vault|launch prompt vault|open vault/i).first();
  if (await launchCandidate.count()) {
    try {
      await launchCandidate.click({ timeout: 15000 });
      await page.waitForTimeout(5000);
      if (context.pages().length > initialPageCount) {
        page = context.pages().at(-1);
        await page.waitForLoadState('domcontentloaded', { timeout: 60000 }).catch(() => {});
        await page.waitForTimeout(3000);
      }
    } catch (error) {
      report.launch_warning = error instanceof Error ? error.message : String(error);
    }
  }

  async function tryFrame(activePage, frame) {
    const inputs = frame.locator('input[type="file"]');
    if (await inputs.count()) {
      await inputs.first().setInputFiles(vaultFile);
      return true;
    }
    const candidates = frame.locator('button, [role="button"], a').filter({ hasText: /import|restore|upload|backup/i });
    const n = await candidates.count();
    for (let i = 0; i < n; i++) {
      const candidate = candidates.nth(i);
      try {
        const chooserPromise = activePage.waitForEvent('filechooser', { timeout: 8000 }).catch(() => null);
        await candidate.click({ timeout: 8000 });
        const chooser = await chooserPromise;
        if (chooser) {
          await chooser.setFiles(vaultFile);
          return true;
        }
        const postInputs = frame.locator('input[type="file"]');
        if (await postInputs.count()) {
          await postInputs.first().setInputFiles(vaultFile);
          return true;
        }
      } catch {}
    }
    return false;
  }

  let imported = false;
  for (const activePage of context.pages()) {
    for (const frame of activePage.frames()) {
      if (await tryFrame(activePage, frame)) {
        imported = true;
        page = activePage;
        break;
      }
    }
    if (imported) break;
  }
  report.imported = imported;
  if (!imported) throw new Error('No Prompt Vault import control or file input was found');

  await page.waitForTimeout(6000);
  await page.screenshot({ path: path.join(outputDir, '02-after-import.png'), fullPage: true });
  report.page_url = page.url();
  await collectUi(page);

  const bodyText = await page.locator('body').innerText();
  const missingTitles = expectedTitles.filter((title) => !bodyText.includes(title));
  const vaultTitleVisible = !vault.vaultTitle || bodyText.includes(vault.vaultTitle);

  report.indexeddb = await page.evaluate(async () => {
    if (!indexedDB.databases) return [{ note: 'indexedDB.databases() unsupported' }];
    const dbs = await indexedDB.databases();
    const result = [];
    for (const info of dbs) {
      const name = info.name;
      if (!name) continue;
      const detail = await new Promise((resolve) => {
        const req = indexedDB.open(name);
        req.onerror = () => resolve({ name, error: String(req.error) });
        req.onsuccess = () => {
          const db = req.result;
          resolve({ name, version: db.version, stores: Array.from(db.objectStoreNames) });
          db.close();
        };
      });
      result.push(detail);
    }
    return result;
  });

  report.prompt_titles_missing = missingTitles;
  report.vault_title_visible = vaultTitleVisible;
  report.verified = imported && missingTitles.length === 0;
  if (!report.verified) throw new Error(`Import completed but UI verification failed; missing titles: ${missingTitles.join(', ')}`);
} catch (error) {
  report.error = error instanceof Error ? error.stack || error.message : String(error);
} finally {
  fs.writeFileSync(path.join(outputDir, 'prompt-vault-import-report.json'), JSON.stringify(report, null, 2));
  if (context) await context.close();
}

if (!report.verified) process.exit(2);
