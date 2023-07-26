#!/bin/bash

# python3 run.py \
#     --kg_type=RDF-star \
#     --prompt_type=None \
#     --example_type=1 \
#     --input_type=0 \
#     --model_type=KULLM;

for ((i=1; i<=5; i++))
do
    python3 run.py \
    # --kg_type=RDF-star \
    # --prompt_type=None \
    # --example_type=1 \
    # --input_type=0 \
    --model_type=LLAMA2;
done

# tmux attach -t orangingq
# ctrl+B -> D