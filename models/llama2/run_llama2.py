import fire
import time
# setting path
import sys
sys.path.append('../LLM_experiment')

from inputs.Benchmark import input_provider
from prompts.prompt import prompt_maker
from models.llama2.generation import Llama
from keys.keys import llama2_path
from results.save import save
from models.base_model import output_parser

def build(prompt:str, inputs, model:str = 'llama-2-70b'):
    generator = Llama.build(
        ckpt_dir=llama2_path + model+'/',
        tokenizer_path=llama2_path + 'tokenizer.model',
        max_seq_len= int(len(str(prompt))/100)*120,
        max_batch_size=int(len(inputs))*2
    )
    return generator

def run(prompt:str, inputs):
    
    # model build
    generator = build(prompt, inputs)

    final_inputs = []
    for i in range(len(inputs)):
        final_inputs = final_inputs + [prompt.format(input=inputs[i])] #+ 'Do not repeat same output. Do not make another "Sentence".'
    
    # run
    start_time = time.time()
    outputs = generator.text_completion(
        final_inputs,
        max_gen_len=512,
        temperature=0,
        top_p=0.9,
    )
        
    results = []
    for i in range(len(outputs)):
        # elapsed_time
        elapsed_time = timer(start_time)
        
        # parse output
        output = output_parser(outputs[i]['generation'])
        
        print(f"** {i}) \nInput: ", inputs[i])
        print(f"Output: {output}\n") 
        results = results + [{
            'elapsed_time': elapsed_time,
            'tokens': -1,
            'output': output
        }]

    return results


def timer(start_time):
    hours, rem = divmod(time.time() - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(
        int(hours), int(minutes), seconds)

def main(kg_type:str='LPG',prompt_type:str='Eng',example_type:str='1', input_type:str='all'):   
 
    prompt = prompt_maker(str(kg_type), str(prompt_type), str(example_type))
    inputs = input_provider(str(input_type))

    # run
    outputs = run(prompt, inputs)
    
    # save
    save({
            'kg_type': kg_type,
            'prompt_type': prompt_type,
            'example_type': example_type,
            'input_type': input_type,
            'model_type': 'Llama2', 
            'elapsed_time': -1,
            'tokens': -1,
            'outputs': outputs
        })


if __name__ == "__main__":
    fire.Fire(main)