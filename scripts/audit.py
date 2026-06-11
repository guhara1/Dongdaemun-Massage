#!/usr/bin/env python3
"""사이트 품질 감사 스크립트.

검사 항목:
  1. 타이틀/디스크립션/H1 — 중복, 길이, 누락
  2. 페이지 간 본문 유사도(3-gram 자카드) — 복붙·도어웨이 위험 탐지
  3. 키워드 밀도 — 키워드 스터핑 탐지
  4. 내부 링크 무결성 — 깨진 링크·앵커
  5. JSON-LD 구문 검증
  6. 금지 패턴 — 지역+테마 조합 경로, 숫자 행정동 경로

usage: python3 scripts/audit.py
"""
import html
import itertools
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from content import PAGES  # noqa: E402

ISSUES = []


def issue(level, where, msg):
    ISSUES.append((level, where, msg))


def visible_text(body):
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body, flags=re.S)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def ngrams(text, n=3):
    toks = re.findall(r"[가-힣a-zA-Z0-9]+", text)
    return set(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    paths = {p["path"] for p in PAGES}

    # ── 1. 메타 검사 ────────────────────────────────────────────
    seen_titles, seen_descs, seen_h1 = {}, {}, {}
    for p in PAGES:
        path = p["path"] or "/"
        t, d, h = p["title"], p["desc"], p["h1"]
        if not t:
            issue("ERROR", path, "타이틀 없음")
        if not d:
            issue("ERROR", path, "디스크립션 없음")
        if not h:
            issue("ERROR", path, "H1 없음")
        if t in seen_titles:
            issue("ERROR", path, f"타이틀 중복: {seen_titles[t]}")
        if d in seen_descs:
            issue("ERROR", path, f"디스크립션 중복: {seen_descs[d]}")
        if h in seen_h1:
            issue("ERROR", path, f"H1 중복: {seen_h1[h]}")
        seen_titles[t], seen_descs[d], seen_h1[h] = path, path, path
        if len(t) > 40:
            issue("WARN", path, f"타이틀 길이 {len(t)}자 (SERP에서 잘릴 수 있음, 권장 ~35자)")
        if not 50 <= len(d) <= 160:
            issue("WARN", path, f"디스크립션 길이 {len(d)}자 (권장 50~160자)")

    # ── 2. 본문 유사도 (도어웨이·복붙 탐지) ─────────────────────
    grams = {}
    for p in PAGES:
        if p.get("noindex"):
            continue
        grams[p["path"] or "/"] = ngrams(visible_text(p["body"]))
    sims = []
    for (pa, ga), (pb, gb) in itertools.combinations(grams.items(), 2):
        s = jaccard(ga, gb)
        sims.append((s, pa, pb))
        if s >= 0.30:
            issue("ERROR", f"{pa} ↔ {pb}", f"본문 유사도 {s:.0%} — 도어웨이/복붙 위험")
        elif s >= 0.20:
            issue("WARN", f"{pa} ↔ {pb}", f"본문 유사도 {s:.0%} — 차별화 점검 권장")
    sims.sort(reverse=True)
    print("── 본문 유사도 상위 10쌍 (인덱스 페이지) ──")
    for s, a, b in sims[:10]:
        print(f"  {s:5.1%}  {a}  ↔  {b}")

    # ── 3. 키워드 밀도 ──────────────────────────────────────────
    print("\n── 키워드 밀도 상위 (출장마사지/홈타이/마사지) ──")
    dens = []
    for p in PAGES:
        if p.get("noindex"):
            continue
        text = visible_text(p["body"])
        words = max(1, len(re.findall(r"[가-힣a-zA-Z0-9]+", text)))
        kw = len(re.findall(r"출장마사지|홈타이|마사지", text))
        dens.append((kw / words, kw, p["path"] or "/"))
    dens.sort(reverse=True)
    for r, k, path in dens[:8]:
        print(f"  {r:5.1%} ({k}회)  {path}")
        if r > 0.05:
            issue("WARN", path, f"키워드 밀도 {r:.1%} ({k}회) — 스터핑 위험")

    # ── 4. 내부 링크 무결성 ─────────────────────────────────────
    anchors = {}
    for p in PAGES:
        ids = set(re.findall(r'id="([^"]+)"', p["body"]))
        # build.py 의 inject_toc 가 부여하는 sec-N 도 허용
        anchors[p["path"]] = ids
    for p in PAGES:
        for href in re.findall(r'href="(/[^"]*)"', p["body"]):
            if href.startswith(("/assets/", "/favicon")):
                continue
            base, _, frag = href.partition("#")
            base = base.lstrip("/")
            if base and base not in paths:
                issue("ERROR", p["path"] or "/", f"깨진 내부 링크: {href}")
            elif frag and base in anchors and frag not in anchors[base] and not frag.startswith("sec-"):
                issue("WARN", p["path"] or "/", f"존재하지 않는 앵커: {href}")

    # ── 5. JSON-LD 구문 검증 ────────────────────────────────────
    for p in PAGES:
        head = p.get("extra_head", "")
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, flags=re.S):
            try:
                json.loads(m.group(1))
            except json.JSONDecodeError as e:
                issue("ERROR", p["path"] or "/", f"JSON-LD 구문 오류: {e}")

    # ── 6. 금지 패턴 ────────────────────────────────────────────
    for p in PAGES:
        path = p["path"]
        if re.search(r"-\d-dong/", path):
            issue("ERROR", path, "숫자 행정동 경로 — 생성 금지 대상")
        if re.search(r"(stations|dong)/.*(swedish|thai|aroma|24)", path):
            issue("ERROR", path, "지역/역+테마 조합 경로 — 도어웨이 금지 대상")

    # ── 결과 ────────────────────────────────────────────────────
    print(f"\n── 발견된 이슈 ({len(ISSUES)}건) ──")
    for level, where, msg in sorted(ISSUES):
        print(f"  [{level}] {where}: {msg}")
    errors = sum(1 for l, _, _ in ISSUES if l == "ERROR")
    print(f"\n총 {len(PAGES)}페이지 검사 — ERROR {errors}건, WARN {len(ISSUES) - errors}건")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
