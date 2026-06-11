#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""간다 GO — 동대문 출장마사지 사이트 정적 빌드 스크립트.

- 공통 셸(헤더/네비/푸터)에 페이지별 고유 본문을 결합해 정적 HTML을 생성한다.
- 본문(태그 제거 후) 2,000자 미만 페이지는 자동으로 noindex 처리한다.
- sitemap.xml / robots.txt 를 함께 생성한다.

사용법: python3 build.py
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "content"))

from core import PAGES as CORE_PAGES          # noqa: E402
from dongs import PAGES as DONG_PAGES         # noqa: E402
from stations import PAGES as STATION_PAGES   # noqa: E402
from themes import PAGES as THEME_PAGES       # noqa: E402
from pages import PAGES as ETC_PAGES          # noqa: E402

# 배포 도메인 확정 후 반드시 교체할 것
BASE_URL = "https://www.example.com"
SITE_NAME = "간다 GO"
PHONE = "0508-202-4719"
PHONE_TEL = "0508-202-4719"
MIN_INDEX_CHARS = 2000

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_PAGES = CORE_PAGES + DONG_PAGES + STATION_PAGES + THEME_PAGES + ETC_PAGES

DONG_MENU = [
    ("dongdaemun-gu/", "동대문구 전체"),
    ("dongdaemun-gu/sinseol-dong/", "신설동"),
    ("dongdaemun-gu/yongdu-dong/", "용두동"),
    ("dongdaemun-gu/jegi-dong/", "제기동"),
    ("dongdaemun-gu/jeonnong-dong/", "전농동"),
    ("dongdaemun-gu/dapsimni-dong/", "답십리동"),
    ("dongdaemun-gu/jangan-dong/", "장안동"),
    ("dongdaemun-gu/cheongnyangni-dong/", "청량리동"),
    ("dongdaemun-gu/hoegi-dong/", "회기동"),
    ("dongdaemun-gu/hwigyeong-dong/", "휘경동"),
    ("dongdaemun-gu/imun-dong/", "이문동"),
]

STATION_MENU = [
    ("dongdaemun-gu/stations/", "동대문 지하철역 전체"),
    ("dongdaemun-gu/stations/sinseol-dong-station/", "신설동역"),
    ("dongdaemun-gu/stations/yongdu-station/", "용두역"),
    ("dongdaemun-gu/stations/jegi-dong-station/", "제기동역"),
    ("dongdaemun-gu/stations/cheongnyangni-station/", "청량리역"),
    ("dongdaemun-gu/stations/hoegi-station/", "회기역"),
    ("dongdaemun-gu/stations/hankuk-univ-foreign-studies-station/", "외대앞역"),
    ("dongdaemun-gu/stations/sinimun-station/", "신이문역"),
    ("dongdaemun-gu/stations/dapsimni-station/", "답십리역"),
    ("dongdaemun-gu/stations/janghanpyeong-station/", "장한평역"),
]

THEME_MENU = [
    ("themes/", "전체 테마"),
    ("themes/swedish/", "스웨디시"),
    ("themes/lomi-lomi/", "로미로미"),
    ("themes/thai-massage/", "타이마사지"),
    ("themes/chinese-massage/", "중국마사지"),
    ("themes/aromatherapy/", "아로마테라피"),
    ("themes/home-care/", "홈케어"),
    ("themes/hotel-style/", "호텔식마사지"),
    ("themes/foot-massage/", "발마사지"),
    ("themes/sports/", "스포츠·경락"),
    ("themes/skin-care/", "스킨케어"),
    ("themes/waxing/", "왁싱"),
    ("themes/couple/", "커플 관리"),
    ("themes/24-hours/", "24시간"),
    ("themes/sleep-friendly/", "수면 가능"),
]

NAV = [
    ("", "홈", None),
    ("service/", "동대문 출장마사지", None),
    ("dongdaemun-gu/", "지역별 안내", DONG_MENU),
    ("dongdaemun-gu/stations/", "지하철역별 안내", STATION_MENU),
    ("themes/", "테마별 안내", THEME_MENU),
    ("courses/", "코스안내", None),
    ("reservation/", "예약안내", None),
    ("guide/", "이용가이드", None),
    ("reviews/", "후기", None),
    ("support/", "고객센터", None),
]


