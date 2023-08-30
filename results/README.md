# results 상위 폴더 설명서

## Overview

먼저, LLM의 출력 결과는 results 폴더 내에 저장된다. 파일 이름은 result_YYYYmmdd_hh.csv 형식이다.

그 다음 results 결과를 채점하기 위해 scoring.py의 scoring 함수를 거친다.
채점된 결과는 scored 폴더 내에 저장된다. 파일 이름은 scored_YYYYmmdd_hh.csv 형식이다.

채점되어 통과한 결과는 Neo4j DB에 넣기 위해 Neo4j cypher query 형식으로 변형된다.
그 cypher query는 queries 폴더 내에 저장되고, 파일 이름은 query_YYYYmmdd_hh.csv 이다.

많은 query문을 한번에 Neo4j DB에 넣기 위해, 마지막으로 전체 query를 통합해 txt file로 변환한다.
file은 onlyqueries 폴더 내에 저장되고, 파일 이름은 RDF_Llama2_gensim_YYYYmmdd_hh.csv 이다. (gensim summarizer 사용, Llama2 모델 사용, RDF format으로 출력했다는 뜻. 파일 이름 변경은 queryonly.py에서 가능하다.)
이 txt file을 전체 복사해 neo4j DB에 넣어주면 node와 edge들이 생성된다.

## 1. 결과 저장

### LLM output -> result_YYYYmmdd_hh.csv

result_YYYYmmdd_hh.csv 파일은 save.py에서 생성한다.
각 row는 kg,prompt,example,input,model,elapsed time,tokens,input_idx,input,output 결과가 나열되어 있다.
kg~model은 run.py를 돌릴 때 넣어주었던 실험 변수를 저장한다.
elapsed time: 모델을 한번 돌릴 때 (inference 시간 기준) 걸린 시간
tokens: token 수 (측정 안됐을 경우는 기본값 -1)
input_idx: input text의 번호
input: input text
output: raw output of LLM

## 2. 채점

### result_YYYYmmdd_hh.csv -> scored_YYYYmmdd_hh.csv

scored_YYYYmmdd_hh.csv 파일은 scoring.py에서 생성한다.
scoring.py에서는 result\_~~.csv 파일의 output을 정규표현식을 이용해 채점하고, 문법에 맞게 조금 다듬는다.
만약 다듬은 결과가 문법에 부합한다면 채점 결과를 1로, 문법에 부합하지 않는다면 0으로 반영한다.

scored\_.csv의 각 row는 kg,prompt,example,model,input_idx,input,output,structure_score,note로 이루어져 있다.
kg~model은 run.py를 돌릴 때 넣어주었던 실험 변수를 저장한다.
input_idx: input text의 번호
input: input text
output: 채점 후 다듬어진 output
structure_score: 문법 통과라면 1, 아니면 0
note: 만약 문법 통과를 못했다면 output의 줄에서 통과를 못했는지 보여준다.

## 3. cypher 문법화

### scored_YYYYmmdd_hh.csv -> query_YYYYmmdd_hh.csv

query_YYYYmmdd_hh.csv 파일은 neo4j.py에서 생성한다.
neo4j.py에서는 채점을 통과한 결과들을 cypher 문법에 맞게 수정한다. (CREATE를 붙이거나 triple을 LPG 형식으로 변환.)

## 4. query text file

### scored_YYYYmmdd_hh.csv -> RDF_Llama2_gensim_YYYYmmdd_hh.txt

이 기능은 triple format의 경우에만 지원한다. LPG 형식도 되기는 하지만 변수가 통일되지 않아서 코드 수정이 필요하다.

3번까지는 run.py를 돌릴 때 자동적으로 다 실행되지만, 4번은 queryonly.py의 마지막 줄에 filename을 직접 입력한 다음에 돌려야 (python3 results/queryonly.py) 한다.

txt 파일의 이름은 RDF_Llama2_gensim_YYYYmmdd_hh.txt인데, 이는 gensim summarizer 사용, Llama2 모델 사용, RDF format으로 출력했다는 뜻이다.
LLM 실험 결과 최종적으로 Llama2 모델 (또는 ChatLlama2)과 RDF format을 사용하기로 결정했기 때문에 이름을 그렇게 지었다.
파일 이름 변경은 queryonly.py에서 가능하다.

이 txt file을 전체 복사해 neo4j DB에 넣어주면 node와 edge들이 생성된다.
