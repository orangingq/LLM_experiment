def input_provider(input_type: str):
    match input_type:
        case 'one':
            return type_one
        case 'two':
            return type_two
        case 'three':
            return type_three
        case 'four':
            return type_four
        case 'five':
            return type_five
        case 'nested':
            return nested
        case 'parallel':
            return parallel
        case 'dependent':
            return dependent
        case 'numbers':
            return numbers
        case '0': 
            return simple_sentence
        case '1':
            return complex_sentence
        case '2':
            return simple_paragraph
        case '3': 
            return get_articles(line=True, summary=True)[0] # return each line of the summarized articles
        case '4':
            return get_articles(line=False, summary=True)[0] # return each summary paragraph of articles
        case '5':
            return get_articles(line=False, summary=False)[0] # return a whole article
        case 'all':
            return simple_sentence + complex_sentence + simple_paragraph + get_articles(line=False, summary=True)[0]
        case _:
            raise ValueError("input_type")

type_one = [
    # 1형 (주어 + 서술어)
    "국내 외식업계가 위축되었다.",
    "플라스틱 사용 줄이기 캠페인이 확대되었다.",
    "환경 보호 운동이 활발히 일어나고 있다.", 
]

type_two = [
    # 2형 (주어 + 목적어 + 서술어)
    "한국 우주청은 달 탐사 로봇 '루나 2'를 성공적으로 발사하였습니다.",
    "유럽 연합은 인공지능 규제에 대한 법안을 추진하고 있습니다.",
    "올림픽 평화봉송단이 남북한 선수들의 공동 출전을 예고하였습니다.",
    "교육부는 국내 초중고등학교의 교육과정 개편을 검토 중에 있습니다.",
]

type_three = [
    # 3형 (주어 + 보어 + 되다/아니다)
    "나는 선생님이 아니다.", 
    "한국은 '반도체 1위'가 아니다.",
    "IAEA 최종 보고서는 일본의 해양범죄에 대한 면죄부가 아니다.",
    "지연된 정의는 정의가 아니다.",
    "구로공단 '공순이'는 21세기 '콜순이'가 되었다."
]

type_four = [
    # 4형 (주어 + 필수부사어 + 서술어)
    "미끄러운 빗길은 교통사고로 이어졌다.",
    "아프리카 국가들은 에볼라 바이러스 감염 확산에 대응하고 있습니다.",
    "여름 휴가지가 인기로 떠오르고 있습니다."
]

type_five = [
    # 5형 (주어 + 여격부사어 + 목적어 + 서술어)
    "희귀병 환자는 세상을 떠나고도 4명에게 생명을 주었다.",
    "엄마가 아기에게 이름을 붙여주었다.",
    "'50억 무죄' 판결은 이 당연한 의문에 답을 주지 못한다.",
]

nested = [
    # 겹문장
    "농구 국가대표팀이 월드컵 본선 진출에 성공했습니다.", 
    "번개장터는 우정사업본부와 중고 거래 플랫폼 최초 '우체국소포'를 정식 출시한다고 밝혔다.",
    "첫 월급을 받은 아들과 딸이 깜짝 선물을 주었다.",

]

parallel = [
    # 대등하게 이어지는 문장
    "물가 상승으로 가계부담이 늘어나고 있으며, 이로 인해 인플레이션 우려가 커지고 있습니다.",
    "테슬라는 자율주행 자동차 사고로 논란이 일어나고 있으며, 안전성에 대한 논의가 계속되고 있습니다.",
]

dependent = [
    # 종속적으로 이어지는 문장
    "정부는 기후변화 대응을 강화하기 위해 신재생에너지에 대한 투자를 확대하고 있습니다.",
    "세계보건기구(WHO)가 신병균 '루카'에 대한 글로벌 대응을 위해 협의하고 있습니다.",
    "미국과 중국은 무역갈등을 완화하기 위해 협상을 재개하려고 합니다.",
    "한국 청소년들의 스마트폰 중독이 증가하면서 대책 마련 필요성이 제기되고 있습니다."    
    # "정부가 코로나19 방역 대책 강화를 위해 예산 증액을 추진하고 있습니다.",
    "젊은 릴케는 스승이 아닌 동료였기에 멘토가 되었다.",
    "검사마저 울먹이자 법정은 울음바다가 되었다."
]

