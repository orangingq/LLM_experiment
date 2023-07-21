def input_provider(input_type: str):
    match input_type:
        case '0': 
            return simple_sentence
        case '1':
            return complex_sentence
        case '2':
            return simple_paragraph
        case '3': 
            return complex_paragraph
        case 'all':
            return simple_sentence + complex_sentence + simple_paragraph + complex_paragraph
        case _:
            raise ValueError("input_type")

simple_sentence = [
    "학생 A와 학생 B가 만났다.",
    "미끄러운 빗길은 교통사고로 이어졌다.",
]

complex_sentence = [
    "번개장터는 우정사업본부와 중고 거래 플랫폼 최초 '우체국소포'를 정식 출시한다고 밝혔다.",
]

simple_paragraph = [
    "올해 장마는 평년보다 많은 비를 기록할 가능성이 높다는 게 전문가들 관측이다. 기상청은 장마철이 시작된 6월25일부터 현재까지 약 2주간 전국 대부분 지역에 200~300㎜, 전남 일부 지역은 600㎜ 안팎의 많은 누적 강수량을 기록했다고 밝혔다."

]

complex_paragraph = [
    "온라인동영상서비스(OTT) 플랫폼 넷플릭스가 구독자 간 ‘무료 계정 공유’를 금지한 뒤 신규 구독자가 큰 폭으로 늘어났다. 19일(현지시간) 넷플릭스가 발표한 실적 보고서를 보면, 넷플릭스 가입자는 올해 2분기 전세계에서 589만명 증가해 총 2억3839만명이 됐다. 전체 가입자 수가 지난해 같은 기간보다 8.0% 늘었다. 2분기 매출액은 81억8700만달러(약 10조3700억원), 영업이익은 18억2700만달러(약 2조3100억원)로 지난해 동기 대비 각각 2.7%, 15.8% 늘었다."

]