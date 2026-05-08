"""Render plaintext guide HTML from structure.json."""
import json
import html as htmllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / ".tools" / "structure.json").read_text(encoding="utf-8"))

def esc(s: str) -> str:
    return htmllib.escape(s or "")

def clean_h1(s: str) -> str:
    return s.replace("<br>", " — ").replace("<br/>", " — ").replace("<br />", " — ")

# Counts
total = sum(len(v) for v in data.values())
series_counts = {k: len(v) for k, v in data.items()}

# Quality flags
missing_tldr = []
missing_faq = []
for series, articles in data.items():
    for a in articles:
        if not a.get("tldr"):
            missing_tldr.append(a)
        if not a.get("faq"):
            missing_faq.append(a)

parts = []
parts.append(f"""
<section class="overview">
  <h2>사이트 한눈에</h2>
  <div class="stats">
    <div><strong>{total}</strong><span>총 글 수</span></div>
    <div><strong>{len(data)}</strong><span>시리즈</span></div>
    <div><strong>{len(missing_tldr)}</strong><span>tldr 누락</span></div>
    <div><strong>{len(missing_faq)}</strong><span>FAQ 누락</span></div>
  </div>
  <ul class="convention">
    <li>URL 패턴: <code>/{{한글-슬러그}}/</code> — 폴더당 <code>index.html</code> 한 개</li>
    <li>head 구성: title · description · canonical · og · twitter · JSON-LD (MedicalWebPage + Person + FAQPage + BreadcrumbList)</li>
    <li>본문 구조: h1 → <code>.tldr</code> → h2 섹션 4–7개 → FAQ <code>&lt;details&gt;</code> → author-box → related → disclaimer</li>
    <li>스타일시트: 단일 <code>/style.css</code> (Pretendard 폰트, accent #1f6f5c, max-width 720px)</li>
  </ul>
""")

if missing_tldr or missing_faq:
    parts.append("""
  <div class="alert">
    <strong>구조 불일치 감지</strong>
    <p>시리즈 1·2는 모두 tldr 박스 + 5개 FAQ를 가지고 있으나, 시리즈 3 (B형·C형 간염) 6개 글은 tldr와 FAQ가 비어있습니다. h1에 <code>&lt;br&gt;</code>이 들어간 점, modified date가 없는 점도 시리즈 1·2와 다릅니다. 시리즈 3을 1·2와 같은 패턴으로 보강하면 SEO·LLM 일관성 모두 개선됩니다.</p>
  </div>
""")

parts.append("</section>")

# Series cards
for series, articles in data.items():
    parts.append(f'<section class="series">\n<h2>{esc(series)} <span class="count">{len(articles)}</span></h2>\n<div class="cards">\n')
    for a in articles:
        h1 = esc(clean_h1(a["h1"]))
        slug = esc(a["slug"])
        url = esc(a["url"])
        desc = esc(a["description"])
        tldr = esc(a["tldr"]) if a["tldr"] else ""
        published = esc((a["published"] or "")[:10])
        modified = esc((a["modified"] or "")[:10]) if a["modified"] else ""
        sections = a["sections"]
        faq = a["faq"]

        parts.append(f'<article class="card">\n')
        parts.append(f'  <div class="card-head">\n')
        parts.append(f'    <code class="slug">{slug}</code>\n')
        parts.append(f'    <a class="visit" href="{url}" target="_blank" rel="noopener">열기 ↗</a>\n')
        parts.append(f'  </div>\n')
        parts.append(f'  <h3>{h1}</h3>\n')
        parts.append(f'  <p class="desc">{desc}</p>\n')

        if tldr:
            parts.append(f'  <div class="tldr-mini"><strong>핵심</strong> {tldr}</div>\n')
        else:
            parts.append(f'  <div class="tldr-mini empty"><strong>핵심</strong> <em>(tldr 없음 — 보강 필요)</em></div>\n')

        if sections:
            parts.append(f'  <div class="block">\n    <strong>섹션 ({len(sections)})</strong>\n    <ol>\n')
            for s in sections:
                if s == "같이 읽으면 좋은 글" or s == "관련 글":
                    parts.append(f'      <li class="muted">{esc(s)}</li>\n')
                else:
                    parts.append(f'      <li>{esc(s)}</li>\n')
            parts.append(f'    </ol>\n  </div>\n')

        if faq:
            parts.append(f'  <div class="block">\n    <strong>FAQ ({len(faq)})</strong>\n    <ul class="faq">\n')
            for q in faq:
                parts.append(f'      <li>{esc(q)}</li>\n')
            parts.append(f'    </ul>\n  </div>\n')
        else:
            parts.append(f'  <div class="block empty"><strong>FAQ</strong> <em>(없음 — 보강 필요)</em></div>\n')

        parts.append(f'  <div class="dates">\n')
        parts.append(f'    <span>발행 {published}</span>\n')
        if modified and modified != published:
            parts.append(f'    <span>수정 {modified}</span>\n')
        elif not modified:
            parts.append(f'    <span class="warn-inline">수정일 없음</span>\n')
        parts.append(f'  </div>\n')
        parts.append(f'</article>\n')
    parts.append('</div>\n</section>\n')

