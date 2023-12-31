from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate
import importlib 
import csv

# kg_type을 통해 kg의 번호값을 내보낸다. 
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
        case 'LPG_sem':
            kg = '5'
        case 'Infoedge': # new format 'infoedge'
            kg = '6'
        case 'LPG_rea':
            kg = '7'
        case _:
            raise ValueError("kg_type - got: ", kg_type)
    return kg


# prompt_type과 kg 번호를 받아, 적절한 prompt template을 return
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

# example_type과 kg 번호를 받아, 해당 kg type에 해당하는 example을 return 
def example_matcher(example_type:str, kg:str):
    match example_type:
        case '0':
            examples = []
        case '1':
            filename = './examples/raw_examples.csv'
            f = open(filename, mode="r")
            csv_file = csv.reader(f, delimiter=",")
            examples = []
            for i, row in enumerate(csv_file):
                if row[0] == 'Sentence':
                    continue
                if len(row[int(kg)]) == 0:
                    break
                if i < 3: continue
                if int(kg) >= 5 and i < 12:
                    continue
                examples += [{
                    "article": row[0],
                    "output": row[int(kg)]
                }]
                if len(examples) == 10: 
                    break
            f.close()
            
        case _:
            raise ValueError("example_type - got: ", example_type)
    
    return examples

# kg_type, prompt_type, example_type을 받아, prompt template과 example을 선택한 뒤 적절히 조합해 최종 prompt를 생성한다. 
def prompt_maker(kg_type:str, prompt_type:str, example_type:str, chat:bool=False)->str:
    kg = kg_matcher(kg_type)
    suffix = prompt_matcher(prompt_type, kg)
    examples = example_matcher(example_type, kg)
    
    if chat:
        # KG format explanation 
        prompt = [{"role": "system", "content": suffix.format()}]
        
        # examples
        for example in examples:
            prompt += [
                {"role": "user", "content": "Article: \n" + example['article'] + "\n\nOutput: \n"},
                {"role": "assistant", "content": example['output']}
            ]
        
        # Sentence given to generate output
        prompt += [{"role": "user", "content": "\n\nArticle: \n{input}\nOutput: \n"}]
    
    
    else:
        example_prompt = PromptTemplate(input_variables=[
                                "article", "output"], template="Article: \n{article}\n\nOutput: \n{output}\n")
        
        prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            suffix=suffix + "\n\nArticle: \n{input}\nOutput: \n",
            input_variables=["input"]
        )
                
    return prompt
    
    
    
