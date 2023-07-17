from abc import ABC, abstractmethod
import time
import torch
# from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun


class BaseLLM(ABC):
    def __init__(self) -> None:
        self.elapsed_time = None
        if torch.cuda.is_available():
            self.device = "cuda:0"
        else:
            AssertionError("You need cuda.")
        self.model_id = ""
        self.tokens = -1
        self.model = None
        self.tokenizer = None

    @abstractmethod
    def set_model(self)->None:
        pass

    @abstractmethod
    def set_tokenizer(self)->None:
        pass

    @abstractmethod
    def run(self, prompt)->str:
        pass

    def calculate_elapsed_time(self, start_time)->None:
        hours, rem = divmod(time.time() - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        self.elapsed_time = "{:0>2}:{:0>2}:{:05.2f}".format(
            int(hours), int(minutes), seconds)
        
    @property
    def _llm_type(self) -> str:
        return self.model_id

    def __call__(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        if self.tokenizer is None or self.model is None:
            self.model = self.set_model()
            self.tokenizer = self.set_tokenizer()
        return self.run(prompt=prompt)
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model_id, "elapsed time": self.elapsed_time, "tokens": self.tokens, "device": self.device}