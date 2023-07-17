#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://huggingface.co/beomi/KoAlpaca-Polyglot-5.8B

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
from models.base_model import BaseLLM

class KoAlpaca_5(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        
    def set_model(self)->None:
        self.model_id = 'beomi/KoAlpaca-Polyglot-5.8B'
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(device=self.device, non_blocking=True)
        self.model.eval()
        # print("** set_model finished!!")

    def set_tokenizer(self)->None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        # print("** set_tokenizer finished!!")


    def run(self, prompt)->str:
        # encode
        input_ids = self.tokenizer.encode(
            prompt, return_tensors='pt').to(self.device)

        self.tokens = input_ids.shape[1]
        print("\n** Tokens: ", input_ids.shape, input_ids[0, :10], "\n")

        # inference
        start_time = time.time()
        output_ids = self.model.generate(input_ids,
                                         max_length=1500,
                                         repetition_penalty=2.0,
                                         pad_token_id=self.tokenizer.pad_token_id,
                                         eos_token_id=self.tokenizer.eos_token_id,
                                         bos_token_id=self.tokenizer.bos_token_id,
                                         use_cache=True)

        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)

        # decode
        generated = self.tokenizer.decode(output_ids[0][:-1])[len(prompt):]
        print("\n** Output:\n", generated)
        return generated


    

        