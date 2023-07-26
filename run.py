import click
from results.save import save
from prompts.prompt import prompt_maker
from models.base_model import model_loader
from inputs.Benchmark import input_provider


kg_range = ['RDF-star', 'LPG', 'Infoedge', 'all'] # "RDF-star": RDF-star format / "LPG": LPG(Neo4j) format / "Infoedge": Infoedge format (new)
prompt_range = ['None', "Eng", "Kor", 'all'] # "None": No Explanation template / "Eng": English Template / "Kor":Korean Template
example_range = ['0', '1',   'all'] # 0: No example / 1: 4 examples / 2: 100 examples # '2',
input_range = ['0', '1', '2', '3', 'all'] # 0: simple sentences / 1: complex sentences / 2: simple paragraphs / 3: complex paragraphs 
model_range = ['LLAMA2', 'KoGPT', 'ChatOpenAI', 'OpenAI', 'KULLM', 'all'] # Reject: 'KoAlpaca12.8','KoGPT2', 'KoAlpaca5.8'

@click.command()
@click.option('--kg_type', default='all', type=click.Choice(kg_range))
@click.option('--prompt_type', default='all', type=click.Choice(prompt_range))
@click.option('--example_type', default='all', type=click.Choice(example_range))
@click.option('--input_type', default='all', type=click.Choice(input_range))
@click.option('--model_type', default='all', type=click.Choice(model_range))
def main(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str):
    runall(kg_type, prompt_type, example_type, input_type, model_type)
            
def runall(kg_type:str, prompt_type:str, example_type:str, input_type:str,  model_type:str, fast_llm=None):
    if model_type=='all':
        for model in model_range[:-1]:
            llm = model_loader(model_type=model)
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
                        
    else:
        run(kg_type, prompt_type, example_type, input_type, model_type, fast_llm=fast_llm)


    
def run(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str, fast_llm=None):
    
    if not fast_llm is None:
        llm = fast_llm
    else:
        llm = model_loader(model_type=model_type)
    prompt = prompt_maker(kg_type, prompt_type, example_type)
    inputs = input_provider(input_type)
    outputs = []
    
    print(f"\n> kg_type: {kg_type}, prompt_type: {prompt_type}, example_type: {example_type}, input_type: {input_type}, model_type: {model_type}")

    for i in range(len(inputs)):
        print(f"** {i}) \nInput: ", inputs[i])
        output = llm(prompt=prompt.format(input=inputs[i]))
        print(f"Output: {output}\n") 
        outputs = outputs + [output]
    
    save({
        'kg_type': kg_type,
        'prompt_type': prompt_type,
        'example_type': example_type,
        'input_type': input_type,
        'model_type': model_type, 
        'elapsed_time': llm._identifying_params.get('elapsed time'),
        'tokens': llm._identifying_params.get('tokens'),
        'outputs': outputs
    })

if __name__ == "__main__":
    main()