def nav_html(current_path):
    items = []
    for path, label, sub in NAV:
        cls = ' class="active"' if path == current_path else ""
        if sub:
            links = "".join(
                '<li><a href="/{p}">{t}</a></li>'.format(p=p, t=html.escape(t))
                for p, t in sub
            )
            items.append(
                '<li class="has-sub"><a{c} href="/{p}">{t}</a>'
                '<ul class="sub">{links}</ul></li>'.format(
                    c=cls, p=path, t=html.escape(label), links=links
                )
            )
        else:
            items.append(
                '<li><a{c} href="/{p}">{t}</a></li>'.format(
                    c=cls, p=path, t=html.escape(label)
                )
            )
    return "".join(items)


def visible_text_len(body_html):
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


SHELL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{robots}<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{site}">
<meta property="og:locale" content="ko_KR">
<link rel="stylesheet" href="/assets/css/style.css">
{jsonld}</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">{site}<span class="brand-sub">동대문 출장마사지</span></a>
    <a class="header-phone" href="tel:{tel}">{phone}</a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
    <label for="nav-toggle" class="nav-toggle-label" aria-label="메뉴 열기"><span></span><span></span><span></span></label>
    <nav class="site-nav" aria-label="주 메뉴"><ul>{nav}</ul></nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<aside class="cta-bar">
  <div class="wrap cta-inner">
    <p><strong>{site}</strong> 예약·상담 문의</p>
    <a class="btn-call" href="tel:{tel}">{phone} 전화 상담</a>
  </div>
</aside>
<footer class="site-footer">
  <div class="wrap">
    <p><strong>{site}</strong> · 동대문 출장마사지·홈타이 안내 · 문의 <a href="tel:{tel}">{phone}</a></p>
    <p class="footer-links"><a href="/support/privacy/">개인정보처리방침</a> · <a href="/support/terms/">이용약관</a> · <a href="/support/">고객센터</a></p>
    <p class="footer-note">본 사이트는 건전한 방문 관리 서비스 안내를 목적으로 하며, 불법적인 서비스는 일체 제공하지 않습니다.</p>
    <p class="copyright">&copy; {site}. All rights reserved.</p>
  </div>
</footer>
</body>
</html>
"""


def build():
    seen = set()
    sitemap_entries = []
    report = []

    for page in ALL_PAGES:
        path = page["path"]
        if path in seen:
            raise SystemExit("중복 경로: " + path)
        seen.add(path)

        body = page["body"]
        length = visible_text_len(body)
        noindex = page.get("noindex", False) or length < MIN_INDEX_CHARS
        robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ""
        canonical = BASE_URL + "/" + path
        jsonld = page.get("jsonld", "")

        doc = SHELL.format(
            title=html.escape(page["title"]),
            description=html.escape(page["description"]),
            robots=robots,
            canonical=canonical,
            site=SITE_NAME,
            tel=PHONE_TEL,
            phone=PHONE,
            nav=nav_html(path),
            body=body,
            jsonld=jsonld,
        )

        out_path = os.path.join(OUT_DIR, path, "index.html") if path else os.path.join(OUT_DIR, "index.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(doc)

        if not noindex:
            sitemap_entries.append(canonical)
        report.append((path or "(home)", length, "noindex" if noindex else "index"))

    urls = "".join(
        "  <url><loc>{u}</loc></url>\n".format(u=u) for u in sitemap_entries
    )
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "</urlset>\n"
        )

    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: {b}/sitemap.xml\n".format(b=BASE_URL))

    print("{:<55} {:>6}  {}".format("PATH", "CHARS", "ROBOTS"))
    for p, n, r in sorted(report):
        print("{:<55} {:>6}  {}".format(p, n, r))
    print("\n총 {}페이지, sitemap 등록 {}페이지".format(len(report), len(sitemap_entries)))


if __name__ == "__main__":
    build()