numbers = [
    "중소기업중앙회는 지난 13일부터 20일까지 3062개 중소기업을 대상으로 실시한 ‘2023년 8월 중소기업 경기전망조사’ 결과를 30일 밝혔다.", # https://www.m-i.kr/news/articleView.html?idxno=1035643
    "먼저 ‘어제 행복도’는 10점 만점 기준 2018년 5.72점에서 2022년 6.29점으로 상승했다.", # 출처 : 굿모닝충청(http://www.goodmorningcc.com)
    "제조업의 8월 경기전망은 전월대비 3.5p 하락한 80.6이며, 비제조업은 2.4p 상승한 79.3으로 나타났다."
]

simple_sentence = type_one + type_two + type_three + type_four + type_five

complex_sentence = nested + parallel + dependent + numbers

simple_paragraph = [
    "올해 장마는 평년보다 많은 비를 기록할 가능성이 높다는 게 전문가들 관측이다. 기상청은 장마철이 시작된 6월25일부터 현재까지 약 2주간 전국 대부분 지역에 200~300㎜, 전남 일부 지역은 600㎜ 안팎의 많은 누적 강수량을 기록했다고 밝혔다.",
    "온라인동영상서비스(OTT) 플랫폼 넷플릭스가 구독자 간 ‘무료 계정 공유’를 금지한 뒤 신규 구독자가 큰 폭으로 늘어났다. 19일(현지시간) 넷플릭스가 발표한 실적 보고서를 보면, 넷플릭스 가입자는 올해 2분기 전세계에서 589만명 증가해 총 2억3839만명이 됐다. 전체 가입자 수가 지난해 같은 기간보다 8.0% 늘었다. 2분기 매출액은 81억8700만달러(약 10조3700억원), 영업이익은 18억2700만달러(약 2조3100억원)로 지난해 동기 대비 각각 2.7%, 15.8% 늘었다.",

]


news_headlines = [
    "물가 상승으로 가계부담 늘어나…인플레이션 우려 커져",
    "정부, 기후변화 대응 강화 위해 신재생에너지 투자 확대",
    "세계보건기구(WHO), 신병균 '루카' 글로벌 대응 협의",
    "미국, 중국과의 무역갈등 완화 위해 협상 재개",
    "한국 우주청, 달 탐사 로봇 '루나 2' 성공 발사",
    "아프리카 국가들, 에볼라 바이러스 감염 확산에 대응",
    "유럽 연합, 인공지능 규제에 대한 법안 추진",
    "테슬라, 자율주행 자동차 사고로 논란…안전성 논의 끊이지 않아",
    "올림픽 평화봉송단, 남북한 선수 공동 출전 예고",
    "교육부, 국내 초중고등학교 교육과정 개편 검토 중"
]

import math

def get_articles(line=False, summary=True, start=0):
    import json
    
    articles = [] # inputs
    files = [
        'inputs/articles/articles_297to981.json',
        'inputs/articles/articles_982to2979.json',
        'inputs/articles/articles_2980to19991.json'
    ]
    i = 0 # iterator
    one_cycle = 25 # 33 articles per one cycle

    total_articles = 0
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_articles += len(data)

    end = min(start + one_cycle, total_articles)
        
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for article in data:
                if i < start:
                    i += 1
                    # print(article['text_rank'][:10])
                    continue
                elif i >= end:
                    break
                # if i > 1:break
                if line and i >= 1:
                    break
                if summary:
                    if line:
                        articles += article['text_rank']#article['summary']
                    else:
                        articles += [' '.join(article['text_rank'])]#article['summary'])]
                else:
                    if line:
                        articles += article['article'].rstrip('\n').split('\n')
                    else:
                        articles += [' '.join(article['article'])]

                # iterate
                i += 1
                
    isdone = (end >= total_articles)
    # print([a[:10] for a in articles])
    return articles, end, isdone

# get_articles()
