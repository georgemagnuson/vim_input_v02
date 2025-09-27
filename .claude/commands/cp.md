---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git status:*), Bash(git diff:*)
description: Smart commit and push - analyzes changes and creates commit message
model: claude-sonnet-4-20250514
---

I'll analyze your changes, create an appropriate commit message, and push to remote.

First, let me check what's changed:

```bash
git status
```

```bash
git diff --name-only
```

Now I'll analyze the changes and create a meaningful commit message, then stage, commit, and push all changes.