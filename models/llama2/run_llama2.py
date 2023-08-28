import fire
import time
# setting path
import sys
sys.path.append('../LLM_experiment')

from inputs.Benchmark import get_articles
from prompts.prompt import prompt_maker
from models.llama2.generation import Llama
from keys.keys import llama2_path
from results.save import save
from models.base_model import output_parser
from results.scoring import scoring
from results.neo4j import save_into_DB
from results.queryonly import queryonly

# build the Llama2 model with the given prompt, inputs and the model name
def build(model:str = 'llama-2-70b', max_seq_len:int = 3000, max_batch_size:int =64):
    generator = Llama.build(
        ckpt_dir=llama2_path + model+'/',
        tokenizer_path=llama2_path + 'tokenizer.model',
        max_seq_len= max_seq_len,
        max_batch_size=max_batch_size
    )
    return generator

# calculate elapsed time from the given start_time
def timer(start_time):
    hours, rem = divmod(time.time() - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(
        int(hours), int(minutes), seconds)


def run(generator, final_inputs, chat:bool):#, max_seq_len:int = 3000, max_batch_size:int = 64):
    # parameters
    # model = 'llama-2-70b-chat' if chat else 'llama-2-70b' 
    max_gen_len = 512
    temperature = 0.1
    top_p = 0.9
    
    # # model build
    # generator = build(model, max_seq_len=max_seq_len, max_batch_size=max_batch_size) #prompt, inputs, 
    
    # run
    start_time = time.time()
    if chat:
        outputs = generator.chat_completion(
            final_inputs,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
    else:
        outputs = generator.text_completion(
            final_inputs,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        
    # return results
    results = []
    for i in range(len(outputs)):
        # elapsed_time
        elapsed_time = timer(start_time)
        
        # parse output
        if chat:
            output = output_parser(outputs[i]['generation']['content'])
        else:
            output = output_parser(outputs[i]['generation'])
            
        results = results + [{
            'elapsed_time': elapsed_time,
            'tokens': -1,
            'output': output
        }]

    return results



def main(kg_type:str='LPG',prompt_type:str='Eng',example_type:str='1', input_type:str='all', chat:str='False'):   
    kg_type, prompt_type, example_type, input_type, chat = str(kg_type), str(prompt_type), str(example_type), str(input_type), bool(chat)
    prompt = prompt_maker(kg_type, prompt_type, example_type, chat = chat)
    
    assert input_type == '4' and kg_type == 'RDF-star' and chat == False
    
    # parameters
    model = 'llama-2-70b-chat' if chat else 'llama-2-70b'
    
    # model build
    generator = build(model, max_seq_len=3000, max_batch_size=64)
    
    
    isdone, start = False, 175 # 0
    while not isdone: 
        inputs, end, isdone = get_articles(start=start)

        # input prompt build
        final_inputs = []
        if chat:        
            for i in range(len(inputs)):
                input_prompt = prompt[-1].copy()
                input_prompt['content'] = input_prompt['content'].format(input=inputs[i])
                final_inputs += [prompt[:-1] + [input_prompt]]
        else:
            for i in range(len(inputs)):
                final_inputs = final_inputs + [prompt.format(input=inputs[i])] 
        
        print("total ", len(final_inputs), "each ", len(final_inputs[0]))
        
        # run
        outputs = run(
            generator=generator,
            final_inputs= final_inputs, 
            chat= chat, 
            # max_seq_len= max(int((len(str(prompt))+len(str(inputs[-1]))+50)/100)*150, 3000), 
            # max_batch_size=max(len(inputs)*2, 64)
        )
        
        # print outputs
        for i, (input, output) in enumerate(zip(inputs, outputs)):
            print(f"** {start+i}) \nInput: ", input)
            print(f"Output: {output['output']}\n") 
            
        print(f"Elapsed Time: {output['elapsed_time']}\ttotal: {len(final_inputs)}")
        
        # save
        filename = save({
                'kg_type': kg_type,
                'prompt_type': prompt_type,
                'example_type': example_type,
                'input_type': input_type,
                'start_idx': start,
                'model_type': 'ChatLlama2' if chat else 'Llama2', 
                'elapsed_time': -1,
                'tokens': -1,
                'inputs': inputs,
                'outputs': outputs
            })
        scorefilename = scoring(filename=filename)
        queryfilename = save_into_DB(filename=scorefilename)
        queryonly(queryfilename)
    
        start = end

if __name__ == "__main__":
    fire.Fire(main)
