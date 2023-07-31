import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from models.base_model import BaseLLM, output_parser
import time

# https://huggingface.co/kakaobrain/kogpt

class KoGPT(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = 'kakaobrain/kogpt'
        self.set_tokenizer()
        self.set_model()
        
        
    def set_model(self)->None:
        
        self.model = AutoModelForCausalLM.from_pretrained(
            # or float32 version: revision=KoGPT6B-ryan1.5b
            self.model_id, revision='KoGPT6B-ryan1.5b-float16',
            pad_token_id= self.tokenizer.eos_token_id,
            torch_dtype='auto', low_cpu_mem_usage=True
        ).to(device=self.device, non_blocking=True)
        self.model.eval()

    def set_tokenizer(self)->None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            # or float32 version: revision=KoGPT6B-ryan1.5b
            self.model_id, revision='KoGPT6B-ryan1.5b-float16',
            bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
        )


    def run(self, prompt)->str:
        with torch.no_grad():
            tokens = self.tokenizer.encode(prompt, return_tensors='pt').to(
                device=self.device, non_blocking=True)
            self.tokens = tokens.shape[1]
            
            # inference
            start_time = time.time()
            gen_tokens = self.model.generate(tokens, do_sample=True, temperature=0.8, max_new_tokens=100, early_stopping=True)
            
             # elapsed time
            self.calculate_elapsed_time(start_time=start_time)
            
            # decode
            generated = self.tokenizer.batch_decode(gen_tokens)[0][len(prompt):]
        
        return output_parser(generated)

