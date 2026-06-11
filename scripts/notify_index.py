#!/usr/bin/env python3
"""검색엔진 즉시 색인 통보 스크립트.

글을 올리거나 수정한 뒤 실행하면:
  1. IndexNow — 빙·네이버(Yeti)·얀덱스 등 참여 엔진에 즉시 통보 (표준 stdlib만 사용)
  2. Google Indexing API — 서비스 계정 키가 있으면 구글에도 통보
     (구글은 IndexNow 미참여. pip install google-auth requests 필요)

usage:
  python3 scripts/notify_index.py                    # sitemap.xml 의 전체 URL 통보
  python3 scripts/notify_index.py /massage/ /about/  # 특정 경로만 통보
  GOOGLE_SA=service-account.json python3 scripts/notify_index.py  # 구글 포함

참고:
  - 구글/빙의 구형 sitemap ping 엔드포인트(google.com/ping, bing.com/ping)는
    2023~2024년에 폐지되어 더 이상 동작하지 않습니다. 구글은 Search Console
    sitemap 제출 + (필요 시) Indexing API, 빙·네이버는 IndexNow 가 현행 경로입니다.
  - 구글 Indexing API 의 공식 지원 대상은 구인(JobPosting)·라이브방송 페이지입니다.
    일반 페이지에도 기술적으로 호출은 가능하지만 정책 외 사용이므로,
    구글 색인의 기본 경로는 Search Console sitemap 제출로 두는 것을 권장합니다.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    xml = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def notify_indexnow(urls):
    host = BASE_URL.split("//", 1)[-1].strip("/")
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"[IndexNow] {len(urls)}개 URL 통보 — HTTP {r.status} (빙·네이버 등 참여 엔진에 전파)")
    except urllib.error.HTTPError as e:
        print(f"[IndexNow] 실패 HTTP {e.code}: {e.read().decode()[:200]}")
        print("  → 키 파일이 배포되어 있는지 확인하세요:",
              f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt")
    except Exception as e:  # noqa: BLE001
        print(f"[IndexNow] 네트워크 오류: {e}")


def notify_google(urls, sa_path):
    try:
        import requests  # noqa: PLC0415
        from google.oauth2 import service_account  # noqa: PLC0415
        from google.auth.transport.requests import Request as GARequest  # noqa: PLC0415
    except ImportError:
        print("[Google] google-auth/requests 미설치 — 건너뜀")
        print("  설치: pip install google-auth requests")
        return
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=["https://www.googleapis.com/auth/indexing"]
    )
    creds.refresh(GARequest())
    headers = {"Authorization": f"Bearer {creds.token}",
               "Content-Type": "application/json"}
    ok = fail = 0
    for url in urls:
        r = requests.post(
            "https://indexing.googleapis.com/v3/urlNotifications:publish",
            headers=headers,
            json={"url": url, "type": "URL_UPDATED"},
            timeout=15,
        )
        if r.status_code == 200:
            ok += 1
        else:
            fail += 1
            print(f"[Google] {url} → HTTP {r.status_code}: {r.text[:150]}")
    print(f"[Google Indexing API] 성공 {ok} / 실패 {fail} (일일 기본 쿼터 200건)")


def main():
    args = sys.argv[1:]
    if args:
        base = BASE_URL.rstrip("/")
        urls = [base + a if a.startswith("/") else a for a in args]
    else:
        urls = sitemap_urls()
    if not urls:
        print("통보할 URL이 없습니다. 먼저 python3 build.py 를 실행하세요.")
        return
    if "example.com" in BASE_URL:
        print("⚠ content/site.py 의 BASE_URL 이 아직 예시 도메인입니다. 실제 도메인으로 바꾼 뒤")
        print("  python3 build.py 를 재실행하고 배포한 다음 이 스크립트를 실행하세요.")
        return

    notify_indexnow(urls)

    sa = os.environ.get("GOOGLE_SA", os.path.join(ROOT, "service-account.json"))
    if os.path.exists(sa):
        notify_google(urls, sa)
    else:
        print("[Google] 서비스 계정 키 없음 — Search Console sitemap 제출이 기본 경로입니다.")
        print("  Indexing API 를 쓰려면 GOOGLE_SA=키파일.json 환경변수로 지정하세요.")


if __name__ == "__main__":
    main()
