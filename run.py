import click
from results.save import save
from prompts.prompt import prompt_maker
from models.base_model import model_loader
from inputs.Benchmark import input_provider
from results.scoring import scoring
from results.neo4j import save_into_DB

kg_range = ['RDF-star', 'LPG_tense', 'all'] # "RDF-star": RDF-star format / "LPG_tense": LPG(Neo4j) format # 추가 기능: 'Infoedge', 'LPG'(LPG 기본형), 'LPG_id', 'LPG_sem', 'LPG_rea' (LPG_tense의 변형들)
prompt_range = ['None', "Eng", "Kor", 'all'] # "None": No Explanation template / "Eng": English Template / "Kor": Korean Template / "all": Experiment repeatedly in each language Template
example_range = ['0', '1',  'all'] # 0: No example / 1: 10 examples 
input_range = ['0', '1', '2', '3', '4', '5', 'all'] # 각 번호의 의미는 inputs/Benchmark.py 참고!! # 추가 기능: 'one'(1형 문장들), 'two'(2형 문장들), 'three'(3형 문장), 'four'(4형 문장), 'five'(5형 문장), 'nested' (겹문장), 'parallel' (대등하게 이어진 문장), 'dependent' (종속적으로 이어진 문장)
model_range = ['ChatLlama2', 'Llama2', 'ChatOpenAI', 'OpenAI', 'KoGPT2', 'KoAlpaca12.8','KoAlpaca5.8', 'KoGPT', 'KULLM', 'all'] 

# runall : 반복 실험을 관리하는 함수
# 각 option 값이 'all'인 경우, 가능한 모든 경우에 대해 loop를 돌려 모두 실행
# fast_llm : 반복 실험에서 LLM model을 매번 load하지 않도록 parameter로 llm을 넘겨준다. (따로 넣어줄 필요는 없음. 함수 내부에서 생성, 전달됨.)
def runall(kg_type:str, prompt_type:str, example_type:str, input_type:str,  model_type:str, fast_llm=None):

    if model_type=='all':
        for model in model_range[:-1]:
            if not 'Llama2' in model:
                llm = model_loader(model_type=model)
            else: 
                llm = None
            runall(kg_type, prompt_type, example_type, input_type, model, fast_llm=llm)
            
    elif kg_type=='all':
        for kg in kg_range[:-1]:
            runall(kg, prompt_type, example_type, input_type, model_type, fast_llm=fast_llm)
     
    elif prompt_type=='all':
        for prompt in prompt_range[:-1]:
            runall(kg_type, prompt, example_type, input_type, model_type, fast_llm=fast_llm)
    
    elif example_type=='all':
        for example in example_range[:-1]:
            runall(kg_type, prompt_type, example, input_type, model_type, fast_llm=fast_llm)
                        
    else: # 이제 'all'에 해당하는 type이 사라졌으니, run 함수를 통해 실험 돌리기
        run(kg_type, prompt_type, example_type, input_type, model_type, fast_llm=fast_llm)


    
    
def run(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str, fast_llm=None):
     
    inputs = input_provider(input_type)
    prompt = prompt_maker(kg_type, prompt_type, example_type)
    outputs = []
    
    # print the experiment type
    print(f"\n> kg_type: {kg_type}, prompt_type: {prompt_type}, example_type: {example_type}, input_type: {input_type}, model_type: {model_type}")

    if not 'Llama2' in model_type:
        if not fast_llm is None:
            llm = fast_llm
        else:
            llm = model_loader(model_type=model_type)
        
        for i in range(len(inputs)):
            # print input text
            print(f"** {i}) \nInput: ", inputs[i])
            
            output = llm(prompt=prompt.format(input=inputs[i]))
                
            # print output KG
            print(f"Output: {output}\n") 
            outputs = outputs + [{
                'elapsed_time': llm._identifying_params.get('elapsed time'),
                'tokens': llm._identifying_params.get('tokens'),
                'output': output
            }]
            
        filename = save({
            'kg_type': kg_type,
            'prompt_type': prompt_type,
            'example_type': example_type,
            'input_type': input_type,
            'model_type': model_type,
            'outputs': outputs
        })
        scorefilename = scoring(filename=filename)
        save_into_DB(filename=scorefilename)
        
    
    else: # Llama2 or ChatLlama2
        from torch.distributed.run import parse_args, run
        args = parse_args(['--nproc_per_node', '8', 
                           '--rdzv-endpoint', 'localhost:29501',
                           'models/llama2/run_llama2.py',
                                  '--kg_type', kg_type, 
                                  '--prompt_type', prompt_type,
                                  '--example_type', example_type,
                                  '--input_type', input_type,
                                  '--chat', 'True' if model_type=='ChatLlama2' else 'False'])
        run(args)
        
    
# main 함수: python3 run.py (--kg=~~) (--prompt=~~) (--example=~~) (--input=~~) (--model=~~) (--chain=~~)의 형태로 실행
# kg:       knowledge graph의 출력 형식을 지정
# prompt:   KG 출력 형식에 대한 설명 template의 종류를 지정 (몇 형식은 영어 버전만 지원)
# example:  zero-shot or few(10)-shot 설정할 수 있음
# input:    inference할 input data의 종류를 지정
# model:    사용할 LLM model 종류 지정

# 실행 예시는 run.sh 파일 참고
@click.command()
@click.option('--kg', default='RDF-star', type=click.Choice(kg_range))     # kg_range list 원소 중 하나를 입력할 수 있음 (기본값: RDF-star)
@click.option('--prompt', default='Eng', type=click.Choice(prompt_range))   # prompt_range list 원소 중 하나를 입력할 수 있음 (기본값: Eng)
@click.option('--example', default='1', type=click.Choice(example_range))   # example_range list 원소 중 하나를 입력할 수 있음 (기본값: 1)
@click.option('--input', default='4', type=click.Choice(input_range))       # input_range list 원소 중 하나를 입력할 수 있음 (기본값: 4)
@click.option('--model', default='ChatLlama2', type=click.Choice(model_range))     # model_range list 원소 중 하나를 입력할 수 있음 (기본값: ChatLlama2)
def main(kg:str,prompt:str,example:str, input:str,  model:str):
    runall(kg, prompt, example, input, model)
            

if __name__ == "__main__":
    main()
