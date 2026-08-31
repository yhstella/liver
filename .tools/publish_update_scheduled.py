#!/usr/bin/env python3
"""
publish_update_scheduled.py — updates/ 드래프트 하나를 예약 발행하고 push까지 한다.

발행 대상 선정은 publish_next_draft.py 에 맡긴다
(.tools/publish_priority.txt 순서 → 없으면 git 최초 커밋 순).

  python .tools/publish_update_scheduled.py
  python .tools/publish_update_scheduled.py --dry-run

단상용 publish_note_scheduled.py 와 같은 안전장치를 쓴다. 두 스크립트가 helper 를
공유하지 않고 각자 갖고 있는 것은, 한쪽을 고치다 다른 쪽 예약 발행을 깨뜨리지
않기 위해서다(2026-08-19 교착 사고 이후).

안전장치
  - 드래프트가 없으면 아무것도 하지 않는다
  - 작업 트리에 updates/ 밖의 수정사항이 있으면 커밋하지 않고 멈춘다
  - 모든 외부 명령에 타임아웃 (멈추면 매달리지 말고 기록하고 죽는다)
  - 비대화형 git 강제 (자격증명 창을 기다리지 않는다)
  - rebuild_seo 를 직접 돌리므로 pre-commit 훅은 건너뛴다 (훅 안 git 중첩 호출이 교착 지점이었다)
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
LOG = TOOLS / "updates_publish.log"

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
}
GIT = ["git", "-c", "core.fsmonitor=false"]


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


def next_slug():
    r = run([sys.executable, str(TOOLS / "publish_next_draft.py"), "--dry-run"],
            check=False, timeout=120, label="publish_next_draft --dry-run")
    out = (r.stdout or "").strip()
    try:
        return json.loads(out).get("wouldPublish")
    except Exception:
        return None


def main() -> int:
    dry = "--dry-run" in sys.argv

    slug = next_slug()
    if not slug:
        log("발행할 드래프트가 없습니다 — 대기열 비어 있음")
        return 0

    st = run(GIT + ["status", "--porcelain"], check=False, timeout=120, label="git status")
    dirty = [ln[3:] for ln in st.stdout.splitlines() if ln.strip()]
    outside = [f for f in dirty if not f.startswith("updates/")]
    if outside:
        log(f"ABORT: updates/ 밖에 커밋 안 된 변경 {len(outside)}건 — {outside[:3]}")
        return 1

    if dry:
        log(f"DRY-RUN would publish {slug}")
        return 0

    log(f"publishing {slug}")
    run([sys.executable, str(TOOLS / "publish_next_draft.py")], timeout=180, label="publish_next_draft")

    page = ROOT / "updates" / slug / "index.html"
    if not page.exists() or "noindex" in page.read_text(encoding="utf-8"):
        log(f"ABORT {slug}: robots meta not flipped")
        return 1

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

    left = next_slug()
    log(f"published /updates/{slug}/ — pushed. 남은 드래프트: {'없음' if not left else left}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
