# ChatGPT App Submission Checklist

## App metadata

- [ ] App name is clear
- [ ] Subtitle is specific
- [ ] Description matches real behaviour
- [ ] Category is appropriate

## Tool review

- [ ] Every exposed tool is listed
- [ ] Tool names match behaviour
- [ ] Tool descriptions are accurate
- [ ] Input schemas are defined
- [ ] Output schemas are present or warnings are recorded
- [ ] `readOnlyHint` is checked
- [ ] `openWorldHint` is checked
- [ ] `destructiveHint` is checked

## Test cases

- [ ] At least five positive test cases
- [ ] At least three negative test cases
- [ ] Negative tests include nearby out-of-scope requests
- [ ] Sensitive-data and permission edge cases are covered

## Final question

Would a reviewer see the same behaviour in the code that the submission claims in the form?
