from datetime import datetime
from os import path
import csv
import re

# score the structural completeness of LPG(_...) format
def scoring(filename:str=''):
    if filename == '':
        now = datetime.now().strftime("%Y%m%d_%H")
        filename = './results/results/result_'+now+'.csv'
        
    scorefilename = './results/scored/scored_'+filename.split('/result_')[1]
        
    if not path.exists(filename):
        raise NameError(f"No file named '{path.abspath(filename)}' was searched.")
    
         
    sf = open(scorefilename, mode='w', encoding="utf-8", newline='')
    wr = csv.writer(sf)
    wr.writerow(['kg', 'prompt', 'example', 'model', 'input_idx', 'input', 'output', 'structure_score', 'note'])
    
    f = open(filename, mode="r")
    # loop through the csv list
    for row in csv.reader(f, delimiter=","):
        # if not 'LPG' in row[0]:
        #     continue
        kg, prompt, example, model, input_idx, input, output = row[0], row[1], row[2], row[4], row[7], row[8], row[9]

        if 'LPG' in row[0]:
            output, score, note = LPG_structure_score(output)
        elif 'RDF' in row[0]:
            output, score, note = RDF_structure_score(output)
        else:
            continue
        
        wr.writerow([kg, prompt, example, model, input_idx, input, output, score, note])
        
    f.close()
    sf.close()
    print(f"\nresult saved: {scorefilename}")
    return scorefilename
       
def RDF_structure_score(output):
    total_score, note = 1, ''
    scored = False # check if the output was scored
    
    parsed_output = ""
    querylist = output.split(')')      
    stop = False   # stop scoring if unformatted query was found.
    record = ""
    for i, query in enumerate(querylist):
        query = query.lstrip(', \t').rstrip(', \t')     
        
        leave_out = False # don't put the query line into the output.

        if len(query) < 3 or query[0] != '(':
            continue 
        query += ')'
        
        print(query)

        # scoring
        if not stop:
            # node
            score = triple_score(query)
            
            if score == 0:
                if  i < len(querylist)-1:
                    total_score = 0
                    note = query
                    stop = True
                else:
                    leave_out = True
            elif record == query:
                leave_out = True
            else:
                record = query
                scored = True
                    
        if not leave_out:
            parsed_output = parsed_output + query + "\n"
            
    if not scored:
        total_score = 0
    return parsed_output, total_score, note
      
                    
def LPG_structure_score(output):
    total_score, note = 1, ''
    node_scored = False # check if the output was scored
    edge_scored = False
    
    varlist = []
    parsed_output = ""
    querylist = output.split('\n')      
    stop = False   # stop scoring if unformatted query was found.
    node_record = ""
    edge_record = ""
    for i, query in enumerate(querylist):
        query = query.lstrip(' \t').rstrip(' \t')     
        query = query.replace('{{', '{').replace('}}', '}')       
        leave_out = False # don't put the query line into the output.

        if len(query) < 3:
            continue
        
        # scoring
        if not stop:
            # node
            n_score, query, varlist = node_score(query, varlist=varlist, check_var=True)
            if n_score == 0:
                # edge
                e_score, query, varlist = edge_score(query, varlist=varlist)
                if e_score == 0 :
                    if  i < len(querylist)-1:
                        total_score = 0
                        note = query
                        stop = True
                    else:
                        leave_out = True
                elif edge_record == query:
                    leave_out = True
                else:
                    edge_record = query
                    edge_scored = True
                    
            elif node_record == query[5:]:
                leave_out = True
            else:
                node_record = query[5:]
                node_scored = True
        if not leave_out:
            parsed_output = parsed_output + query + "\n"
            
    if not node_scored and not edge_scored:
        total_score = 0
    if len(varlist)>10 and not edge_scored:
        total_score = 0
    return parsed_output, total_score, note
      

def triple_score(query):
    # regular expression format
    node1_format = "(?P<name1>\w[\w ]*\w):(?P<label1>[\w]+)"
    node2_format = "(?P<name2>\w[\w ]*\w):(?P<label2>[\w]+)"
    edge_format = "(?P<edge>\w[\w ]*\w)"
    format = "^[(]" + node1_format + "[ ]{1,3}-[ ]{1,3}" + edge_format + "[ ]{1,3}-[ ]{1,3}" + node2_format + "[)]$"
    p = re.compile(format)
    m = p.search(query)
    
    if not m is None:
        score = 1
    else:
        score = 0
        # # Check label
        # label = m.group('label')
        # if ' ' in label:
        #     new_label = label.replace(' ', '_')
        #     idx =  m.start('label')
        #     new_query = query[:idx] + new_label + query[idx+len(label):]
        #     # print("replaced: ", query , " -> ", new_query)
        #     return node_score(new_query, varlist, check_var)
        
        # # Check attributes
        # att_score = 1
        # attributes = m.group('attributes')
        # if not attributes is None: 
        #     att_score = attribute_score(attributes, varlist=varlist)
        
        # # Check variable
        # var = m.group("var")
        # # print("node var: ", var)
        # if var is None:
        #     score = 1
        # elif not var in varlist:
        #     varlist += [var]
        #     score = 1
             
        # if score == 1 and att_score == 0:
        #     score = 0
    
    # print("node score:", score)
    return score
    

                
