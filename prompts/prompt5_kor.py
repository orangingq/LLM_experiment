# Infoedge 형식에 대한 설명 prompt

prompt = """
위에 주어진 문장에 대해 하나의 Relationship을 추론하세요. 
절대 거짓말을 해서는 안 됩니다. Relationship을 최대한 정확하게 추론하세요.
Relationship에는 세 가지 유형이 있습니다. Node, Edge 및 Infoedge입니다. 

1. Node
모든 Node에는 고유한 id와 label이 있습니다. 
Node의 형식은 (id-label)입니다.
Node의 label은 문장의 주어입니다.

2. Edge
모든 Edge에는 'from' node의 id와 'to' node의 id, edge의 id, 그리고 label이 있습니다.
Edge의 형식은 (id-label): node id->node id입니다.
모든 Edge는 Node 집합에서 다른 Node 집합으로 방향성을 가지고 연결됩니다. 
Edge의 label은 문장의 동사의 기본형입니다. label은 항상 정확하고 짧아야 합니다. 

3. Infoedge
Infoedge는 시간, 위치, 기간, 누구로부터 등 문장의 추가 정보를 엣지에 추가합니다. 
모든 Infoedge에는 하나의 기본 Edge id, 정보성 Node id, 그리고 infoedge 자체의 id 및 label이 있습니다. 
Infoedge의 형식은 (id-label): Edge id->Node id입니다.
Infoedge의 label은 '부터 (시간)', '까지 (시간)', '에서 (장소)', '에 (시간)', '에게', '에게서' 중 하나여야 합니다.

"""