# Series 4 placeholder
parts.append("""
<section class="series upcoming">
  <h2>시리즈 4 · /updates (논문 노트 · 전문가용) <span class="count">0</span></h2>
  <p class="placeholder">
    의료진·전공의 대상 hepatology 논문·가이드라인 업데이트 노트.
    환자용 글과 톤·구조가 다릅니다 (Background → Methods → Findings → Critique → References).
    JSON-LD type은 <code>ScholarlyArticle</code>, audience는 <code>Physician</code>.
    URL 패턴: <code>/updates/{학회-연도-키워드}/</code>.
  </p>
  <p class="placeholder">아직 글이 없습니다. <a href="/updates/" target="_blank" rel="noopener">/updates/ 허브 페이지 ↗</a></p>
</section>
""")

# Coverage gaps
parts.append("""
<section class="gaps">
  <h2>아직 다루지 않은 주요 주제</h2>
  <p>현재 17개 글은 외래에서 자주 받는 질문을 잘 커버하지만, 다음 주제는 환자 검색량·임상 빈도 대비 비어 있습니다. 우선순위 참고용.</p>
  <div class="gap-grid">
    <div>
      <strong>간경변</strong>
      <ul>
        <li>대상성 vs 비대상성 차이</li>
        <li>복수·간성혼수·식도정맥류 첫 신호</li>
        <li>Child-Pugh / MELD 점수가 의미하는 것</li>
        <li>간이식 대상자 평가 흐름</li>
      </ul>
    </div>
    <div>
      <strong>간암</strong>
      <ul>
        <li>간암 진단 후 첫 외래에서 결정되는 것</li>
        <li>BCLC 병기와 치료 옵션</li>
        <li>색전술 · 방사선 · 면역치료 — 무엇이 어떤 환자에게</li>
        <li>간암 재발 감시 일정</li>
      </ul>
    </div>
    <div>
      <strong>약물·간 손상</strong>
      <ul>
        <li>건강기능식품·한약 간독성</li>
        <li>타이레놀 안전 용량</li>
        <li>스타틴은 정말 간에 나쁜가</li>
      </ul>
    </div>
    <div>
      <strong>응급 / 알람 신호</strong>
      <ul>
        <li>황달이 보일 때 24시간 안에 해야 할 것</li>
        <li>토혈·흑변 — 식도정맥류 출혈 신호</li>
        <li>의식 변화·간성혼수 응급도</li>
      </ul>
    </div>
    <div>
      <strong>예방·생활</strong>
      <ul>
        <li>간 건강을 위한 술 한도 — 정확한 숫자</li>
        <li>간염 백신 — 누가, 언제, 몇 번</li>
        <li>건강검진 간 검사 어디까지 받아야 충분한가</li>
      </ul>
    </div>
    <div>
      <strong>기타 임상</strong>
      <ul>
        <li>간 낭종·혈관종 — 우연히 발견됐을 때</li>
        <li>철저장과 간 (혈색소증)</li>
        <li>윌슨병 / 자가면역간염 — 흔치 않지만 놓치면 안 되는 진단</li>
      </ul>
    </div>
  </div>
</section>
""")

content = "".join(parts)

out = ROOT / ".tools" / "guide_content.html"
out.write_text(content, encoding="utf-8")
print(f"Wrote {out} ({len(content)} bytes)")
