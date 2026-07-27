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
  schema_version: '0.1',
  target: 'https://appliedaihub.org/tools/prompt-vault/',
  isolated_profile: true,
  vault_file: path.basename(vaultFile),
  vault_title_expected: vault.vaultTitle,
  prompt_titles_expected: expectedTitles,
  imported: false,
  verified: false,
  page_url: null,
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
  const pages = context.pages();
  const page = pages[0] || await context.newPage();
  page.on('dialog', async (dialog) => {
    try { await dialog.accept(); } catch {}
  });
  await page.goto(report.target, { waitUntil: 'networkidle', timeout: 120000 });
  await page.screenshot({ path: path.join(outputDir, '01-before-import.png'), fullPage: true });

  const collectUi = async () => {
    report.visible_buttons = await page.locator('button').evaluateAll((els) => els.map((e) => ({
      text: (e.innerText || '').trim(),
      title: e.getAttribute('title'),
      aria: e.getAttribute('aria-label'),
    })).slice(0, 100));
    report.visible_links = await page.locator('a').evaluateAll((els) => els.map((e) => ({
      text: (e.innerText || '').trim(),
      href: e.href,
      title: e.getAttribute('title'),
      aria: e.getAttribute('aria-label'),
    })).slice(0, 100));
  };
  await collectUi();

  // Marketing-page handoff, when present.
  const launchCandidate = page.getByText(/start organizing now|open prompt vault|launch prompt vault|open vault/i).first();
  if (await launchCandidate.count()) {
    try {
      await launchCandidate.click({ timeout: 10000 });
      await page.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});
    } catch {}
  }

  async function tryFrame(frame) {
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
        const chooserPromise = page.waitForEvent('filechooser', { timeout: 5000 }).catch(() => null);
        await candidate.click({ timeout: 5000 });
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
  for (const frame of page.frames()) {
    if (await tryFrame(frame)) {
      imported = true;
      break;
    }
  }
  report.imported = imported;
  if (!imported) throw new Error('No Prompt Vault import control or file input was found');

  await page.waitForTimeout(5000);
  await page.screenshot({ path: path.join(outputDir, '02-after-import.png'), fullPage: true });
  report.page_url = page.url();
  await collectUi();

  // Import may succeed inside a child frame; collect visible text from every frame.
  const frameTexts = [];
  for (const frame of page.frames()) {
    try {
      frameTexts.push(await frame.locator('body').innerText({ timeout: 5000 }));
    } catch {}
  }
  const bodyText = frameTexts.join('\n');
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
  report.verified = imported && missingTitles.length === 0 && vaultTitleVisible;
  if (!report.verified) {
    throw new Error(
      `Import completed but UI verification failed; missing titles: ${missingTitles.join(', ') || '(none)'}; vault_title_visible: ${vaultTitleVisible}`,
    );
  }
} catch (error) {
  report.error = error instanceof Error ? error.stack || error.message : String(error);
} finally {
  fs.writeFileSync(path.join(outputDir, 'prompt-vault-import-report.json'), JSON.stringify(report, null, 2));
  if (context) await context.close();
}

if (!report.verified) process.exit(2);
