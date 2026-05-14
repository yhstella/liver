#!/bin/bash
set -euo pipefail

# Only run setup inside Claude Code on the web.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Pillow is the only external Python dependency used by
# .tools/{augment_open_source_figures,collect_personal_web_figures,make_favicon,relabel_visual_keywords}.py
# The rest of .tools/*.py and .tools/build_guide.js only need stdlib.
pip install --quiet --disable-pip-version-check Pillow

# Activate the in-repo pre-commit hook so HTML edits auto-trigger
# rebuild_seo.py (sitemap, llms.txt, search-index, recent posts).
git config core.hooksPath .tools/hooks
