import time
from models.base_model import BaseLLM
from langchain.chat_models import ChatOpenAI
from keys.openai_key import key
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

class ChatOpenai(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.set_model()
        self.set_tokenizer()
        
    def set_model(self)->None:
        self.model_id = 'ChatOpenAI'
        self.model = ChatOpenAI(openai_api_key=key, temperature=0)

    def set_tokenizer(self)->None:
        pass


    def run(self, prompt)->str:
        if self.model is None:
            self.model = ChatOpenAI(openai_api_key=key, temperature=0)
            
        # inference
        start_time = time.time()
        messages = [SystemMessage(content="You are a smart assistant."),
                    HumanMessage(content=prompt)]
        output = self.model(messages=messages)

        # elapsed time
        self.calculate_elapsed_time(start_time=start_time)

        # decode
        generated = output.content
        print("\n** Output:\n", generated)
        return generated
