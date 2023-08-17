#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json

# setting path
sys.path.append('../LLM_experiment')
from keys.keys import clova_id, clova_secret

url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-APIGW-API-KEY-ID': clova_id,
            'X-NCP-APIGW-API-KEY': clova_secret
        }

def summarize(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        articles = json.load(file)

        for i, data in enumerate(articles):
            article = data['article']
            data['summaryCount'] = min(max(round(len(article)/170), 3), 10) # 3 ~ 10 사이
            print(f"article {i}) start: {data['line_start']}, end: {data['line_end']}, length: {len(article)}, summaryCnt: {data['summaryCount']}")

            send_data = {
            "document": { "content": article  },
            "option": {
                "language": "ko",
                "model": "news",
                "tone": 0,
                "summaryCount": data['summaryCount'] 
                }
            }

            response = requests.post(url, headers=headers, data=json.dumps(send_data).encode('UTF-8'))
            rescode = response.status_code
            if(rescode == 200):
                summ_st = 12    # {"summary":"
                summ_end = -2   # "}
                line_sp = '\\n'
                # print(response.text[12:-2])
                lines = response.text[summ_st:summ_end].split(line_sp)
                data['summary'] = []
                for l in lines:
                    print(l)
                    data['summary'].append(l)
                
                articles[i] = data
                # print(articles[i])
            else:
                print("Error : " + response.text)
                
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent="\t")
        
    print("summarize done: ", filename)
    return

summarize('inputs/articles/articles_297to492.json')