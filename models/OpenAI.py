import time
from models.base_model import BaseLLM
from langchain.llms import OpenAI
from keys.openai_key import key

class Openai(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        
    def set_model(self)->None:
        self.model_id = 'OpenAI'
        self.model = OpenAI(openai_api_key=key, temperature=0)

    def set_tokenizer(self)->None:
        pass


    def run(self, prompt)->str:
        if self.model is None:
            self.model = OpenAI(openai_api_key=key, temperature=0)
            
        # inference
        start_time = time.time()
        generated = self.model(prompt)

        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)

        # decode
        print("\n** Output:\n", generated)
        return generated
