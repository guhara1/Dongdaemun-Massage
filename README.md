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

## 색인·인덱싱 인프라

빌드 시 자동 생성됩니다.

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 전 인덱스 페이지 + `lastmod` (구글·네이버·빙 공통) |
| `rss.xml` | 최신 글 우선 49개 아이템 — 네이버 서치어드바이저 RSS 제출용 |
| `robots.txt` | Googlebot·Yeti(네이버)·Bingbot 명시 허용 + sitemap/rss 위치 |
| `{IndexNow키}.txt` | IndexNow 키 검증 파일 (키는 `content/site.py`) |

### 글 올릴 때마다 즉시 색인 통보

```bash
python3 build.py                      # 재빌드 (sitemap·rss 갱신)
python3 scripts/notify_index.py      # sitemap 전체 URL을 IndexNow로 통보 (빙·네이버)
python3 scripts/notify_index.py /magazine/new-post/   # 특정 URL만 통보
```

- **IndexNow**: 빙·네이버 등 참여 엔진에 즉시 전파. 별도 설정 불필요(키 파일이 배포에 포함됨).
- **구글**: IndexNow 미참여. 기본 경로는 Search Console sitemap 제출이며,
  서비스 계정 키를 두면(`GOOGLE_SA=키.json`) Indexing API 통보도 함께 실행됩니다.
  단, Indexing API의 공식 지원 대상은 구인·라이브방송 페이지라는 점은 유의하세요.
- 구형 sitemap ping(google.com/ping 등)은 2023~2024년 폐지되어 사용하지 않습니다.
- 콘텐츠를 수정한 날에는 `content/site.py`의 `SITE_UPDATED`를 갱신하세요(sitemap `lastmod` 반영).

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt·rss.xml에 반영됨)
3. Google Search Console·네이버 서치어드바이저에 `sitemap.xml` 제출, 네이버에는 `rss.xml`도 제출
4. 배포 확인 후 `python3 scripts/notify_index.py` 실행 (IndexNow 첫 통보)
