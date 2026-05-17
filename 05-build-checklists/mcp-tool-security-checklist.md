# MCP Tool Security Checklist

## Tool inventory

- [ ] Every tool is listed
- [ ] Every tool has a clear purpose
- [ ] Every tool has defined input and output schemas
- [ ] Every tool has side effects classified

## Side-effect review

- [ ] Read-only behaviour is actually read-only
- [ ] Write actions are explicit
- [ ] Destructive actions are labelled
- [ ] External-world actions require clear user intent
- [ ] Public or third-party changes are not hidden behind vague tool names

## Sensitive data review

- [ ] Tool does not expose secrets
- [ ] Tool does not log raw sensitive content unnecessarily
- [ ] Tool does not send unapproved content to models or third parties
- [ ] Tool respects approval gates

## Final question

Could this tool surprise a user by doing more than its name or description suggests?
