"""Strip ' — subtitle' suffix from titles across all pages.

Targets:
  - <h1>X — subtitle</h1>  → <h1>X</h1>
  - <title>X — subtitle — Hepatology Note</title> → <title>X — Hepatology Note</title>
    (preserves the trailing site-name segment)
  - <meta property="og:title" content="X — subtitle"> → <meta ... content="X">
    (also handle " — Hepatology Note" suffix)
  - JSON-LD "name":"X — subtitle" → "name":"X"
  - Topic-list <h3>X — subtitle</h3> inside <ul class="topic-list"> → <h3>X</h3>
  - Breadcrumb final <span>X — subtitle</span> → <span>X</span>

Strategy: split on " — " and take FIRST segment for the visible title;
for <title> tag preserve trailing " — Hepatology Note" segment.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_SUFFIX = " — Hepatology Note"


def strip_first(s: str) -> str:
    """Strip everything after first ' — ', return first segment."""
    return s.split(" — ")[0].strip()


def fix_title_tag(text: str) -> str:
    """<title>X — sub — Hepatology Note</title> → <title>X — Hepatology Note</title>"""
    def repl(m):
        full = m.group(1)
        if SITE_SUFFIX in full:
            head = full[:full.rfind(SITE_SUFFIX)]
            head_clean = strip_first(head)
            return f"<title>{head_clean}{SITE_SUFFIX}</title>"
        else:
            return f"<title>{strip_first(full)}</title>"
    return re.sub(r"<title>([^<]+)</title>", repl, text)


def fix_h1(text: str) -> str:
    def repl(m):
        attrs = m.group(1)
        body = m.group(2)
        # Body may contain inline tags — but for our pages it's plain text or with <em>
        # If it's plain text with em-dash, strip after first " — "
        if " — " in body:
            new_body = strip_first(body)
            return f"<h1{attrs}>{new_body}</h1>"
        return m.group(0)
    return re.sub(r"<h1([^>]*)>(.*?)</h1>", repl, text, flags=re.DOTALL)


def fix_og_title(text: str) -> str:
    def repl(m):
        prefix = m.group(1)
        content = m.group(2)
        suffix = m.group(3)
        # If content ends with site suffix, preserve it
        if SITE_SUFFIX in content:
            head = content[:content.rfind(SITE_SUFFIX)]
            return prefix + strip_first(head) + SITE_SUFFIX + suffix
        return prefix + strip_first(content) + suffix
    return re.sub(
        r'(<meta\s+property="og:title"\s+content=")([^"]+)(")',
        repl, text,
    )


def fix_jsonld_name(text: str) -> str:
    def repl(m):
        name = m.group(1)
        return '"name":"' + strip_first(name) + '"'
    return re.sub(r'"name":"([^"]+)"', repl, text)


def fix_topic_list_h3(text: str) -> str:
    """Inside <ul class='topic-list'>...<h3>X — sub</h3>...</ul>"""
    def repl_block(m):
        block = m.group(0)
        def repl_h3(mm):
            body = mm.group(1)
            if " — " in body:
                return f"<h3>{strip_first(body)}</h3>"
            return mm.group(0)
        return re.sub(r"<h3>([^<]+)</h3>", repl_h3, block)
    return re.sub(r'<ul class="topic-list">.*?</ul>', repl_block, text, flags=re.DOTALL)


def fix_breadcrumb(text: str) -> str:
    """Final <span>X — sub</span> in <nav class='crumb'>"""
    def repl_crumb(m):
        cr = m.group(1)
        # Find spans without class attribute — those are page-title spans
        spans = list(re.finditer(r"<span(?![^>]*class)([^>]*)>([^<]+)</span>", cr))
        if not spans:
            return cr
        last = spans[-1]
        body = last.group(2)
        if " — " in body:
            new_body = strip_first(body)
            new_span = f"<span{last.group(1)}>{new_body}</span>"
            return cr[:last.start()] + new_span + cr[last.end():]
        return cr
    return re.sub(r'(<nav class="crumb">.*?</nav>)', repl_crumb, text, flags=re.DOTALL)


def fix_page(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    new = text
    new = fix_title_tag(new)
    new = fix_h1(new)
    new = fix_og_title(new)
    new = fix_jsonld_name(new)
    new = fix_topic_list_h3(new)
    new = fix_breadcrumb(new)
    if new != text:
        p.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for p in ROOT.rglob("index.html"):
        if any(x in p.parts for x in ("private-figures", "assets", ".tools", "node_modules")):
            continue
        if fix_page(p):
            n += 1
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            print(f"  fixed: {rel}")
    print(f"Done. {n} pages fixed.")


if __name__ == "__main__":
    main()
