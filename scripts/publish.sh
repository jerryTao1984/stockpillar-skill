#!/usr/bin/env bash
#
# Sync this skill from the StockPillar monorepo to the standalone public repo
# at ~/stockpillar-skill-pub, then commit and push.
#
# Usage:
#   ./publish.sh "Release notes for this sync"          # publish
#   ./publish.sh --dry-run "Release notes for this sync"  # preview only, no rsync, no commit
#
# Prerequisites:
#   - ~/stockpillar-skill-pub already cloned from the public repo
#   - git remote `origin` already pointing at jerryTao1984/stockpillar-skill

set -euo pipefail

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  shift
fi

MSG="${1:-Sync from monorepo}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST="${HOME}/stockpillar-skill-pub"

if [[ ! -d "${DST}/.git" ]]; then
  echo "Error: ${DST} is not a git repo. Clone it first:"
  echo "  git clone https://github.com/jerryTao1984/stockpillar-skill ${DST}"
  exit 1
fi

echo "Source:      ${SRC}"
echo "Destination: ${DST}"
echo "Message:     ${MSG}"
[[ ${DRY_RUN} -eq 1 ]] && echo "Mode:        DRY-RUN (no changes will be made)"

RSYNC_FLAGS=(-av --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='.DS_Store')
[[ ${DRY_RUN} -eq 1 ]] && RSYNC_FLAGS+=(--dry-run)

rsync "${RSYNC_FLAGS[@]}" "${SRC}/" "${DST}/"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo
  echo "Dry-run complete. Re-run without --dry-run to apply."
  exit 0
fi

cd "${DST}"
if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

git add .
git status --short
read -r -p "Commit and push? [y/N] " ans
if [[ "${ans}" != "y" && "${ans}" != "Y" ]]; then
  echo "Aborted; staged changes left in ${DST}."
  exit 0
fi

git commit -m "${MSG}"
git push origin main
echo "Published."
