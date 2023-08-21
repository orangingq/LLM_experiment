#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json

# setting path
sys.path.append('../LLM_experiment')
from inputs.clova_summary import summarize


def article_parser(start_limit=297, end_limit = 500):
    # global parameters & data
    filename = '/mnt/disk1/data/news1719-all-context.txt'
    articles = []
    f = open(filename, 'r')

    # iteration parameters
    line_cnt = 0
    start_limit = max(start_limit, 297)
    article_start = start_limit # starting line of the article
    article_end = start_limit
    start = 0 # 0: ready to start / 1: adding lines
    article = ""
    article_num = 0
    
    # iterate
    while line_cnt <= end_limit:
        # read
        line = f.readline()
        
        # finish reading
        if line_cnt < start_limit: # pass the first long~~~~ interview
            line_cnt += 1
            continue
        if not line:  # end of the file
            break
        # print(line_cnt, line)
        
        if line == '\n':
            if start == 1:
                if len(article) > 0 and len(article) < 2000: # 2000자 이내
                    article_end = line_cnt-1
                    article_arr = sentence_tokenize(article) 
                    data = {"line_start": article_start, "line_end": article_end, "article": article_arr, "article_num":article_num}
                    articles.append(data)
                    article_num += 1
                    # print(data)
                start = 0
        elif start == 0:
            article_start = line_cnt
            article = line
            start = 1
        elif start == 1:
            article += line
        
        line_cnt += 1
    f.close()

    # save
    savefilename = 'inputs/articles/articles_'+str(start_limit)+ 'to'+ str(article_end) +'.json'
    with open(savefilename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent="\t")

    print(f"start: {start_limit}\tend: {end_limit}\ttotal: {len(articles)} articles")
    # add summary
    summarize(filename=savefilename)
    
    print("file saved: ", savefilename)
    return

import re 
def sentence_tokenize(article):
    splitted = re.split(r'(?<=[.!?])\s+', article)

    article_arr = []
    memory = ''
    for s in splitted:
        if len(s) < 2:
            continue
        else:
            if s[-2].isnumeric():
                memory += s
            else:
                article_arr += [memory + s.strip()]
                memory = ''
    
    return article_arr

article_parser(start_limit=2980, end_limit=20000)