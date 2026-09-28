#!/usr/bin/env python3
"""
publish_update_scheduled.py — 발행 큐에서 저자가 승인한 초안 하나를 공개하고 push까지 한다.

큐 파일: .tools/publish_queue.txt (UTF-8, 한 줄에 하나, # 은 주석)
  간암-B형간염-약 | 간암          ← 세부 글: 슬러그 | 허브(목록에 추가할 허브, 없으면 생략)
  updates/Lean-MASLD-review-2026   ← 최신 지견 글

승인 규칙
  - 초안의 DRAFT 주석이 <!-- DRAFT: 발행 승인 ... --> 인 글만 발행한다.
  - 큐 순서대로 보되, 승인된 것 중 가장 앞의 한 편만 올린다. 승인된 글이 없으면 아무것도 하지 않는다.

  python .tools/publish_update_scheduled.py
  python .tools/publish_update_scheduled.py --dry-run

안전장치 (2026-08-19 교착, 9/1 cp949, 9/4~13 dirty-check 교착 이후)
  - 작업 트리에 큐·우선순위 파일 밖의 수정사항이 있으면 커밋하지 않고 멈춘다
  - 모든 외부 명령에 타임아웃, 비대화형 git, 자식 python UTF-8
  - rebuild_seo 를 직접 돌리므로 pre-commit 훅은 건너뛴다
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
LOG = TOOLS / "updates_publish.log"
QUEUE = TOOLS / "publish_queue.txt"
PRIORITY = TOOLS / "publish_priority.txt"
KST = timezone(timedelta(hours=9))

APPROVED_RE = re.compile(r"<!--\s*DRAFT:\s*발행 승인[^>]*-->")
DRAFT_COMMENT_RE = re.compile(r"<!--\s*DRAFT[^>]*-->\s*\n?")
ROBOTS_NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="noindex,nofollow">')
ROBOTS_INDEX = '<meta name="robots" content="index,follow,max-image-preview:large">'
PUBLISH_DATE_RE = re.compile(r'<p class="publish-date">.*?</p>', re.S)

# 발행되면 홈의 질문 카드가 이 글을 가리키게 바꾼다: 슬러그 → (지금 href, 새 설명)
HOME_CARD = {
    "간이-나빠지지-않게": ("#topics", "원인별로 먼저 할 일과 매일 지킬 것"),
    "간-외래-검사": ("/간수치/", "피검사부터 초음파, 파이브로스캔까지"),
}

try:  # 콘솔이 cp949여도 한글 로그가 깨지지 않게
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GIT_ENV = {
    **os.environ,
    "GIT_TERMINAL_PROMPT": "0",
    "GCM_INTERACTIVE": "never",
    "GIT_ASKPASS": "",
    "SSH_ASKPASS": "",
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8",
}
GIT = ["git", "-c", "core.fsmonitor=false", "-c", "core.quotepath=false"]


def log(msg: str) -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args, check=True, timeout=600, label=None):
    name = label or " ".join(str(a) for a in args[:3])
    try:
        r = subprocess.run(
            args, cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=GIT_ENV, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT {name} :: {timeout}s 안에 끝나지 않아 중단했습니다")
        raise SystemExit(1)
    if check and r.returncode != 0:
        log(f"FAIL {name} :: {(r.stderr or r.stdout or '').strip()[:400]}")
        raise SystemExit(1)
    return r


def read_queue():
    if not QUEUE.exists():
        return []
    out = []
    for ln in QUEUE.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        slug, _, hub = (x.strip() for x in s.partition("|"))
        out.append((s, slug, hub or None))
    return out


def drop_from_queue(raw_line: str) -> None:
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    kept, dropped = [], False
    for ln in lines:
        if not dropped and ln.strip() == raw_line:
            dropped = True
            continue
        kept.append(ln)
    QUEUE.write_text("\n".join(kept) + "\n", encoding="utf-8")


def page_of(slug: str) -> Path:
    return ROOT / slug / "index.html"


def add_to_hub(hub: str, slug: str, text: str) -> bool:
    hub_page = ROOT / hub / "index.html"
    if not hub_page.exists():
        log(f"WARN 허브 없음: {hub}")
        return False
    h = hub_page.read_text(encoding="utf-8")
    if f'href="/{slug}/"' in h:
        return False
    items = list(re.finditer(r'<li class="published">.*?</li>', h, re.S))
    if not items:
        log(f"WARN 허브 목록 형식을 찾지 못함: {hub}")
        return False
    title = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1)).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)"', text).group(1)
    desc = desc.split(". ")[0].rstrip(".")
    num = f"{len(items) + 1:02d}"
    li = (f'\n  <li class="published">\n    <a href="/{slug}/">\n      <span class="num">{num}</span>\n'
          f'      <div class="body">\n        <h3>{title}</h3>\n        <p>{desc}</p>\n      </div>\n'
          f'      <span class="status published">읽기 →</span>\n    </a>\n  </li>')
    end = items[-1].end()
    hub_page.write_text(h[:end] + li + h[end:], encoding="utf-8", newline="")
    return True


def update_home_card(slug: str) -> bool:
    if slug not in HOME_CARD:
        return False
    old_href, new_desc = HOME_CARD[slug]
    home = ROOT / "index.html"
    h = home.read_text(encoding="utf-8")
    m = re.search(rf'<a href="{re.escape(old_href)}" class="start-card">(.*?)</a>', h, re.S)
    if not m:
        return False
    inner = re.sub(r"(<span>)(?!<)[^<]*(</span>)", rf"\g<1>{new_desc}\g<2>", m.group(1), count=1)
    new = f'<a href="/{slug}/" class="start-card">{inner}</a>'
    home.write_text(h[:m.start()] + new + h[m.end():], encoding="utf-8", newline="")
    return True


def publish_detail(slug: str, hub, now: datetime) -> None:
    p = page_of(slug)
    text = p.read_text(encoding="utf-8")
    text = ROBOTS_NOINDEX_RE.sub(ROBOTS_INDEX, text, count=1)
    text = DRAFT_COMMENT_RE.sub("", text, count=1)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    date_iso = now.strftime("%Y-%m-%d")
    kor = f'<span class="y">{now.year}년 </span>{now.month}월 {now.day}일'
    text = PUBLISH_DATE_RE.sub(f'<p class="publish-date">작성일 <time datetime="{date_iso}">{kor}</time></p>', text, count=1)
    text = re.sub(r'<meta property="article:published_time" content="[^"]*">',
                  f'<meta property="article:published_time" content="{iso}">', text, count=1)
    for key in ("datePublished", "dateModified"):
        text = re.sub(rf'"{key}":"[^"]*"', f'"{key}":"{iso}"', text)
    text = re.sub(r'"lastReviewed":"[^"]*"', f'"lastReviewed":"{date_iso}"', text)
    p.write_text(text, encoding="utf-8", newline="")
    if hub and add_to_hub(hub, slug, text):
        log(f"  허브 목록에 추가: /{hub}/")
    if update_home_card(slug):
        log("  홈 질문 카드 링크 교체")


def publish_update(slug: str) -> None:
    short = slug.split("/", 1)[1]
    cur = PRIORITY.read_text(encoding="utf-8").splitlines() if PRIORITY.exists() else []
    rest = [ln for ln in cur if ln.strip() != short]
    head = [ln for ln in rest if ln.startswith("#")]
    body = [ln for ln in rest if not ln.startswith("#")]
    PRIORITY.write_text("\n".join(head + [short] + body) + "\n", encoding="utf-8")
    run([sys.executable, str(TOOLS / "publish_next_draft.py")], timeout=180, label="publish_next_draft")


def main() -> int:
    dry = "--dry-run" in sys.argv
    queue = read_queue()
    if not queue:
        log("발행 큐가 비어 있습니다")
        return 0

    target = None
    for raw, slug, hub in queue:
        p = page_of(slug)
        if not p.exists():
            log(f"SKIP {slug}: 페이지 없음")
            continue
        text = p.read_text(encoding="utf-8")
        if not ROBOTS_NOINDEX_RE.search(text):
            log(f"SKIP {slug}: 이미 공개됨 — 큐에서 뺍니다")
            if not dry:
                drop_from_queue(raw)
            continue
        if APPROVED_RE.search(text):
            target = (raw, slug, hub)
            break
    if not target:
        log(f"HOLD: 승인된 초안 없음 (큐 {len(queue)}편, 저자 검수 대기)")
        return 0
    raw, slug, hub = target

    st = run(GIT + ["status", "--porcelain"], check=False, timeout=120, label="git status")
    dirty = [ln[3:] for ln in st.stdout.splitlines() if ln.strip()]
    allowed = {".tools/publish_queue.txt", ".tools/publish_priority.txt"}
    outside = [f for f in dirty if f not in allowed]
    if outside:
        log(f"ABORT: 커밋 안 된 변경 {len(outside)}건 — {outside[:3]}")
        return 1

    if dry:
        log(f"DRY-RUN would publish {slug}" + (f" (허브 {hub})" if hub else ""))
        return 0

    log(f"publishing {slug}")
    if slug.startswith("updates/"):
        publish_update(slug)
    else:
        publish_detail(slug, hub, datetime.now(KST))
    if ROBOTS_NOINDEX_RE.search(page_of(slug).read_text(encoding="utf-8")):
        log(f"ABORT {slug}: robots meta not flipped")
        return 1
    drop_from_queue(raw)

    run([sys.executable, str(TOOLS / "rebuild_seo.py")], timeout=900, label="rebuild_seo")
    run(GIT + ["add", "-A"], timeout=180, label="git add")
    c = run(GIT + ["commit", "--no-verify", "-m", f"자동 발행: {slug}"],
            check=False, timeout=300, label="git commit")
    if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
        log(f"FAIL commit :: {(c.stderr or c.stdout).strip()[:300]}")
        return 1
    p = run(GIT + ["push", "origin", "main"], check=False, timeout=300, label="git push")
    if p.returncode != 0:
        log(f"FAIL push :: {(p.stderr or p.stdout).strip()[:300]}")
        return 1
    left = len(read_queue())
    log(f"published /{slug}/ — pushed. 큐에 남은 글: {left}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
