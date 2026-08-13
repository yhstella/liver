export const meta = {
  name: 'drshin-apply-factcheck-fixes',
  description: 'fact-check에서 확인된 MAJOR 의학 오류 17페이지 수정 (검증된 사실 적용)',
  phases: [{ title: 'Apply fixes' }],
}

const ROOT = "C:/Users/R/Dropbox/drshin.kr"
const FACTS = "검증된 사실(이대로 반영):\n- CheckMate 9DW(nivolumab+ipilimumab) 진행성 HCC 1차 FDA 승인: 2025년 4월 11일. (2024년은 ESMO 학회 발표 시점이지 승인 아님)\n- 세마글루타이드(Wegovy) MASH 적응증 FDA 가속승인: 2025년 8월 15일. 비간경변 F2-F3 섬유화. ESSENCE phase 3에서 MASH 해소 62.9% vs 위약 34.3%.\n- Bulevirtide(Hepcludex) FDA 가속승인: 2026년 5월 22일.\n- B-Clear(bepirovirsen phase 2b): N Engl J Med 2022;387:1957-1968. (Lancet 아님, 2024 아님)\n- Survodutide phase 2(Sanyal): N Engl J Med 2024(NEJMoa2401755). MASH 호전(섬유화 악화 없이) 용량별 47%/62%/43% vs 위약 14% (최대 62%, \"80%\"는 틀림). Lancet 아님.\n- 대상성 간경변에서 GLE/PIB 8주는 유전형 1~6형 모두 승인. 12주 연장 고려 대상은 1형이 아니라 3형(baseline NS5A RAS).\n- Avatrombopag: baseline 혈소판 <40,000/μL → 60mg/일 5일, 40,000~<50,000 → 40mg/일 5일."
const FIXES = [
  { path: "C형간염-2025-KASL-가이드라인/index.html", fix: "본문 '대상성 간경변'에서 'GLE/PIB 8주는 일부 1형 환자에서 12주로 연장 권고'를 '일부 3형(유전형 3) 환자에서는 baseline 내성·치료 반응을 고려해 12주를 검토'로 수정. (1형이 아니라 3형이 맞음)" },
  { path: "D형간염-치료-가이드라인/index.html", fix: "Bulevirtide FDA 승인 연도가 페이지 곳곳에 '2024'로 적혀 TLDR(2026-05)과 모순. 모든 'FDA 가속 2024'·'2024 FDA'를 '2026년 5월(FDA 가속승인)'로 통일. 핵심정보 표·결론·FAQ·본문 전부." },
  { path: "updates/Bepirovirsen-HBV-Lancet-2024/index.html", fix: "B-Clear를 'Lancet 2023/2024'·'NEJM/Lancet 2024'로 표기한 것을 'N Engl J Med 2022;387:1957-1968 (B-Clear, phase 2b)'로 정정. 제목·meta description·og·본문·References의 'Lancet 2024'를 'NEJM 2022'로. 단 slug/canonical/JSON-LD url은 그대로 둘 것(파일 경로라 못 바꿈)." },
  { path: "updates/ESSENCE-survodutide-MASH-Lancet-2024/index.html", fix: "이 글은 survodutide를 다룸. (1) 'NASH 호전 약 80%'·'60~80%'를 '위약 14% 대비 용량에 따라 약 47~62%에서 MASH 호전(섬유화 악화 없이)'로 수정. (2) 저널 'Lancet 2024'·'NEJM/Lancet'을 'N Engl J Med 2024(Sanyal AJ et al. NEJMoa2401755)'로 통일. slug/canonical/JSON-LD url은 파일 경로라 그대로." },
  { path: "updates/Klausen-Semaglutide-AUD-Lancet-2026/index.html", fix: "'첫 phase-3급 RCT' 표현(TLDR·BACKGROUND)을 '소규모(108명) 무작위 시험'으로 수정하고 'phase-3급' 삭제. SEMALCO는 N=108 소규모 탐색 시험이라 phase-3급은 과대표현." },
  { path: "간경변-감염-SBP-예방/index.html", fix: "SBP 사망률이 한 페이지에 3개 값(TLDR '20~30%', 본문 '60~70%', FAQ '30~50%')으로 충돌. TLDR을 '입원(단기) 사망률 약 20~40%, 첫 발생 후 1년 사망률 약 50~70%'로 분리 표기하고, FAQ의 1년 사망률도 본문(50~70%)과 통일. 문헌상 1년 사망률 ~60%." },
  { path: "간경변-복수/index.html", fix: "'Tapper JAMA 2023 review에 따르면 ... 복수 해소율이 높음(76% vs 56%)'에서 출처에 추적 안 되는 76% vs 56% 수치를 삭제하고 '병용이 단계적 단독보다 더 빠른 해소·낮은 실패율을 보인다'는 정성 표현으로 교체. 임상 결론(병용이 표준)은 유지." },
  { path: "간암-면역치료-1차/index.html", fix: "(1) 'Ipilimumab+Nivolumab(CheckMate 9DW) 2024년 FDA 1차 승인'이 표·본문·보험 섹션에 3회. 모두 '2025년 미국 FDA 1차 승인(CheckMate 9DW, ESMO 2024 발표)'로 수정. (2) 옵션 표 캡션 'NCCN 2026 기준 모두 Category 1'을 '환자별 동반 질환·출혈 위험으로 결정(atezo+bev·STRIDE·ipi+nivo가 선호 1차)'로 완화하고 '모두 Category 1' 삭제." },
  { path: "간양성종양-낭종-관리/index.html", fix: "'tolvaptan(somatostatin analog 또는 vasopressin antagonist)'를 'tolvaptan(바소프레신 V2 수용체 길항제)'로 수정. tolvaptan은 V2 길항제 단일 기전이고 somatostatin analog가 아님(소마토스타틴 유사체는 octreotide/lanreotide로 별개). 간 부피 감소 효과는 '주로 신장 낭종(ADPKD)에 적응증이고 간 효과는 제한적'으로 톤 완화." },
  { path: "지방간-SGLT2-GLP1/index.html", fix: "세마글루타이드 MASH 적응증을 미래시제('ESSENCE 결과 발표 후 결정될 가능성', 'MASH 적응증 추가 가능성')로 적은 부분을 사실로 갱신: '2025년 8월 미국 FDA가 비간경변 MASH(F2-F3)에 세마글루타이드(위고비)를 가속승인했습니다(ESSENCE phase 3, MASH 해소 62.9% vs 위약 34.3%)'. 국내 적응증·급여는 별도로 '국내는 아직 비만 적응증 중심'임을 표기." },
  { path: "케이스/MASLD-HCC-비만당뇨/index.html", fix: "섬유화 병기가 F2(intro·첫만남)와 F3(SVG 도식·병리)로 모순. 한 병기로 통일하되, 추적 중 F2였다가 절제 병리에서 F3 확인된 경과라면 그렇게 명시적으로 서술. 임의로 병기를 만들지 말고 페이지 내 다수 표기(F3 병리)에 맞춰 일관되게." },
  { path: "케이스/MetALD-당뇨-음주/index.html", fix: "환자 음주량 '주 200 g'이 같은 페이지 pearl의 남성 MetALD 역치(210~420 g/주) 미달이라 자기모순. 음주량을 남성 MetALD 범위(예: 주 약 250 g)로 상향해 MetALD 분류와 일치시킬 것." },
  { path: "케이스/약물성간손상-항결핵제/index.html", fix: "도입부 '잠복 결핵 양성 진단 후 isoniazid+rifampin+pyrazinamide+ethambutol 4제(HRZE) 표준 치료'가 틀림 — 4제 HRZE는 활동성 결핵 요법이고 잠복결핵은 INH 단독/RIF/INH+RIF로 치료(PZA·EMB 안 씀). 본문 후반(9개월 연장 등)이 활동성 결핵 틀이므로 도입부를 '활동성 폐결핵 진단 후 표준 4제(HRZE)'로 통일." },
  { path: "케이스/임신중-HBsAg발견/index.html", fix: "case-pearl·teaching points의 깨진 표기 'HBV DNA ≥ 2 IU/mL×10⁵ IU/mL'(2곳)를 'HBV DNA ≥ 2×10⁵ IU/mL (200,000 IU/mL)'로 수정. 임신 중 항바이러스제(TDF) 시작 역치." },
  { path: "케이스/정맥류출혈이력-STRIDE/index.html", fix: "임상 트리비아(pearl) 박스가 종양학 STRIDE를 'Baveno VII STRIDE(문맥압 관리)'로 잘못 설명. Baveno VII에 STRIDE 정의 없음. pearl 박스를 종양학 STRIDE 설명으로 교체: 'STRIDE = tremelimumab 1회 priming + durvalumab 유지(HIMALAYA), CTLA-4 single high-priming 개념'. 'Baveno VII' 문장 삭제." },
  { path: "케이스/큰낭종-bleomycin-경화요법/index.html", fix: "'블레오마이신 주입 — 60,000 IU(약 60 mg)'는 통상 상한 초과. 구체 수치를 빼고 '체중·낭종 크기 기준으로 용량 결정(통상 회당 약 15~45 unit 범위)'로 일반화. 'IU' 표기는 'unit'으로." },
  { path: "케이스/큰종양-TACE-SBRT-결합/index.html", fix: "(1) 'STRBED, TACE-HIGH' 시험명은 확인되지 않는 미확인/조작 의심 시험이라 인용 삭제, 'TACE+SBRT 결합의 데이터가 누적되는 단계'로 톤 다운. (2) 'TACE+SBRT 국소 통제율 약 85%(LEAP-012)'에서 LEAP-012는 TACE+렌바티닙/펨브롤리주맙 시험(SBRT 아님)이라 명백한 오인용 — LEAP-012 인용 삭제하고 구체 수치 단정 회피." }
]

