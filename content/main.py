# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "logo": "{BASE_URL}/assets/icon-512.png",
  "description": "동대문구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 동대문구"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "동대문구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 신설동, 용두동, 청량리동, 장안동, 이문동 등 대표 동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "청량리역이나 신설동역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "전농1동과 전농2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "전농1동과 전농2동은 전농동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "테마별 관리는 어디에서 확인하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 특징과 추천 대상을 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 동대문구 전지역</p>
    <h1>동대문 출장마사지·홈타이<br>예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>자택·오피스텔·숙소 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>10개</strong><span>대표 지역</span></li>
      <li><strong>9개</strong><span>역세권 안내</span></li>
      <li><strong>14개</strong><span>관리 테마</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>동대문 출장마사지·홈타이 서비스 안내</h2>
<p>동대문구에서 방문 마사지와 홈타이 예약을 찾는 이용자를 위해 가능 지역, 예약 절차, 코스 선택 기준, 이용 전 확인사항을 한곳에 정리했습니다. 이 메인페이지는 동대문구 전체 구조를 설명하는 허브 역할을 하며, 동별 생활권 정보나 역세권 정보, 관리 유형별 특징 같은 상세 내용은 지역별·지하철역별·테마별 안내 페이지에서 각각 확인할 수 있도록 구성했습니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 어렵지 않게 예약할 수 있도록 각 단계를 명확하게 안내해 드립니다.</p>
</section>

<section id="coverage">
<h2>동대문구 전지역 방문 가능 안내</h2>
<p>동대문구는 신설동, 용두동, 제기동, 전농동, 답십리동, 장안동, 청량리동, 회기동, 휘경동, 이문동을 중심으로 지역 안내를 구성합니다. 전농1동·전농2동처럼 숫자로 나뉜 행정동은 별도 페이지를 만들지 않고 대표 동 페이지에서 통합 안내하여 중복 정보를 줄였습니다. 아파트, 오피스텔, 빌라, 호텔, 모텔, 레지던스 등 조용한 공간이 확보되는 곳이라면 주거 형태와 관계없이 방문이 가능하며, 정확한 가능 여부는 예약 시점의 위치와 배정 상황에 따라 안내해 드립니다. 동대문구 경계와 가까운 인접 지역도 상담을 통해 확인할 수 있습니다.</p>
</section>

<section id="areas">
<h2>지역별 안내</h2>
<p>지역별 안내는 동대문구 대표 동 기준으로 구성됩니다. 각 페이지에서는 해당 생활권의 특징, 주변 역세권, 방문 전 확인사항, 예약 가능 시간, 관련 테마를 고유하게 설명합니다. 거주하시는 동을 선택하면 해당 지역에 맞는 안내를 확인할 수 있습니다.</p>
<ul class="card-grid">
<li><a href="/dongdaemun-gu/sinseol-dong/">신설동</a></li>
<li><a href="/dongdaemun-gu/yongdu-dong/">용두동</a></li>
<li><a href="/dongdaemun-gu/jegi-dong/">제기동</a></li>
<li><a href="/dongdaemun-gu/jeonnong-dong/">전농동</a></li>
<li><a href="/dongdaemun-gu/dapsimni-dong/">답십리동</a></li>
<li><a href="/dongdaemun-gu/jangan-dong/">장안동</a></li>
<li><a href="/dongdaemun-gu/cheongnyangni-dong/">청량리동</a></li>
<li><a href="/dongdaemun-gu/hoegi-dong/">회기동</a></li>
<li><a href="/dongdaemun-gu/hwigyeong-dong/">휘경동</a></li>
<li><a href="/dongdaemun-gu/imun-dong/">이문동</a></li>
</ul>
<p>동대문구 전체 구조가 궁금하시면 <a href="/dongdaemun-gu/">동대문구 전체 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>지하철역 인근 안내</h2>
<p>지하철역별 안내는 동대문구를 지나는 1호선·2호선 지선·5호선·경의중앙선·경춘선·수인분당선·우이신설선 주요 역세권을 기준으로 구성합니다. 각 역 페이지에서는 인근 생활권, 주변 대표 동, 예약 가능 시간, 방문 전 준비사항을 설명하며, 출구별 페이지나 역과 테마를 조합한 페이지는 만들지 않습니다. 환승역은 노선이 여러 개라도 페이지는 하나로 운영합니다.</p>
<ul class="card-grid">
<li><a href="/dongdaemun-gu/stations/sinseol-dong-station/">신설동역</a></li>
<li><a href="/dongdaemun-gu/stations/yongdu-station/">용두역</a></li>
<li><a href="/dongdaemun-gu/stations/jegi-dong-station/">제기동역</a></li>
<li><a href="/dongdaemun-gu/stations/cheongnyangni-station/">청량리역</a></li>
<li><a href="/dongdaemun-gu/stations/hoegi-station/">회기역</a></li>
<li><a href="/dongdaemun-gu/stations/hankuk-univ-foreign-studies-station/">외대앞역</a></li>
<li><a href="/dongdaemun-gu/stations/sinimun-station/">신이문역</a></li>
<li><a href="/dongdaemun-gu/stations/dapsimni-station/">답십리역</a></li>
<li><a href="/dongdaemun-gu/stations/janghanpyeong-station/">장한평역</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>테마별 안내에서는 관리 유형별 특징, 추천 대상, 예약 전 확인사항을 설명합니다. 테마는 각각 독립 페이지로 운영하며, 지역 페이지와 역 페이지에서는 관련 테마로 연결만 해 드립니다. 특정 역이나 동과 테마를 조합한 페이지는 운영하지 않으니, 원하시는 관리 유형을 먼저 고른 뒤 예약 시 위치를 알려주시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomi-lomi/">로미로미</a></li>
<li><a href="/themes/thai-massage/">타이마사지</a></li>
<li><a href="/themes/chinese-massage/">중국마사지</a></li>
<li><a href="/themes/aromatherapy/">아로마테라피</a></li>
<li><a href="/themes/home-care/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot-massage/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skin-care/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24-hours/">24시간</a></li>
<li><a href="/themes/sleep-friendly/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 이용 목적과 그날의 컨디션에 따라 선택하시는 것이 좋습니다. 누적된 피로를 풀고 싶은 분, 편안한 휴식이 필요한 분, 운동 후 근육 이완이 필요한 분, 숙소로 방문을 원하시는 분, 커플이 함께 받고 싶은 분 등 상황에 맞는 선택 기준을 <a href="/courses/">코스안내</a> 페이지에서 자세히 다룹니다. 고민되시면 예약 전화에서 상태를 말씀해 주세요. 함께 정해 드립니다.</p>
</section>

