import csv
from os import path
from datetime import datetime

# extract only queries from the query file
def queryonly(filename=''):
    if filename == '':
        now = datetime.now().strftime("%Y%m%d_%H")
        filename = './results/queries/query_'+now+'.csv'
    
    # raise an error if not exists
    if not path.exists(filename):
        raise NameError(f"Cannot read file named '{path.abspath(filename)}'.")
    
    queryfilename = './results/onlyqueries/RDF_Llama2_gensim_'+filename.split('/query_')[1].split('.csv')[0]+'.txt'
    
    qf = open(queryfilename, mode='a', encoding="utf-8")

    # memory = []    
    with open(filename, mode='r', encoding="utf-8") as f:
        csv_file = csv.reader(f, delimiter=",")
        for row in csv_file:
            input, query = row
            
            if query == 'query':
                continue
            if input.startswith('['):
                continue
            
            qf.write(query)
            qf.write('\n\n')
        
    qf.close()
    
    print(f"\nquery saved: {queryfilename}")
    return queryfilename


queryonly(filename='results/queries/query_YYYYmmdd_hh.csv') # ex) results/queries/query_20230825_14.csv