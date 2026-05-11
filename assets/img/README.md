# assets/img — public image structure

공개 사이트가 직접 서빙하는 이미지 폴더. 모든 경로는 `/assets/img/...`로 HTML에서 참조됩니다.

## 구조 (2026-05-12 정리)

```
assets/img/
├── README.md            이 파일
├── db/         39M  130  ← 메인 figure DB (Codex 큐레이션, canonical)
├── papers/    3.6M   43  ← 논문 figure (Updates 페이지용)
├── concepts/  2.3M   10  ← 외부 CC 라이선스 stock 이미지 (Wikimedia 등)
├── web/       5.3M    3  ← 수동 추가 web figure (정맥류 결찰·복수 천자·식단)
└── author/    512K    1  ← 저자 사진
```

## 폴더별 역할

### `db/` — figure DB (메인 소스)

**가장 우선적으로 사용**하는 figure 저장소. 원본은 `private-figures/db/`에 있으며 `place_db_figures.py`가 자동 복사·배치.

- 토픽 폴더 6개: `autoimmune_cholestatic/`, `cirrhosis_portal_htn/`, `hcc/`, `imaging/`, `masld_mash/`, `viral_hepatitis/`
- 파일명: `img_XXXXX.png` (또는 `.jpg`)
- 메타데이터: `private-figures/manifest.csv`
- HTML 페이지에는 `<!-- db-figure:auto:start --> ... <!-- db-figure:auto:end -->` 마커로 삽입

### `papers/` — 논문 figure

Updates 페이지(논문 요약)용. `inject_paper_figures.py`가 `private-figures/paper-figures/`에서 복사.
- 폴더명: `{DOI-hash}/figure-NN-name.jpg` 패턴

### `concepts/` — 외부 stock 이미지

Wikimedia Commons 등 CC 라이선스 stock 이미지. 10개만 유지 (3개 토픽: hcc-liver-cancer, liver-anatomy, viral-hepatitis). 신규 추가 안 함 — `db/`가 canonical.

### `web/` — 수동 추가 web figure

특정 페이지에 직접 추가한 시술/도식 이미지 (식도정맥류 결찰, 복수 천자, 지중해식 식단 피라미드). 3개 유지.

### `author/` — 저자 사진

`drshin.jpg` 1개. og:image fallback.

## 신규 figure 추가 워크플로우

1. **원본을 `private-figures/db/{topic}/`에 둠**
2. `private-figures/manifest.csv`에 메타 행 추가
3. `.tools/place_db_figures.py` 실행 → 자동 매칭·복사·삽입

`concepts/`·`web/`에 직접 추가하는 것은 피하기 (`db/`가 canonical).

## 정리 이력

- 2026-05-12: `topics/` (58M, 0 refs), `figures/` (30M, 0 refs) 완전 삭제. `concepts/` 168→10 슬림. dead script(`embed_page_figures.py`, `distribute_figures.py`, `distribute_concept_figures.py`, `embed_real_figures.py`) 제거. 총 142MB → 44MB (-69%).
- 2026-05-12: open-license 보강분을 `db/`에 반영. 공개 DB 101→130장, 특히 `autoimmune_cholestatic`, `cirrhosis_portal_htn`, `masld_mash`, `imaging`, `hcc` 보강.
- 2026-05-11: Codex curated `db/` 추가. `place_db_figures.py`로 101 페이지 자동 배치.