<section id="how">
<h2>예약 진행 방식</h2>
<p>예약은 다섯 단계로 진행됩니다. 먼저 희망 지역 또는 역 인근 위치를 확인하고, 희망 시간을 확인한 뒤, 코스와 인원을 정하고, 방문 가능 여부를 안내받은 다음, 예약을 확정합니다. 저녁 시간대나 주말에는 문의가 몰릴 수 있으므로 한두 시간 이상 여유를 두고 예약하시기를 권장합니다. 자세한 절차는 <a href="/reservation/">예약안내</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="check">
<h2>이용 전 확인사항</h2>
<p>원활한 방문 관리를 위해 정확한 주소, 공동현관 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 확인해 주시면 좋습니다. 숙소나 오피스텔로 방문을 요청하실 때는 건물 출입 안내와 예약 시간대 연락 가능 여부를 함께 알려주세요. 준비사항 전체는 <a href="/guide/">이용가이드</a>에 정리되어 있습니다.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>건전하고 안전한 방문 관리를 위해 위생 기준, 예약 정보 확인, 개인정보 보호, 금지행위 안내를 명확히 제공합니다. 모든 관리 도구와 용품은 위생 기준에 따라 관리되며, 예약 시 수집된 개인정보는 예약 확인과 방문 목적 외에는 사용하지 않습니다. 이용 전 서비스 범위와 유의사항을 확인해 주시고, 불법적이거나 무리한 요청은 어떤 경우에도 진행하지 않는다는 기준을 분명히 안내드립니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>동대문구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 신설동, 용두동, 청량리동, 장안동, 이문동 등 대표 동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>청량리역이나 신설동역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>전농1동과 전농2동은 왜 따로 없나요?</h3>
<p>전농1동과 전농2동은 전농동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다. 답십리동, 장안동, 휘경동, 이문동도 같은 기준으로 통합 운영합니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다. 정확한 대기 시간은 전화로 확인해 주세요.</p>
</div>
<div class="faq-item">
<h3>테마별 관리는 어디에서 확인하나요?</h3>
<p>스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 각 관리의 특징과 추천 대상을 확인할 수 있습니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>동대문구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "동대문 출장마사지·홈타이 | 동대문구 전지역 방문 마사지 예약 안내",
    "desc": "동대문 출장마사지·홈타이 안내 페이지입니다. 신설동, 용두동, 청량리동, 장안동, 이문동과 동대문구 주요 지하철역 인근, 테마별 관리, 예약 전 확인사항을 확인해보세요.",
    "h1": "동대문 출장마사지·홈타이 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
