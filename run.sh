#!/bin/bash

# kg_range = ['LPG', 'LPG_tense', 'LPG_sem', 'LPG_rea', 'all'] # "RDF-star": RDF-star format / "LPG": LPG(Neo4j) format / "Infoedge": Infoedge format (new) # Reject: 'RDF-star', 'Infoedge', 'LPG_id', 
# prompt_range = ['None', "Eng", "Kor", 'all'] # "None": No Explanation template / "Eng": English Template / "Kor":Korean Template
# example_range = ['0', '1',  'all'] # 0: No example / 1: 4 examples / 2: 100 examples # '2',
# input_range = ['one', 'two', 'three', 'four', 'five', 'nested', 'parallel', 'dependent', '0', '1', '2', '3', '4', 'all'] # 0: simple sentences / 1: complex sentences / 2: simple paragraphs / 3: complex paragraphs 
# model_range = ['ChatLlama2', 'Llama2', 'all'] # Reject: 'KoAlpaca12.8','KoGPT2', 'KoAlpaca5.8', 'KoGPT', 'KULLM', 'ChatOpenAI', 'OpenAI', 


python3 run.py --kg=LPG --input=4 --model=ChatLlama2;
python3 run.py --kg=LPG --input=all --model=ChatLlama2;
python3 run.py --kg=LPG_tense --input=4 --model=ChatLlama2;
python3 run.py --kg=LPG_tense --input=all --model=ChatLlama2;
python3 run.py --kg=LPG_sem --input=4 --model=ChatLlama2;
python3 run.py --kg=LPG_sem --input=all --model=ChatLlama2;
python3 run.py --kg=LPG_rea --input=4 --model=ChatLlama2;
python3 run.py --kg=LPG_rea --input=all --model=ChatLlama2;
python3 run.py --kg=LPG --input=4 --model=Llama2;
python3 run.py --kg=LPG --input=all --model=Llama2;
python3 run.py --kg=LPG_tense --input=4 --model=Llama2;
python3 run.py --kg=LPG_tense --input=all --model=Llama2;
python3 run.py --kg=LPG_sem --input=4 --model=Llama2;
python3 run.py --kg=LPG_sem --input=all --model=Llama2;
python3 run.py --kg=LPG_rea --input=4 --model=Llama2;
python3 run.py --kg=LPG_rea --input=all --model=Llama2;


# python3 run.py \
#     --kg_type=RDF-star \
#     --prompt_type=None \
#     --example_type=1 \
#     --input_type=0 \
#     --model_type=KULLM;

# for ((i=1; i<=5; i++))
# do
#     python3 run.py \
#     # --kg_type=RDF-star \
#     # --prompt_type=None \
#     # --example_type=1 \
#     # --input_type=0 \
#     --model_type=LLAMA2;
# done

# tmux attach -t orangingq
# ctrl+B -> D
