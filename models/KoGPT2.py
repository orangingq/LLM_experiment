import time
from transformers import TFGPT2LMHeadModel
# import os
# import tensorflow as tf
from transformers import PreTrainedTokenizerFast
from models.base_model import BaseLLM

# os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# tf.config.list_physical_devices('GPU')
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# https://github.com/SKT-AI/KoGPT2


# def KoGPT2(input):
#     model_id = 'skt/kogpt2-base-v2'
#     print("\n** Model: ", model_id)
#     print("\n** Input: \n...\n", input[-200:])

#     tokenizer = PreTrainedTokenizerFast.from_pretrained(model_id,
#                                                         bos_token='</s>', eos_token='</s>', unk_token='<unk>',
#                                                         pad_token='<pad>', mask_token='<mask>')
#     model = TFGPT2LMHeadModel.from_pretrained(model_id, from_pt=True)

#     # encode
#     input_ids = tokenizer.encode(input, return_tensors='pt')
#     print("\n** Tokens: ", input_ids.shape, input_ids[0, :10], "\n")

#     # inference
#     start_time = time.time()
#     output_ids = model.generate(input_ids,
#                                 max_length=1500,
#                                 repetition_penalty=2.0,
#                                 pad_token_id=tokenizer.pad_token_id,
#                                 eos_token_id=tokenizer.eos_token_id,
#                                 bos_token_id=tokenizer.bos_token_id,
#                                 use_cache=True)
#     print(
#         f"** Elapsed Time: {time.time()-start_time} seconds", "\n")

#     # decode
#     generated = tokenizer.decode(output_ids[0])
#     print("Output:\n", generated)


class KoGPT2(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        self.device='cpu'
        
    def set_model(self)->None:
        self.model_id = 'skt/kogpt2-base-v2'
        self.model = TFGPT2LMHeadModel.from_pretrained(self.model_id, from_pt=True)

    def set_tokenizer(self)->None:
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.model_id,
                                                        bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                        pad_token='<pad>', mask_token='<mask>')


    def run(self, prompt)->str:
        # encode
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt').to(device=self.device)

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
        generated = self.tokenizer.decode(output_ids[0])[len(prompt):]
        print("\n** Output:\n", generated)
        return generated


    
