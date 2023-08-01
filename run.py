import click
from results.save import save
from prompts.prompt import prompt_maker
from models.base_model import model_loader
from inputs.Benchmark import input_provider
from langchain.chains import LLMChain

kg_range = ['RDF-star', 'LPG', 'LPG_tense', 'LPG_id',  'all'] # "RDF-star": RDF-star format / "LPG": LPG(Neo4j) format / "Infoedge": Infoedge format (new) # Reject: 'Infoedge',
prompt_range = ['None', "Eng", "Kor", 'all'] # "None": No Explanation template / "Eng": English Template / "Kor":Korean Template
example_range = ['0', '1',   'all'] # 0: No example / 1: 4 examples / 2: 100 examples # '2',
input_range = ['one', 'two', 'three', 'four', 'five', 'nested', 'parallel', 'dependent', '0', '1', '2', '3', 'all'] # 0: simple sentences / 1: complex sentences / 2: simple paragraphs / 3: complex paragraphs 
model_range = ['ChatLlama2', 'Llama2', 'ChatOpenAI', 'OpenAI', 'all'] # Reject: 'KoAlpaca12.8','KoGPT2', 'KoAlpaca5.8', 'KoGPT', 'KULLM', 


def runall(kg_type:str, prompt_type:str, example_type:str, input_type:str,  model_type:str, fast_llm=None, chain=False):

    if model_type=='all':
        for model in model_range[:-1]:
            if not 'Llama2' in model_type:
                llm = model_loader(model_type=model)
            else: 
                llm = None
            runall(kg_type, prompt_type, example_type, input_type, model, fast_llm=llm, chain=chain)
            
    elif kg_type=='all':
        for kg in kg_range[:-1]:
            runall(kg, prompt_type, example_type, input_type, model_type, fast_llm=fast_llm, chain=chain)
     
    elif prompt_type=='all':
        for prompt in prompt_range[:-1]:
            runall(kg_type, prompt, example_type, input_type, model_type, fast_llm=fast_llm, chain=chain)
    
    elif example_type=='all':
        for example in example_range[:-1]:
            runall(kg_type, prompt_type, example, input_type, model_type, fast_llm=fast_llm, chain=chain)
                        
    else:
        run(kg_type, prompt_type, example_type, input_type, model_type, fast_llm=fast_llm, usechain=chain)


    
def run(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str, fast_llm=None, usechain:bool=False):
     
    inputs = input_provider(input_type)
    prompt = prompt_maker(kg_type, prompt_type, example_type)
    outputs = []
    
    print(f"\n> kg_type: {kg_type}, prompt_type: {prompt_type}, example_type: {example_type}, input_type: {input_type}, model_type: {model_type}, chain: {usechain}")

    if not 'Llama2' in model_type:
        if not fast_llm is None:
            llm = fast_llm
        else:
            llm = model_loader(model_type=model_type)
        
        for i in range(len(inputs)):
            print(f"** {i}) \nInput: ", inputs[i])
            
            if usechain == True:
                chain = LLMChain(llm=llm.model, prompt=prompt)
                output = chain.run(inputs[i])
                
            else:
                output = llm(prompt=prompt.format(input=inputs[i]))
                
            print(f"Output: {output}\n") 
            outputs = outputs + [{
                'elapsed_time': llm._identifying_params.get('elapsed time'),
                'tokens': llm._identifying_params.get('tokens'),
                'output': output
            }]
            
        save({
            'kg_type': kg_type,
            'prompt_type': prompt_type,
            'example_type': example_type,
            'input_type': input_type,
            'model_type': model_type if not usechain else model_type + '_chain', 
            'outputs': outputs
        })
    
    else: # Llama2 or ChatLlama2
        from torch.distributed.run import parse_args, run
        args = parse_args(['--nproc_per_node', '8', 'models/llama2/run_llama2.py',
                                  '--kg_type', kg_type, 
                                  '--prompt_type', prompt_type,
                                  '--example_type', example_type,
                                  '--input_type', input_type,
                                  '--chat', 'True' if model_type=='ChatLlama2' else 'False'])
        run(args)
        
    

@click.command()
@click.option('--kg', default='all', type=click.Choice(kg_range))
@click.option('--prompt', default='all', type=click.Choice(prompt_range))
@click.option('--example', default='all', type=click.Choice(example_range))
@click.option('--input', default='all', type=click.Choice(input_range))
@click.option('--model', default='all', type=click.Choice(model_range))
@click.option('--chain', default='0', type=click.Choice(['1', '0']))
def main(kg:str,prompt:str,example:str, input:str,  model:str, chain:str):
    chain_p = True if chain == '1' else False
    runall(kg, prompt, example, input, model, chain=chain_p)
            

if __name__ == "__main__":
    main()
