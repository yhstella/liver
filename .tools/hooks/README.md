# Git hooks — drshin.kr

이 폴더는 사이트 콘텐츠 변경 시 자동으로 SEO/GEO 자산(홈 '최근 작성글', sitemap, llms.txt, search-index 등)을 갱신하는 git 훅을 담고 있습니다.

## 설치 (PC당 한 번)

```bash
git config core.hooksPath .tools/hooks
```

확인:
```bash
git config --get core.hooksPath
# → .tools/hooks
```

## 동작

`pre-commit` 훅은 다음 조건에서 자동으로 `rebuild_seo.py`를 실행하고 갱신된 자산을 같은 커밋에 포함시킵니다.

- staged 변경에 `.html` 파일이 포함되어 있을 때
- `.tools/` 또는 `assets/` 안의 변경만 있는 경우는 건너뜀 (자산 회귀 방지)

rebuild 실패 시 커밋이 차단되어 사이트 일관성이 보장됩니다.

## 우회 (긴급 시)

```bash
git commit --no-verify -m "긴급 hotfix"
```

## 새 PC에서 작업할 때

drshin.kr 폴더를 Dropbox로 동기화한 새 PC에서는 git 설정이 따라오지 않으므로 한 번만:

```bash
cd C:/Users/R/Dropbox/drshin.kr   # 또는 D:/Dropbox/drshin.kr
git config core.hooksPath .tools/hooks
```
