import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
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
        
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.model_id, device=self.device)


    def set_tokenizer(self)->None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        pass

    def run(self, prompt)->str:
        
        # encode
        input_ids = self.tokenizer.encode(prompt)
        self.tokens = len(input_ids)

        # inference
        start_time = time.time()
        output = self.pipeline(prompt, max_new_tokens=100, temperature=0, early_stopping=True) #, num_beams=5, eos_token_id=2
        
        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)
        
        generated = output[0]["generated_text"][len(prompt):]
        return generated


    
