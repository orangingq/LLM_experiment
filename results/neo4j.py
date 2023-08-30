import csv
from os import path
from datetime import datetime


def next_alphabet(curr):
    up = -1
    while -up <= len(curr) and curr[up] == 'z':
        up -= 1
    
    if -up == len(curr) + 1: # next order
        return 'a'*(len(curr)+1)
    else:
        return curr[:up] + chr(ord(curr[up])+1)+'a'*(-up-1)

# Covert triples to the Neo4j format
def TripleToNeo4j(triple:str, startvar='a'):
    create_nodes = ''
    create_edges = ''
    nodelist = []
    edgelist = []
    varlist = []
    alphabet = startvar
    next_a = next_alphabet(alphabet)
    
    triple = ''.join(triple.split('(')[1:])
    triple = ''.join(triple.split(')')[:-1])
    for line in triple.split('\n'):
        pair = line.split(' - ')
        if len(pair) != 3: 
            continue
        [ent1, rel, ent2] = pair
        [ent1, ent1_type] = ent1.split(':')
        [ent2, ent2_type] = ent2.split(':')
        
        nodes = [f':{ent1_type.capitalize()} {{name: "{ent1}"}})', f':{ent2_type.capitalize()} {{name: "{ent2}"}})']
        now = [alphabet, next_a]
        for i, n in enumerate(nodes):
            if i==0:
                a = alphabet
            else:
                a = next_a
                
            if n in nodelist: 
                idx = nodelist.index(n)
                now[i] = varlist[idx]
            else:
                create_nodes += f'CREATE ({now[i]}'+n+'\n'
                nodelist += [n]
                varlist += [a]
                        
        if "'" in rel:
            continue
        
        edge = f'({now[0]})-[:{rel.replace(" ", "_")}]->({now[1]})'
        if not edge in edgelist:
            create_edges += f'CREATE ({now[0]})-[:{rel.replace(" ", "_")}]->({now[1]})\n' #MATCH ({alphabet}), ({next_a}) WHERE {alphabet}.name = “{ent1}” AND {next_a}.name = “{ent2}” 
            edgelist += [edge]
            
        # update alphabets
        alphabet = next_alphabet(next_a)
        next_a = next_alphabet(alphabet)
        
    return create_nodes + create_edges[:-1], alphabet



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
    startvar = 'a'

    with open(filename, mode='r', encoding="utf-8") as f:
        csv_file = csv.reader(f, delimiter=",")
        for row in csv_file:
            if row[6] == 'output':
                continue
            if int(row[7]) == 0: # structure score is 0
                continue
            
            id = ''.join(row[0:5])+row[5][:5]+str(len(row[5]))+row[7]
            if id in memory:
                continue
            
            output = row[6].rstrip('\n')
            if 'RDF' in row[0]:
                output, startvar = TripleToNeo4j(output, startvar)
            elif 'LPG' in row[0]:
                output = 'CREATE ' + output.replace('\n', '\nCREATE ')
                
            wr.writerow([row[5], output])
            memory.append(id)

    qf.close()
    
    print(f"\nquery saved: {queryfilename}")
    return queryfilename

# save_into_DB(filename='./results/scored/scored_20230821_18.csv')
            