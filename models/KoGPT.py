import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from models.base_model import BaseLLM
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
        # encode
        # input_ids = self.tokenizer.encode(
        #     prompt, return_tensors='pt').to(self.device)

        # self.tokens = input_ids.shape[1]
        # print("\n** Tokens: ", input_ids.shape, input_ids[0, :10], "\n")

        
        
        with torch.no_grad():
            tokens = self.tokenizer.encode(prompt, return_tensors='pt').to(
                device=self.device, non_blocking=True)
            self.tokens = tokens.shape[1]
            
            # inference
            start_time = time.time()
            gen_tokens = self.model.generate(
                tokens, do_sample=False, temperature=0, max_length=1500, num_return_sequences=1)
            
             # elapsed time
            self.calculate_elapsed_time(start_time=start_time)
            print(self.tokenizer.batch_decode(gen_tokens))
            generated = self.tokenizer.batch_decode(gen_tokens)[0][len(prompt):]
            

        # decode
        print("\n** Output:\n", generated)
        return generated




# class KoGPT(BaseLLM):
#     def __init__(self) -> None:
#         super().__init__()
        
#     def set_model(self):
#         self.model_id = 'kakaobrain/kogpt'
#         self.model = AutoModelForCausalLM.from_pretrained(
#             # or float32 version: revision=KoGPT6B-ryan1.5b
#             self.model_id, revision='KoGPT6B-ryan1.5b-float16',
#             pad_token_id=tokenizer.eos_token_id,
#             torch_dtype='auto', low_cpu_mem_usage=True
#         ).to(device=self.device, non_blocking=True)
#         self.model.eval()

#     def set_tokenizer(self):
#         self.tokenizer = AutoTokenizer.from_pretrained(
#             # or float32 version: revision=KoGPT6B-ryan1.5b
#             self.model_id, revision='KoGPT6B-ryan1.5b-float16',
#             bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
#         )

#     def run(self, prompt)->str:
        
#         with torch.no_grad():
#             tokens = self.tokenizer.encode(template.prompt(), return_tensors='pt').to(
#                 device=self.device, non_blocking=True)
#             gen_tokens = self.model.generate(
#                 tokens, do_sample=True, temperature=0.8, max_length=1500)
#             generated = self.tokenizer.batch_decode(gen_tokens)[0]

#         # elapsed time
#         self.elapsed_time(start_time=start_time)

#         # decode
#         generated = self.tokenizer.decode(output_ids[0][:-1])
#         return generated
#         print(generated)
        
        
        
#         # encode
#         input_ids = self.tokenizer.encode(
#             prompt, return_tensors='pt').to(self.device)
#         self.tokens = input_ids.shape[1]

#         # inference
#         start_time = time.time()
#         output_ids = self.model.generate(input_ids,
#                                          max_length=1500,
#                                          repetition_penalty=2.0,
#                                          pad_token_id=self.tokenizer.pad_token_id,
#                                          eos_token_id=self.tokenizer.eos_token_id,
#                                          bos_token_id=self.tokenizer.bos_token_id,
#                                          use_cache=True)

#         # elapsed time
#         self.elapsed_time(start_time=start_time)

#         # decode
#         generated = self.tokenizer.decode(output_ids[0][:-1])
#         return generated