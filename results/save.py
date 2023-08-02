import csv
from os import path
from datetime import datetime
from inputs.Benchmark import input_provider

# save results into the csv file
def save(save_info)->str:
   
    now = datetime.now().strftime("%Y%m%d_%H")
    
    filename = './results/result_'+now+'.csv'
    
    # create a csv file if not exists
    if not path.exists(filename):
        f = open(filename, mode='w', encoding="utf-8", newline='')
        wr = csv.writer(f)
        wr.writerow(['kg', 'prompt', 'example', 'input', 'model', 'elapsed time', 'tokens', 'input_idx', 'input', 'output'])
        f.close()
            
    inputs = input_provider(save_info['input_type'])
    outputs = save_info['outputs']
    assert(len(inputs) == len(outputs))
    
    # save the results
    f= open(filename, mode='a', encoding="utf-8", newline='')
    wr = csv.writer(f)
    for i in range(len(inputs)):
        wr.writerow([save_info['kg_type'], save_info['prompt_type'], save_info['example_type'], save_info['input_type'], save_info['model_type'], outputs[i]['elapsed_time'], outputs[i]['tokens'], i, inputs[i], outputs[i]['output']])    
    f.close()
    
    print(f"output saved: {filename}")
    return filename