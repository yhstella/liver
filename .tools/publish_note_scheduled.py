#!/usr/bin/env python3
"""
publish_note_scheduled.py — 예약 발행. 큐에서 단상 글 하나를 꺼내 공개하고 push까지 한다.

큐 파일: .tools/notes_publish_queue.txt (UTF-8, 슬러그 한 줄에 하나, # 은 주석)
맨 위 줄부터 하나 꺼내 공개하고, 그 줄을 큐에서 지운다.

인자 없이 실행한다 (Windows 작업 스케줄러에서 한글 인자를 넘기면 깨지므로).

  python .tools/publish_note_scheduled.py
  python .tools/publish_note_scheduled.py --dry-run

안전장치
  - 큐가 비어 있으면 아무것도 하지 않는다
  - 슬러그 폴더가 없거나 이미 공개 상태면 건너뛴다
  - 본문이 비어 있는 글("본문 미작성" 포함)은 발행하지 않고 큐에 남긴다
  - 작업 트리에 단상/ 밖의 수정사항이 있으면 커밋하지 않고 멈춘다
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
QUEUE = TOOLS / "notes_publish_queue.txt"
LOG = TOOLS / "notes_publish.log"
NOT_READY = "본문 미작성"


try:  # 콘솔이 cp949여도 한글 로그가 깨지지 않게
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def log(msg: str) -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# 비대화형 환경에서 git이 자격증명 입력을 기다리며 멈추지 않도록
GIT_ENV = {
    **os.environ,
    "GIT_TERMINAL_PROMPT": "0",
    "GCM_INTERACTIVE": "never",
    "GIT_ASKPASS": "",
    "SSH_ASKPASS": "",
}

# fsmonitor 데몬은 다른 세션에서 붙으면 교착할 수 있어 이 스크립트에서는 끈다
GIT = ["git", "-c", "core.fsmonitor=false"]


def run(args, check=True, timeout=600, label=None):
    """모든 외부 명령에 타임아웃을 건다. 멈추면 조용히 매달리지 말고 죽고 기록한다."""
    name = label or " ".join(args[:3])
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


def read_queue() -> list[str]:
    if not QUEUE.exists():
        return []
    out = []
    for ln in QUEUE.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def drop_from_queue(slug: str) -> None:
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    kept = [ln for ln in lines if ln.strip() != slug]
    QUEUE.write_text("\n".join(kept) + "\n", encoding="utf-8")


def main() -> int:
    dry = "--dry-run" in sys.argv
    queue = read_queue()
    if not queue:
        log("queue empty — nothing to publish")
        return 0

    slug = queue[0]
    page = ROOT / "단상" / slug / "index.html"
    if not page.exists():
        log(f"SKIP {slug}: page not found")
        return 1

    html = page.read_text(encoding="utf-8")
    if "noindex" not in html:
        log(f"SKIP {slug}: already published — dropping from queue")
        if not dry:
            drop_from_queue(slug)
        return 0
    if NOT_READY in html:
        log(f"HOLD {slug}: body not written — left in queue")
        return 1

    # 단상/ 밖에 커밋 안 된 변경이 있으면 멈춘다 (남의 작업을 같이 커밋하지 않도록)
    st = run(GIT + ["status", "--porcelain"], check=False, timeout=120, label="git status")
    dirty = [ln[3:] for ln in st.stdout.splitlines() if ln.strip()]
    outside = [f for f in dirty if not f.startswith("단상/")]
    if outside:
        log(f"ABORT: uncommitted changes outside 단상/ ({len(outside)} files) — {outside[:3]}")
        return 1

    if dry:
        log(f"DRY-RUN would publish {slug}")
        return 0

    log(f"publishing {slug}")
    run([sys.executable, str(TOOLS / "new_note.py"), "--publish", slug], timeout=120, label="new_note --publish")
    run([sys.executable, str(TOOLS / "rebuild_seo.py")], timeout=900, label="rebuild_seo")

    if "noindex" in page.read_text(encoding="utf-8"):
        log(f"ABORT {slug}: robots meta not flipped")
        return 1

    run(GIT + ["add", "-A"], timeout=180, label="git add")
    msg = f"단상 예약 발행: {slug}"
    # rebuild_seo 를 위에서 이미 돌렸으므로 pre-commit 훅(같은 작업 반복)은 건너뛴다.
    # 훅 안에서 git 을 중첩 호출하다 교착이 났던 지점.
    c = run(GIT + ["commit", "--no-verify", "-m", msg], check=False, timeout=300, label="git commit")
    if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
        log(f"FAIL commit :: {(c.stderr or c.stdout).strip()[:300]}")
        return 1
    p = run(GIT + ["push", "origin", "main"], check=False, timeout=300, label="git push")
    if p.returncode != 0:
        log(f"FAIL push :: {(p.stderr or p.stdout).strip()[:300]}")
        return 1

    drop_from_queue(slug)
    remaining = read_queue()
    log(f"published /단상/{slug}/ — pushed. queue left: {len(remaining)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
