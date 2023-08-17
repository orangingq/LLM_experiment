import csv
from os import path
from datetime import datetime

# save results into the csv file
def save_into_DB(filename=''):
    if filename == '':
        now = datetime.now().strftime("%Y%m%d_%H")
        filename = './results/scored/scored_'+now+'.csv'
    
    # raise an error if not exists
    if not path.exists(filename):
        raise NameError(f"Cannot read file named '{path.abspath(filename)}'.")
    
    queryfilename = './results/queries/query_'+filename.split('/scored_')[1]
    
    qf = open(queryfilename, mode='w', encoding="utf-8", newline='')
    wr = csv.writer(qf)
    wr.writerow(['input', 'query'])

    memory = []    
    with open(filename, mode='r', encoding="utf-8") as f:
        csv_file = csv.reader(f, delimiter=",")
        for row in csv_file:
            if row[6] == 'output':
                continue
            if int(row[7]) == 0: # structure score is 0
                continue
            # if int(row[4]) > 6: ###############
            #     continue
            # if len(row[5]) >200 and not row[4] == '0': ###############
            #     continue
            id = ''.join(row[0:5])+row[5][:5]+str(len(row[5]))+row[7]
            if id in memory:
                continue
            
            output = row[6]
            output = output.rstrip('\n').replace('\n', '\nCREATE ')
            output = 'CREATE ' + output
            wr.writerow([row[5], output])
            memory.append(id)
    # print(memory, len(memory))
    qf.close()
    
    print(f"\nquery saved: {queryfilename}")
    return queryfilename

# save_into_DB(filename='./results/scored/scored_20230810_15.csv')