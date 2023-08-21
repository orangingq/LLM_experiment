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
            
            id = ''.join(row[0:5])+row[5][:5]+str(len(row[5]))+row[7]
            if id in memory:
                continue
            
            output = row[6]
            if 'RDF' in row[0]:
                output = TripleToNeo4j(output)
            elif 'LPG' in row[0]:
                output = output.rstrip('\n').replace('\n', '\nCREATE ')
                output = 'CREATE ' + output
                
            wr.writerow([row[5], output])
            memory.append(id)
    # print(memory, len(memory))
    qf.close()
    
    print(f"\nquery saved: {queryfilename}")
    return queryfilename

# save_into_DB(filename='./results/scored/scored_20230810_15.csv')
            
def next_alphabet(curr):
    if curr[-1] == 'z':
        return curr+'a'
    else:
        return curr[:-1] + chr(ord(curr)+1)

def TripleToNeo4j(triple):
    create_nodes = ''
    create_edges = ''
    alphabet = 'a'
    next_a = next_alphabet(alphabet)

    for line in triple.split('\n'):
        pair = line.split(' - ')
        ent1, rel, ent2 = pair[0], pair[1], pair[2]
        [ent1, ent1_type] = ent1.split(':')
        [ent2, ent2_type] = ent2.split(':')
        
        create_nodes += f'CREATE ({alphabet}:{ent1_type.capitalize()} {{name: “{ent1}“}});\n'
        create_nodes += f'CREATE ({next_a}:{ent2_type.capitalize()} {{name: “{ent2}“}});\n'
        
        if "'" in rel:
            continue
        create_edges.append(f'MATCH ({alphabet}), ({next_a}) WHERE {alphabet}.name = “{ent1}” AND {next_a}.name = “{ent2}” CREATE ({alphabet})-[r:{rel.replace(" ", "_")}]->({next_a});\n')
        
        # update alphabets
        alphabet = next_alphabet(next_a)
        next_a = next_alphabet(alphabet)
        
    # print(len(create_nodes), create_nodes[0])
    # print(len(create_edges), create_edges[0])
    # create_nodes = list(set(create_nodes))
    # create_edges = list(set(create_edges))
    # with open(‘tfidf_greedy/graph_cypher_query.txt’, ‘w’) as fw:
    #     for line in create_nodes + create_edges:
    #         fw.write(f”{line}\n”)
    return create_nodes + create_edges[:-2]
