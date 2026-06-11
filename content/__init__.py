# 전체 페이지 목록 집계.
#
# main/magazine/about 은 프레임워크 형식 그대로 작성되어 있고,
# core/dongs/stations/themes/pages 모듈의 동대문 콘텐츠는 아래 변환기로
# 프레임워크 형식(섹션 래핑, faq-item, CTA, 브레드크럼)에 맞춘다.
import re

from .site import NAV, PHONE, PHONE_DISPLAY
from .pricing import PRICING
from . import main, magazine, about
from . import core as _core
from . import dongs as _dongs
from . import stations as _stations
from . import themes as _themes
from . import pages as _pages


def _faq_items(m):
    inner = m.group(1)
    pairs = re.findall(
        r"<dt>\s*Q\.\s*(.*?)\s*</dt>\s*<dd>\s*A\.\s*(.*?)\s*</dd>", inner, flags=re.S
    )
    return "".join(
        f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in pairs
    )


def _convert_body(body: str) -> tuple:
    """h1 분리, FAQ(dl)→faq-item, 연락처 라인→CTA 버튼, h2 단위 섹션 래핑."""
    m = re.search(r"<h1>(.*?)</h1>", body, flags=re.S)
    h1 = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    body = re.sub(r"<h1>.*?</h1>", "", body, flags=re.S)

    body = re.sub(r'<dl class="faq">(.*?)</dl>', _faq_items, body, flags=re.S)
    body = re.sub(
        r'<p class="contact-line">.*?</p>',
        f'<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>',
        body,
        flags=re.S,
    )

    parts = re.split(r"(?=<h2)", body)
    out = [parts[0]]
    for chunk in parts[1:]:
        idm = re.match(r'<h2 id="([^"]+)">', chunk)
        sid = f' id="{idm.group(1)}"' if idm else ""
        if idm:
            chunk = re.sub(r'<h2 id="[^"]+">', "<h2>", chunk, count=1)
        cls = ' class="cta"' if "cta-phone" in chunk else ""
        out.append(f"<section{sid}{cls}>\n{chunk.strip()}\n</section>\n")
    return h1, "".join(out)


def _breadcrumb_for(path: str):
    """NAV 구조에서 현재 경로의 브레드크럼을 만든다."""
    href = "/" + path
    for label, top_href, children in NAV:
        if top_href == href and top_href != "/":
            return [(label, None)]
        for c_label, c_href in children:
            if "#" in c_href:
                continue
            if c_href == href and c_href != top_href:
                return [(label, top_href), (c_label, None)]
    return []


def _adapt(page: dict, with_pricing: bool = False) -> dict:
    h1, body = _convert_body(page["body"])
    if with_pricing:
        body = body.replace('<section class="cta"', PRICING + '<section class="cta"', 1)
    out = {
        "path": page["path"],
        "title": page["title"],
        "desc": page.get("description") or page.get("desc", ""),
        "h1": h1,
        "body": body,
        "breadcrumb": _breadcrumb_for(page["path"]),
    }
    if page.get("noindex"):
        out["noindex"] = True
    if page.get("jsonld"):
        out["extra_head"] = page["jsonld"]
    return out


def _is_detail(path: str) -> bool:
    """대표 동·역 상세 페이지에만 공용 요금 블록을 붙인다."""
    return path.startswith("dongdaemun-gu/") and path not in (
        "dongdaemun-gu/",
        "dongdaemun-gu/stations/",
    )


_LEGACY = (
    [p for p in _core.PAGES if p["path"] != ""]  # 메인은 main.PAGE 가 담당
    + _dongs.PAGES
    + _stations.PAGES
    + _themes.PAGES
    + _pages.PAGES
)

PAGES = (
    [main.PAGE]
    + [_adapt(p, with_pricing=_is_detail(p["path"])) for p in _LEGACY]
    + magazine.PAGES
    + [about.PAGE]
)
