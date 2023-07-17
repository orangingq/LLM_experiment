import inputs.Benchmark as Benchmark
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate
import click
import json

def prompt(example_type, prompt_type, input_type):
    match int(example_type):
        case 0:
            examples = []
        case 1:
            from examples import example1
            examples = example1.examples
        case _:
            print("Value Error: only 0 or 1 is allowed.")

    match int(prompt_type):
        case 0:
            suffix = ""
        case 1:
            from prompts import prompt1
            suffix = prompt1.prompt
        case 2:
            from prompts import prompt1_kor
            suffix = prompt1_kor.prompt
        case _:
            print("Value Error: only 0 ~ 2 is allowed.")

    try:
        input_type = int(input_type)
    except ValueError:
        print("Value Error: only integer input type is allowed.")
        return False
    else:
        input = Benchmark.input[int(input_type)-1]

    example_prompt = PromptTemplate(input_variables=[
                                "sentence", "relationships"], template="Sentence: {sentence}\nRelationships: {relationships}")
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix=suffix + "Sentence: {input}\nRelationships: ",
        input_variables=["input"]
    )
    return prompt.format(input=input)


def save(model_type, example_type, prompt_type, input_type, time, tokens, output):
    id = str(example_type)+str(prompt_type)+str(input_type)+model_type
    result = {
        'experiment type': {
            'example type': example_type,
            'prompt type': prompt_type,
            'input type': input_type,
            'model': model_type,
        },
        'results': [
            {
                'elapsed time': time,
                'tokens': tokens,
                'output': output
            }
        ]
    }
    
    with open('result.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        if id in data:
            data[id]['results'].append(result['results'][0])
        else:
            data[id] = result
            
    with open('result.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    


@click.command()
@click.option('--model_type', default='koAlpaca5.8', help='model to run on, select one of koAlpaca5.8, koAlpaca12.8, koGPT, koGPT2, openAI')
@click.option('--example_type', default='0', help='model to run on, select one of 0~1')
@click.option('--prompt_type', default='1', help='model to run on, select one of 1~2')
@click.option('--input_type', default='1', help='model to run on, select one of 1~3')
# @click.option('--device_type', default='cuda', help='device to run on, select gpu, cpu or mps')
# @click.option('--db_type', default='chroma', help='vector database to use, select chroma or pinecone')
# @click.option('--embedding_type', default='KoSimCSE', help='embedding model to use, select OpenAI or KoSimCSE.')
def main(model_type, example_type, prompt_type, input_type):
    
    # prompt=prompt(example_type, prompt_type, input_type)
    
    match(model_type):
        case 'koAlpaca5.8':
            from models.KoAlpaca_5 import KoAlpaca_5
            llm = KoAlpaca_5()
        case 'koAlpaca12.8':
            from models.KoAlpaca_12 import KoAlpaca_12
            llm = KoAlpaca_12()
        case 'koGPT':
            from models.KoGPT import KoGPT
            llm = KoGPT()
        case 'koGPT2':
            from models.KoGPT2 import KoGPT2
            llm = KoGPT2()
        case 'openAI':
            from models.ChatOpenAI import ChatOpenai
            llm = ChatOpenai()
            # prompt = 
        case _:
            print("Value Error: Wrong model type.")

    print(llm._llm_type)
    output = llm(prompt=prompt(example_type, prompt_type, input_type))
    print(f"example_type: {example_type}, prompt_type: {prompt_type}, input_type: {input_type}")
    print(llm._identifying_params)
    
    
    # id = str(example_type)+str(prompt_type)+str(input_type)+model_type
    # result = {
    #     'experiment type': {
    #         'example type': example_type,
    #         'prompt type': prompt_type,
    #         'input type': input_type,
    #         'model': llm._identifying_params.get('model'),
    #     },
    #     'results': [
    #         {
    #             'elapsed time': llm._identifying_params.get('elapsed time'),
    #             'tokens': llm._identifying_params.get('tokens'),
    #             'output': output
    #         }
    #     ]
    # }
    
    # with open('result.json', 'r') as f:
    #     data = json.load(f)
    #     if not data[id] is None:
    #         data[id].append(result['results'][0])
    #     else:
    #         data[id] = result
    
    # # with open('result2.json', 'w') as f:
    # #     json.dump(result, f)
    save(model_type, example_type, prompt_type, input_type, llm._identifying_params.get('elapsed time'), llm._identifying_params.get('tokens'), output)

if __name__ == "__main__":
    main()
