from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate
from inputs.Benchmark import input_provider

def prompt_maker(kg_type:str, prompt_type:str, example_type:str, input_type:str)->str:
    match kg_type:
        case 'RDF-star': # RDF-star format
            kg = '1'
        case 'LPG':     # LPG (Neo4j) format
            kg = '2'
        case 'Infoedge': # new format 'infoedge'
            kg = '3'
        case _:
            raise ValueError("kg_type")
        
    match prompt_type:
        case 'None':
            suffix = ""
        case 'Eng':
            import prompts
            suffix = prompts.import_module("prompt"+kg+"_eng").prompt
        case 'Kor':
            import prompts
            suffix = prompts.import_module("prompt"+kg+"_kor").prompt
        case _:
            raise ValueError("prompt_type")
        
    match example_type:
        case '0':
            examples = []
        case '1':
            import examples
            examples = examples.import_module("example"+kg).examples
        case _:
            raise ValueError("example_type")

        # case '10':
        #     suffix = ""
        # case '11':
        #     from prompts import prompt1_eng
        #     suffix = prompt1_eng.prompt
        # case '12':
        #     from prompts import prompt1_kor
        #     suffix = prompt1_kor.prompt
        # case '20':
        #     suffix = ""
        # case '21':
        #     from prompts import prompt2_eng
        #     suffix = prompt2_eng.prompt
        # case '22':
        #     from prompts import prompt2_kor
        #     suffix = prompt2_kor.prompt
        # case '30':
        #     suffix = ""
        # case '31':
        #     from prompts import prompt3_eng
        #     suffix = prompt3_eng.prompt
        # case '32':
        #     from prompts import prompt3_kor
        #     suffix = prompt3_kor.prompt
        # case _:
        #     raise ValueError("prompt_type")

    try:
        input_type = int(input_type)
    except ValueError:
        raise ValueError("input_type: only integer input type is allowed.")
    else:
        input = input_provider(input_type)
        # Benchmark.inputt[int(input_type)-1]

    example_prompt = PromptTemplate(input_variables=[
                                "sentence", "output"], template="Sentence: {sentence}\nOutput: {output}")
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix=suffix + "Sentence: {input}\nOutput: ",
        input_variables=["input"]
    )
    return prompt.format(input=input)