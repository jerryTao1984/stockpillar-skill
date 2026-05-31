#!/usr/bin/env bash
#
# Sync this skill from the StockPillar monorepo to the standalone public repo
# at ~/stockpillar-skill-pub, then commit and push.
#
# Usage:
#   ./publish.sh "Release notes for this sync"
#   ./publish.sh -y "Release notes"        # skip the confirm prompt (non-interactive)
#   PUBLISH_ASSUME_YES=1 ./publish.sh "..."  # same, via env
#
# Prerequisites:
#   - ~/stockpillar-skill-pub already cloned from the public repo
#   - git remote `origin` already pointing at jerryTao1984/stockpillar-skill

set -euo pipefail

# Parse args: an optional -y/--yes flag (anywhere) skips the interactive confirm;
# the first non-flag arg is the commit message. PUBLISH_ASSUME_YES=1 also skips it.
ASSUME_YES="${PUBLISH_ASSUME_YES:-0}"
MSG=""
for arg in "$@"; do
  case "${arg}" in
    -y|--yes) ASSUME_YES=1 ;;
    *) [[ -z "${MSG}" ]] && MSG="${arg}" ;;
  esac
done
MSG="${MSG:-Sync from monorepo}"

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST="${HOME}/stockpillar-skill-pub"

if [[ ! -d "${DST}/.git" ]]; then
  echo "Error: ${DST} is not a git repo. Clone it first:"
  echo "  git clone https://github.com/jerryTao1984/stockpillar-skill ${DST}"
  exit 1
fi

echo "Source:      ${SRC}"
echo "Destination: ${DST}"

rsync -av --delete \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='__pycache__' \
  --exclude='.DS_Store' \
  --exclude='scripts/publish.sh' \
  "${SRC}/" "${DST}/"

cp "${SRC}/scripts/publish.sh" "${DST}/scripts/publish.sh" 2>/dev/null || true

cd "${DST}"
if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

git add .
git status --short
if [[ "${ASSUME_YES}" == "1" ]]; then
  echo "Auto-confirm enabled (-y / PUBLISH_ASSUME_YES); committing and pushing."
else
  read -r -p "Commit and push? [y/N] " ans
  if [[ "${ans}" != "y" && "${ans}" != "Y" ]]; then
    echo "Aborted; staged changes left in ${DST}."
    exit 0
  fi
fi

git commit -m "${MSG}"
git push origin main
echo "Published."
