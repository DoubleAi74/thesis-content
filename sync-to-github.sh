#!/usr/bin/env bash
# Save, commit, and push this folder to GitHub.
set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository: $PWD" >&2
  exit 1
fi

branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$branch" == "HEAD" ]]; then
  echo "Detached HEAD; checkout a branch before pushing." >&2
  exit 1
fi

git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
else
  stamp="$(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "Auto-sync ${stamp}"
fi

git push -u origin "$branch"
echo "Done: $PWD -> origin/${branch}"
