# 간다 GO — 동대문 출장마사지·홈타이 안내 사이트

동대문구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

`동대문구 > 대표 동 > 역세권 > 테마` 분리 구조로 도어웨이·중복·얇은 콘텐츠 위험을
줄이는 SEO 설계안을 구현했으며, 디자인·UI는 기존 사이트 프레임워크(다크 골드 테마,
히어로, 좌측 목차, 브레드크럼, 요금 블록, 전화 FAB)를 그대로 사용합니다.

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ 히어로, LocalBusiness/FAQPage JSON-LD)
  core.py           # 동대문 출장마사지 안내(/massage/) + 지역·역·테마 허브
  dongs.py          # 지역별: 대표 동 10개 (신설동~이문동)
  stations.py       # 지하철역별: 9개 역 (환승역 URL 통합)
  themes_a.py/_b.py # 테마별: 14개 테마
  pages.py          # 코스·예약·가이드·후기·고객센터·약관
  magazine.py       # 매거진(정보성 아티클 6편 + 허브)
  about.py          # 운영자 소개
  pricing.py        # 공통 요금 블록 (글자수 집계에서 제외)
  __init__.py       # 페이지 집계 + 콘텐츠 형식 변환기
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
scripts/gen_assets.py  # 브랜드 아이콘·OG 이미지 재생성 (Pillow 필요)
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 지역은 대표 동 10개만 — 숫자 행정동(전농1·2동 등) 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승역도 URL 하나, 출구별 페이지 없음
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 상단/하위 메뉴와 푸터에 키워드·지역명·역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)
- 후기·고객센터·약관은 실콘텐츠가 채워지기 전까지 의도적 noindex

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console에 `sitemap.xml` 제출
