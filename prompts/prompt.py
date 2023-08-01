from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate
import importlib 
import csv

def kg_matcher(kg_type:str)->str:
    match kg_type:
        case 'RDF-star': # RDF-star format
            kg = '1'
        case 'LPG':     # LPG (Neo4j) format
            kg = '2'
        case 'LPG_tense':
            kg = '3'
        case 'LPG_id':
            kg = '4'
        case 'Infoedge': # new format 'infoedge'
            kg = '5'
        case _:
            raise ValueError("kg_type - got: ", kg_type)
    return kg


def prompt_matcher(prompt_type:str, kg:str)->str:
    match prompt_type:
        case 'None':
            suffix = ""
        case 'Eng':
            suffix = importlib.import_module("prompts.prompt"+kg+"_eng").prompt
        case 'Kor':
            suffix = importlib.import_module("prompts.prompt"+kg+"_kor").prompt
        case _:
            raise ValueError("prompt_type - got: ", prompt_type)
    return suffix

def example_matcher(example_type:str, kg:str):
    match example_type:
        case '0':
            examples = []
        case '1':
            filename = './examples/raw_examples.csv'
            f = open(filename, mode="r")
            csv_file = csv.reader(f, delimiter=",")
            examples = []
            for row in csv_file:
                if row[0] == 'Sentence':
                    continue
                if row[int(kg)] is None:
                    break
                
                examples += [{
                    "sentence": row[0],
                    "output": row[int(kg)]
                }]
                
                if len(examples) == 8: 
                    break
            f.close()
            
        case _:
            raise ValueError("example_type - got: ", example_type)
    return examples


def prompt_maker(kg_type:str, prompt_type:str, example_type:str, chat:bool=False)->str:
    kg = kg_matcher(kg_type)
    suffix = prompt_matcher(prompt_type, kg)
    examples = example_matcher(example_type, kg)
    
    if chat:
        # KG format explanation 
        prompt = [{"role": "system", "content": suffix}]
        
        # examples
        for example in examples:
            prompt += [
                {"role": "user", "content": "Sentence: " + example['sentence'] + "\nOutput: "},
                {"role": "assistant", "content": example['output']}
            ]
        
        # Sentence given to generate output
        prompt += [{"role": "user", "content": "Sentence: {input}\nOutput: "}]
    
    
    else:
        example_prompt = PromptTemplate(input_variables=[
                                "sentence", "output"], template="Sentence: {sentence}\nOutput: {output}")
        
        prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            suffix=suffix + "Sentence: {input}\nOutput: ",
            input_variables=["input"]
        )
        
    return prompt
    
    
    
