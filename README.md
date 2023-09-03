# 설치

#### github project 다운로드 받기

```bash
git clone https://github.com/orangingq/LLM_experiment.git
```

#### 환경설정하기

```bash
cd LLM_experiment
conda create -n llm_env -f conda_requirements.txt
conda activate llm_env
pip3 install -r requirements.txt
```

## 빠르게 돌리기

```bash
python3 run.py
```

위 코드를 실행할 경우, 가장 기본 option으로 설정되어 결과가 출력된다.

#### option 기본값

- `--kg=RDF-star`: Knowledge Graph는 RDF-star 형식으로 출력된다.
- `--prompt=Eng`: RDF-star 형식에 대한 영어 description이 입력된다.
- `--example=1`: 10쌍의 text input과 RDF-star 형식 output이 example로 LLM에 제공된다.
- `--input=4`: input으로는 'gensim' summarizer에 의해 한 문단 정도의 길이로 요약된 기사가 LLM에 제공된다.
- `--model=ChatLlama2`: ChatLlama2 model을 사용해 KG를 출력한다.

#### option 설정 변경

- `--kg={K}`: `{KG}`에는 `RDF-star`, `LPG_tense`, `all`를 쓸 수 있다. `LPG_tense`는 LPG 형식으로 출력하는 option이고, `all`은 두 가지 경우에 대해 모두 실험하는 방식이다.
- `--prompt={P}`: `{P}`에는 `None`, `Eng`,`Kor`, `all`을 쓸 수 있다. `None`은 KG 형식에 대한 description을 제공하지 않는 옵션이고, `Eng`과 `Kor`은 각각 영어와 한국어 버전의 설명을 제공하는 옵션이다.
- `--example={E}`: `{E}`에는 `0` 또는 `1`을 쓸 수 있다. 직관적으로 `0`은 zero-shot을, `1`은 few-shot을 의미한다.
- `--input={I}`: `{I}`에는 `0`부터 `5` 사이의 숫자를 쓸 수 있다. `0`은 간단한 문장들을 제공하고, `5`는 기사 전체를 요약 없이 제공한다. 숫자가 커질수록 복잡한 형태의 input을 제공한다.
- `--model={M}`: `{M}`에는 `ChatLlama2`, `Llama2`, `ChatOpenAI`, `OpenAI` 등을 쓸 수 있다.

이외의 추가 option들은 `run.py` 파일을 확인하라.

#### option 변경 예시

```bash
python3 run.py --kg=LPG_tense --example=1 --input=5 --model=Llama2
```

#### 결과 확인

`results/results/result_{YYYYMMdd_hh}.csv` 파일을 확인하라.
`YYYYMMdd_hh`는 실험을 돌린 '년월일\_시간'을 의미한다.

결과를 더 자세히 분석하기 위해서는 `results` directory의 README 파일을 참고하라.

# 구성 폴더

```python3
├── inputs      # KG로 변환할 input text를 구성하는 directory
│   ├── articles           # article dataset
│   └── article_clustering.py       # article dataset을 클러스터링
│   └── article_parser.py           # raw text file로부터 article dataset 생성
│   └── clova_summary.py            # article dataset의 각 article에 대한 요약본 생성
│   └── Benchmark.py       # LLM에 input으로 넣어줄 input text를 생성
│
├── prompts     # LLM에 넣어줄 prompt를 구성하는 directory
│   └── prompt.py
│   └── prompt1_eng.py     # English description of RDF-star format
│   └── ...
│
├── examples    # prompt에 넣어줄 example을 저장하는 directory
│   └── raw_examples.csv    # 각 출력 형식 별 example들을 저장
│
├── models      # LLM들을 관리하는 directory
│   ├── llama2
│   │   └── run_llama2.py  # Llama2 모델과 Llama2-Chat 모델을 실행
│   │   └── ...
│   └── base_model.py      # LLM model class의 abstract class 및 model loader 정의
│   └── ChatOpenAI.py      # ChatOpenAI model의 LLM model class 정의
│   └── ...
│
├── results     # LLM의 출력 결과 및 후처리된 결과를 저장/관리하는 directory
│   ├── results             # 1) LLM의 출력 결과를 저장
│   ├── scored              # 2) results 폴더의 결과의 채점 결과 저장
│   ├── queries             # 3) 채점된 결과를 Neo4j의 cypher query문으로 변환, 저장
│   ├── onlyqueries         # 4) query문을 통합하여 txt file로 저장
│   └── save.py             # LLM output  -> 1)
│   └── scoring.py          #    1)       -> 2)
│   └── neo4j.py            #    2)       -> 3)
│   └── queryonly.py        #    3)       -> 4)
│
├── keys        # OpenAI 보안키 등 암호를 보관하는 directory
│   └── keys_template.py    # 보안키들의 template 저장. 파일명을 'keys.py' 변경 필요.
│
└── run.py     # 전체 실험 pipeline을 한 번에 실행할 수 있는 파일
└── conda_requirements.txt    # conda library 환경 설치
└── requirements.txt          # pip3 library 환경 설치
```
