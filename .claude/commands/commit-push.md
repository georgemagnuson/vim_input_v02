---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git status:*)
argument-hint: [commit message]
description: Add, commit with Claude Code signature, and push changes to remote
model: claude-sonnet-4-20250514
---

I'll stage all changes, commit with your message and Claude Code signature, then push to remote.

First, let me stage all changes:
```bash
git add -A
```

Now I'll commit with your message and the Claude Code signature:
```bash
git commit -m "$ARGUMENTS

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Finally, I'll push to the remote repository:
```bash
git push
```