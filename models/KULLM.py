import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from models.base_model import BaseLLM
import torch

class KULLM(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        
    def set_model(self)->None:
        self.model_id = 'nlpai-lab/kullm-polyglot-12.8b-v2'
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(device=self.device, non_blocking=True)
        self.model.eval()

    def set_tokenizer(self)->None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)


    def run(self, prompt)->str:
        
        # encode
        input_ids = self.tokenizer.encode(prompt)

        self.tokens = input_ids.shape[1]
        print("\n** Tokens: ", input_ids.shape, input_ids[0, :10], "\n")

        # inference
        start_time = time.time()
        output_ids = self.model.generate(input_ids,
                                        #  max_length=1500,
                                        temperature = 0,
                                        #  repetition_penalty=2.0,
                                        #  pad_token_id=self.tokenizer.pad_token_id,
                                        #  eos_token_id=self.tokenizer.eos_token_id,
                                        #  bos_token_id=self.tokenizer.bos_token_id,
                                         max_new_tokens=100, early_stopping=True,
                                         use_cache=True)

        print(output_ids)
        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)

        # decode
        generated = self.tokenizer.decode(output_ids[0])[len(prompt):]
        return generated


    