function prompt(item) {
  return `당신은 환자용 간 질환 의료정보 사이트(drshin.kr)의 의학 오류를 정확히 교정하는 간 전문의 에디터다.

## 대상 파일
${ROOT}/${item.path}

## ${FACTS}

## 적용할 수정 (정확히 이것만)
${item.fix}

## 규칙
- 파일을 Read한 뒤, 위 수정을 적용한다(Edit).
- 본문에서 고친 사실은 같은 페이지의 meta description·og·JSON-LD에도 같은 의미로 일관되게 반영한다(단 canonical/url/@id 같은 파일 경로성 필드는 절대 바꾸지 않는다).
- 위에 명시된 수정 외에 의학 내용을 임의로 추가·변경하지 않는다. 확신이 안 서면 더 보수적인(덜 단정적인) 표현을 택한다.
- 자연스러운 한국어 진료실 어조 유지.

## 출력 (한국어 1~2줄) + 마지막 한 줄:
RESULT: page=${item.path} | applied=<yes|partial|no> | note=<무엇을 어떻게 고쳤는지 또는 못 고친 이유>`
}

phase('Apply fixes')
log(`Applying fixes to ${FIXES.length} pages`)

const reports = []
const BATCH = 5
for (let i = 0; i < FIXES.length; i += BATCH) {
  const slice = FIXES.slice(i, i + BATCH)
  const part = await parallel(
    slice.map((item) => () =>
      agent(prompt(item), { phase: 'Apply fixes', label: item.path.split('/').pop().slice(0, 20) })
    )
  )
  reports.push(...part)
  log(`batch ${Math.floor(i / BATCH) + 1} done (${reports.filter(Boolean).length}/${reports.length})`)
}

const results = reports.map((r, i) => {
  if (!r) return { page: FIXES[i].path, status: 'FAILED' }
  const m = r.match(/RESULT:\s*(.+)$/m)
  return { page: FIXES[i].path, resultLine: m ? m[1].trim() : '(no RESULT)' }
})

return { total: FIXES.length, applied: reports.filter(Boolean).length, results }
