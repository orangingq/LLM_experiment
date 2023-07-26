import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from models.base_model import BaseLLM
from huggingface_hub import login
from keys.keys import huggingface_token

class LLAMA2(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        
    def set_model(self)->None:
        self.model_id = "meta-llama/Llama-2-13b-chat-hf"
        login(token = huggingface_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            low_cpu_mem_usage=True,
            use_auth_token=True
        ).to(device=self.device, non_blocking=True)
        self.model.eval()
        
        
    def set_tokenizer(self)->None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, use_auth_token=True)
        pass

    def run(self, prompt)->str:
        
        # encode
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        print(input_ids.shape)
        self.tokens = input_ids.shape[1]

        # inference
        start_time = time.time()
        output_ids = self.model.generate(input_ids, max_new_tokens=100)
                
        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)
        generated = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return generated


    