# attribute format: {att_label: 'att_val'} or {att_label: (att_var)}
def attribute_score(attributes, varlist, check_var=True):
    # regular expression format
    att_label_format = "^[ ]{0,3}\w+[ ]{0,3}$"
    att_val_format = "^[ ]{0,3}((?P<start>[']|[\"])[^\t\n\r\f\v'\"]+(?P=start)|[(](?P<att_var>\w+)[)]|\d+|[T][r][u][e]|[F][a][l][s][e])[ ]{0,3}$"
    p_al = re.compile(att_label_format) 
    p_av = re.compile(att_val_format)
    
    # for each attribute
    att_list = attributes[1:-1].split(',')
    att_score = 1
    for att in att_list:
        splitted = att.rstrip('\t ').lstrip('\t ').split(':')
        if len(splitted) == 2: # split into attribute label and attribute value
            att_label, att_val = splitted
            m_al, m_av = p_al.match(att_label), p_av.match(att_val)
            if m_al is None or m_av is None:
                att_score = 0
                break
            else:
                att_var = m_av.group('att_var')
                if check_var and not att_var is None:
                    att_score = 0
                    break
                elif not att_var is None and not att_var in varlist:
                    att_score = 0
                    break
                
    # print(att_score, att_list)
    return att_score

# node format: (var:label {att_label: att_val})
def node_score(query, varlist, check_var=False):
    score = 0
    
    # regular expression format
    var_format = "(?P<var>\w+)" + ('' if check_var else '?')
    label_format = "(?P<label>(\w|[ ]|:)*\w)"
    attribute_format = "(?P<attributes>[{].+[}])?"
    node_format = "^[(]" + var_format + "?:[ ]{0,3}"+label_format+"[ ]{0,3}"+attribute_format+"[)]$" #(?P<attributes>[{]\w+:\s?['].+['](,\s{0,3}\w+:\s?['].+['])*[}])?
    p = re.compile(node_format) 
    m = p.search(query)
    
    if not m is None:
        # Check label
        label = m.group('label')
        if ' ' in label:
            new_label = label.replace(' ', '_')
            idx =  m.start('label')
            new_query = query[:idx] + new_label + query[idx+len(label):]
            # print("replaced: ", query , " -> ", new_query)
            return node_score(new_query, varlist, check_var)
        
        # Check attributes
        att_score = 1
        attributes = m.group('attributes')
        if not attributes is None: 
            att_score = attribute_score(attributes, varlist=varlist)
        
        # Check variable
        var = m.group("var")
        # print("node var: ", var)
        if var is None:
            score = 1
        elif not var in varlist:
            varlist += [var]
            score = 1
             
        if score == 1 and att_score == 0:
            score = 0
    
    # print("node score:", score)
    return score, query, varlist
    
    

# edge format: (var)-[var:label {att_label: att_val}]->(var)
def edge_score(query, varlist):
    score = 0
    
    # regular expression format
    var1_format = "[(](?P<var1>:?.*)[)]"
    var_format = "(?P<var>\w+)?"
    label_format = "(?P<label>(\w|[ ]|:)*\w)"
    # label_format = "(?P<label>(\w|[ ]|:)+)" # label_format = ":(?P<label>\w+)"
    var2_format = "[(](?P<var2>:?.*)[)]"
    attribute_format = "(?P<attributes>[{].+[}])?"
    edge_format = "^" + var1_format + "[ ]?[-][ ]?\["+var_format+label_format+"[ ]{0,3}"+attribute_format+"\][ ]?[-][>][ ]?"+var2_format + "$"
    p = re.compile(edge_format) 
    m = p.search(query)
    # print(query)
    if not m is None:
        # set variables
        var1, var2, var = m.group('var1'), m.group('var2'), m.group('var')
        # print(var1, var2, var)
        label = m.group('label')
        attributes = m.group('attributes')
        
        # Check label
        label = m.group('label')
        if ' ' in label:
            new_label = label.replace(' ', '_')
            idx =  m.start('label')
            new_query = query[:idx] + new_label + query[idx+len(label):]
            # print("replaced: ", query , " -> ", new_query)
            return edge_score(new_query, varlist)
        
        # Check variables
        score1, score2, score3 = 0, 0, 0
        if ':' in var1:
            score1, _, varlist = node_score("("+var1+")", varlist=varlist, check_var=False)
        elif var1 in varlist:
            score1 = 1
        
        if ':' in var2:
            score2, _, varlist = node_score("("+var2+")", varlist=varlist, check_var=False)
        elif var2 in varlist:
            score2 = 1
            
        if var is None:
            score3 = 1
        elif not var in varlist:
            varlist += [var]
            score3 = 1
            
        if score1 + score2 + score3 == 3:
            score = 1
        
        # Check attributes
        if not attributes is None and score == 1: 
            score = attribute_score(attributes, varlist=varlist)
            
    return score, query, varlist # , label if score ==1 else ''


# examples

# scoring(filename="./results/results/result_20230817_12.csv")

s1 = "(a)-[:늘었다 {비율: '8.0%'}]->(:구독자)"
s2 = '(a) -[:늘었다 {비율: "8.0%"}]->(:구독자)'
s3 = "(a)-[:때문에]->(:가능성)"
# print(edge_score(s2, ['a', 'b', 'd']))
# print(edge_score(s3, ['a']))

output1 = """
(a:장마)
(b:평년)
(c:비)
(d:전문가)
(e:기상청)
(f:6월25일)
(g:현재)
(h:전국)
(i:대 부분)
(j:지역)
(k:누 적)
(l:강수 량)
(a)-[:때문 에]->(:가능성)
(d)-[:관 측]->(a)
(e)-[:밝혔다]->(c)
(f)-[:시작된]->(a)
(g)-[:현재까지]->(f)
(h)-[:전국 대부분]->(i)
(i)-[:지역에]->(j)
(j)-[:많은 누적]->(k)
(k)-[:강수량을]->
"""

# outputs = output1.split('\n')
# varlist = []
# for o in outputs:
#     score1, o, varlist = node_score(o, varlist)
#     if score1 == 0:
#         score1, o, varlist = edge_score(o, varlist)
#     print(score1, varlist, o)

