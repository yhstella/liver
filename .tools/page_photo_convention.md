# page-photo convention (2026-05-11 update)

## Rule

`page-photo:auto` 블록은 **세부주제(detail) 페이지에만 사용한다**.

대주제(hub) 페이지에는 page-photo가 들어가지 않는다.

## 대주제(hub) 페이지 — page-photo 제외

다음 8개 페이지에는 `<!-- page-photo:auto:start --> ... <!-- page-photo:auto:end -->` 블록을 절대 주입하지 않는다:

- `/간암/index.html`
- `/간경화/index.html`
- `/B형간염/index.html`
- `/C형간염/index.html`
- `/지방간/index.html`
- `/간수치/index.html`
- `/자가면역간염/index.html`
- `/간양성종양/index.html`

이유: hub는 series-meta + identifying SVG infographic + topic-list로 구성되며, 대표 사진이 페이지 흐름을 끊는다. 사진은 detail 페이지의 시각적 anchor 역할로 한정.

## 세부주제(detail) 페이지 — page-photo 사용

`/대주제-세부키워드/index.html` 패턴(예: `/간암-BCLC병기/`, `/B형간염-검사결과/`, `/지방간-치료/`)에는 page-photo 블록을 page-id 또는 first heading 직후에 주입한다.

품질 기준: 사진이 페이지 주제와 직접 연관되어야 한다 (단순 anatomy stock photo X). naming convention `NNN-{topic}-{slug-snippet}-{hash}.jpg`로 topic이 page와 일치해야 한다.

## og:image / twitter:image

대주제 page에서도 og:image 자체는 social card용으로 유지 가능 (visible figure는 아니므로). 다만 향후 Open Graph 전용 placeholder를 따로 만들어 hub와 구분하는 것이 더 깔끔할 수 있음.

## 자동 주입 스크립트 갱신 필요 사항

page-photo를 자동 주입하는 스크립트(Codex가 관리)는 다음을 반영해야 함:
- skip list로 위 8개 hub slug를 제외
- detail 페이지에만 주입
- 재실행 시 hub에 잘못 주입된 블록을 자동 제거 (idempotent)

## 변경 이력

- 2026-05-11: hub 8개 페이지에서 page-photo 블록 수동 제거 (Claude). Codex 측 스크립트 갱신 필요.
