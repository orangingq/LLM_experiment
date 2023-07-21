import click
from results.save import save
from prompts.prompt import prompt_maker
from models.base_model import model_loader

kg_range = ['RDF-star', 'LPG', 'Infoedge', 'all'] # "RDF-star": RDF-star format / "LPG": LPG(Neo4j) format / "Infoedge": Infoedge format (new)
prompt_range = ['None', "Eng", "Kor", 'all'] # "None": No Explanation template / "Eng": English Template / "Kor":Korean Template
example_range = ['0', '1', '2', 'all'] # 0: No example / 1: 4 examples / 2: 100 examples
input_range = ['0', '1', '2', '3', '4'] # 0: 1 simple sentence / 1: 1 complex sentence / 2: 1 complex paragraph / 3: 10 inputs / 4: 100 inputs
model_range = ['koGPT', 'chatOpenAI', 'openAI', 'koAlpaca12.8','koGPT2', 'koAlpaca5.8', 'all']

@click.command()
@click.option('--kg_type', default='all', type=click.Choice(kg_range), help='"RDF-star": RDF-star format\n"LPG": LPG(Neo4j) format\n"Infoedge": Infoedge format (new)')
@click.option('--prompt_type', default='all', type=click.Choice(prompt_range), help='"None": No Explanation template\n"Eng": English Template\n"Kor":Korean Template')
@click.option('--example_type', default='all', type=click.Choice(example_range), help='0: No example\n1: 4 examples\n2: 100 examples')
@click.option('--input_type', default='0', type=click.Choice(input_range), help="0: 1 simple sentence\n1: 1 complex sentence\n2: 1 complex paragraph\n3: 10 inputs\n4: 100 inputs")
@click.option('--model_type', default='all', type=click.Choice(model_range), help='model to run on, select one of koAlpaca5.8, koAlpaca12.8, koGPT, koGPT2, chatOpenAI, openAI')
def main(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str):
    if kg_type=='all':
        for kg in kg_range[:-1]:
            main(kg, prompt_type, example_type, input_type, model_type)
     
    elif prompt_type=='all':
        for prompt in prompt_range[:-1]:
            main(kg_type, prompt, example_type, input_type, model_type)
    
    elif example_type=='all':
        for example in example_range[:-1]:
            main(kg_type, prompt_type, example, input_type, model_type)
            
    elif model_type=='all':
        for model in model_range[:-1]:
            main(kg_type, prompt_type, example_type, input_type, model)
            
    else:
        run(kg_type, prompt_type, example_type, input_type, model_type)
            

    
def run(kg_type:str,prompt_type:str,example_type:str, input_type:str,  model_type:str):
    print(f"\n> kg_type: {kg_type}, prompt_type: {prompt_type}, example_type: {example_type}, input_type: {input_type}, model_type: {model_type}\n")
    
    llm = model_loader(model_type=model_type)
    prompt = prompt_maker(kg_type, prompt_type, example_type, input_type)
    
    output = llm(prompt=prompt)
    print("\n> output results: ", llm._identifying_params)
    
    save({
        'kg_type': kg_type,
        'prompt_type': prompt_type,
        'example_type': example_type,
        'input_type': input_type,
        'model_type': model_type, 
        'elapsed_time': llm._identifying_params.get('elapsed time'),
        'tokens': llm._identifying_params.get('tokens'),
        'output': output
    })

    

if __name__ == "__main__":
    main()
