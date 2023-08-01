# RDF-star 형식에 대한 설명 prompt

prompt = """
주어진 입력 문장을 RDF-star 형식으로 변환하세요. 

거짓말을 해서는 안 됩니다. 실제 객체와 관계들만 변환해야 합니다.
다음은 RDF-star 형식에 대한 간단한 설명입니다. 인터넷에서 추가 정보를 찾을 수 있습니다. 

객체와 값이 있습니다.
객체는 ':객체'로 표시됩니다.
값은 문자열 유형, 숫자 또는 날짜가 될 수 있으며 '"값"'로 표시됩니다.

표현의 기본 단위는 triple입니다.
객체 간의 관계는 ' :객체1 :관계 :객체2 . '으로 표현합니다.
객체의 속성은 ' :객체 :속성 :객체 . ' 또는 ' :객체 :속성 "값" . '으로 표현합니다.

RDF-star 형식과 기본 RDF 형식의 주요 차이점은 'Quoted Triple'입니다. 
' << :객체 :속성 :값 >> :관계 :객체 . '와 같이, '<<'와 '>>' 사이에 triple을 묶어 triple을 단일 객체처럼 참조할 수 있습니다.

"""
