# Agent instructions

## Where repositories live (owner decision 2026-11-02)

- New repositories are created on **GitLab only**, in the group `translife-group` on gitlab.com
  (`glab repo create translife-group/<name> --private --defaultBranch main`). Never create a new
  repository on GitHub, from any tool or platform (Claude Code, Codex, Cursor, Kilo Code,
  Antigravity, Windsurf, Devin, ChatGPT or any other).
- Every new GitLab project: protected `main` (merge requests only, no direct or force push), squash
  merges, "Pipelines must succeed", auto-merge, GitLab-hosted shared runners off. CI and tests run
  only on our self-hosted runners, which start when jobs wait and stop when idle. Every deploy job
  sits in a `resource_group` so two deploys never overlap.
- This repository itself stays at `github.com/translife-ai/obsidian-auto-linker` until the owner moves it.
