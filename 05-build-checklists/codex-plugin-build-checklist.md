# Codex Plugin Build Checklist

## Required structure

- [ ] Plugin folder has a clear name
- [ ] `.codex-plugin/plugin.json` exists
- [ ] Skills are placed under `skills/<skill-name>/SKILL.md`
- [ ] Each skill has a purpose, trigger, workflow, and output contract
- [ ] Any MCP/app integration is documented separately

## Review checks

- [ ] No secrets are committed
- [ ] Skill behaviour is specific enough to test
- [ ] Tool side effects are labelled
- [ ] Review gates are explicit
- [ ] Outputs are reusable outside the original chat

## Final question

Can another builder use this plugin without needing the original conversation context?
