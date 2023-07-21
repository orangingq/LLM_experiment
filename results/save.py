import csv
from os import path
from datetime import datetime

# save results into the csv file
def save(save_info)->None:
   
    today = datetime.now().strftime("%Y%m%d")
    
    filename = './results/result_'+today+'.csv'
    if not path.exists(filename):
        f = open(filename, 'w', encoding="utf-8", newline="")
        wr = csv.writer(f)
        wr.writerow(['kg', 'prompt', 'example', 'input', 'model', 'elapsed time', 'tokens', 'output'])
        f.close()
            
    f= open(filename, 'a', encoding="utf-8", newline="")
    wr = csv.writer(f)
    wr.writerow([save_info['kg_type'], save_info['prompt_type'], save_info['example_type'], save_info['input_type'], save_info['model_type'], save_info['elapsed_time'], save_info['tokens'], save_info['output']])    
    f.close() 
    
    print(f"output saved: {filename}")
    return