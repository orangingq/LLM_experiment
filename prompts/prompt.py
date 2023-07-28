from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate
import importlib 

def prompt_maker(kg_type:str, prompt_type:str, example_type:str)->str:
    match kg_type:
        case 'RDF-star': # RDF-star format
            kg = '1'
        case 'LPG':     # LPG (Neo4j) format
            kg = '2'
        case 'Infoedge': # new format 'infoedge'
            kg = '3'
        case _:
            raise ValueError("kg_type - got: ", kg_type)
        
    match prompt_type:
        case 'None':
            suffix = ""
        case 'Eng':
            suffix = importlib.import_module("prompts.prompt"+kg+"_eng").prompt
        case 'Kor':
            suffix = importlib.import_module("prompts.prompt"+kg+"_kor").prompt
        case _:
            raise ValueError("prompt_type - got: ", prompt_type)
        
    match example_type:
        case '0':
            examples = []
        case '1':
            import examples
            examples = importlib.import_module("examples.example"+kg).examples
        case _:
            raise ValueError("example_type - got: ", example_type)


    example_prompt = PromptTemplate(input_variables=[
                                "sentence", "output"], template="Sentence: {sentence}\nOutput: {output}")
        
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix=suffix + "Sentence: {input}\nOutput: ",
        input_variables=["input"]
    )
    
    return prompt