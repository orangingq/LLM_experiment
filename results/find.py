import csv
from os import path
from datetime import datetime
import sys
 
# setting path
sys.path.append('../LLM_experiment')
from run  import kg_range, prompt_range, example_range, input_range, model_range

def findall(date:str=''):
    exists = []
    not_exists = []
    for kg in kg_range[:-1]:
        for pr in prompt_range[:-1]:
            for ex in example_range[:-1]:
                for inp in input_range[:-1]:
                    for mo in model_range[:-1]:
                        resarr = find(date, kg, pr, ex, inp, mo, 0)
                        if len(resarr) == 0:
                            not_exists += [[kg, pr, ex, inp, mo]]
                        else:
                            exists += [[kg, pr, ex, inp, mo]]

    print(f"** Existing Rows: ({len(exists)})")
    for e in exists:
        [kg, pr, ex, inp, mo] = e
        print(f"KG: {kg}\tprompt: {pr}\texample: {ex}\tinput: {inp}\tmodel: {mo}\t")
    
    print(f"\n** Not Existing Rows: ({len(not_exists)})")
    for e in not_exists:
        [kg, pr, ex, inp, mo] = e
        print(f"KG: {kg}\tprompt: {pr}\texample: {ex}\tinput: {inp}\tmodel: {mo}\t")


def find(date:str='', kg_type:str = 'all', prompt_type:str = 'all', example_type:str= 'all', input_type:str= 'all',  model_type:str= 'all', print_output:int=1):
   
    if date == '':
        date = datetime.now().strftime("%Y%m%d")
    
    filename = './results/result_'+date+'.csv'
    
    # return False if file does not exist
    if not path.exists(filename):
        print(f"No file named '{path.abspath(filename)}' was searched.")
        return []
    
    csv_file = csv.reader(open(filename, "r"), delimiter=",")

    #loop through the csv list
    retarr = []
    if print_output > 0:
        print("** Search Start!\n")
    for row in csv_file:
        if kg_type == 'all' or row[0] == kg_type:
            if prompt_type == 'all' or row[1] == prompt_type:
                if example_type == 'all' or row[2] == example_type:
                    if input_type == 'all' or row[3] == input_type:
                        if model_type == 'all' or row[4] == model_type:
                            if print_output > 0:
                                print(f"** KG: {row[0]}\tprompt: {row[1]}\texample: {row[2]}\tinput: {row[3]}\tmodel: {row[4]}")
                                if print_output > 1: 
                                    print(f"Input: \n{row[8]}\nOutput: \n{row[9]}\n")

                            retarr += [row]
                        # elif model_type == 'all': 
                        #     print(f"** KG: {row[0]}\prompt: {row[1]}\texample: {row[2]}\tinput: {row[3]}\tmodel: {row[4]} \t-> Not Exist")
                    # elif input_type == 'all': 
                    #     print(f"** KG: {row[0]}\prompt: {row[1]}\texample: {row[2]}\tinput: {row[3]}\tmodel: {row[4]} \t-> Not Exist")
    if print_output > 0:                     
        print("** Search End!\n");
    return retarr


findall(date='20230721')