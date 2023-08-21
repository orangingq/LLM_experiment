#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json
from gensim.summarization.summarizer import summarize as gensim_summarize

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
        total_len = len(articles)
        cycle = int(total_len/500)
        
    for itr in range(cycle+1):
        with open(filename, 'r', encoding='utf-8') as file:
            articles = json.load(file)
            for i, data in enumerate(articles[itr*500: min(total_len, (itr+1)*500)]):
                article = data['article']
                print(f"article {i}) start: {data['line_start']}, end: {data['line_end']}, length: {len(article)}") #, summaryCnt: {data['summaryCount']}

                # add 'summary' (from_clova=True) or 'text_rank' (from_clova=False)
                # if not 'summary' in data or not 'text_rank' in data:                    
                data = get_summary(data, from_clova=False)         
                
                # add 'article_num'
                if not 'article_num' in data:
                    data['article_num'] = i
                    
                articles[i] = data
                
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(articles, file, ensure_ascii=False, indent="\t")
        
    print("summarize done: ", filename)
    return


# get summary from clova or attention mechanism
def get_summary(data, from_clova=False):
    if from_clova:
        lines = clova_summary(data['article'])
        data['summary'] = []
        for l in lines:
            print(l)
            data['summary'].append(l)
        # return data
        
    # page_rank algorithm
    else:
        data = TextRank(data)
    
    # add numbering to the summarized sentences
    return sentenceNumbering(data, from_clova=from_clova)
    
    
def clova_summary(article):
    send_data = {
    "document": { "content": article  },
    "option": {
        "language": "ko",
        "model": "news",
        "tone": 0,
        "summaryCount": min(max(round(len(article)/170), 3), 10) # 3 ~ 10 사이 #summary_count(article)
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(send_data).encode('UTF-8'))
    rescode = response.status_code
    if(rescode == 200):
        summ_st = 12    # {"summary":"
        summ_end = -2   # "}
        line_sp = '\\n'
        lines = response.text[summ_st:summ_end].split(line_sp)
        return lines
    else:
        raise ConnectionAbortedError("Error : " + response.text)


# add 'summaryCountNum' (from_clova=True) or 'textrankCountNum' (from_clova=False)
def sentenceNumbering(data, from_clova=True):
    article_arr = data['article']
    sentenceNum = len(article_arr)

    i = 0
    if from_clova:
        summary = data['summary']
    else:
        summary = data['text_rank']
    summary_cnt = [-1 for _ in range(len(summary))]
    for j, s in enumerate(summary):
        while i < sentenceNum:
            if s.replace(' ', '') in article_arr[i].replace(' ', ''):
                summary_cnt[j] = i
                break
            i += 1
    
    if -1 in summary_cnt:
        print(data)
        
    if from_clova:
        data['summaryCountNum'] = summary_cnt
    else:
        data['textrankCountNum'] = summary_cnt
    
    return data


def TextRank(data):
    article = data['article']
    data['text_rank'] = gensim_summarize(' \n'.join(article), ratio=0.3).split('\n')
    return data
        

summarize('inputs/articles/articles_2980to19991.json')
summarize('inputs/articles/articles_982to2979.json')
summarize('inputs/articles/articles_297to981.json')



    
# import tensorflow as tf
# from tensorflow.keras.layers import Input, LSTM, Dense, Attention, Concatenate, Embedding
# from tensorflow.keras.models import Model
# from tensorflow.keras.callbacks import EarlyStopping # , ModelCheckpoint
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# def attention_summary_train(filename):
     
#     # 가정: vocab_size는 단어의 수, embedding_dim은 임베딩 차원, hidden_size는 LSTM 유닛의 수
#     vocab_size = 10000
#     embedding_dim = 128 #256
#     hidden_size = 256 #512
    
#     with open(filename, 'r', encoding='utf-8') as file:
#         articles = json.load(file)
#         n_of_val = int(len(articles)*0.2)
#         encoder_input = np.array([''.join(a['article']).replace('.', ' ') for a in articles])
#         decoder_input = np.array(['sostoken '+''.join(a['summary']).replace('.', '') for a in articles])
#         decoder_target = np.array([''.join(a['summary']).replace('.', '')+' eostoken' for a in articles])
        
#         # print(encoder_input[0])
#         # print(decoder_input[0])
#         # print(decoder_target[0])
        
    
#     # shuffle
#     indices = np.arange(encoder_input.shape[0])
#     np.random.shuffle(indices)
#     encoder_input = encoder_input[indices]
#     decoder_input = decoder_input[indices]
#     decoder_target = decoder_target[indices]
    
#     # train set
#     encoder_input_train = encoder_input[:-n_of_val]
#     decoder_input_train = decoder_input[:-n_of_val]
#     decoder_target_train = decoder_target[:-n_of_val]

#     # test set
#     encoder_input_test = encoder_input[-n_of_val:]
#     decoder_input_test = decoder_input[-n_of_val:]
#     decoder_target_test = decoder_target[-n_of_val:]
    
#     print('훈련 데이터의 개수 :', len(encoder_input_train))
#     print('훈련 레이블의 개수 :',len(decoder_input_train))
#     print('테스트 데이터의 개수 :',len(encoder_input_test))
#     print('테스트 레이블의 개수 :',len(decoder_input_test))
    
#     # Input Tokenizer
#     src_tokenizer = Tokenizer(num_words = vocab_size) 
#     src_tokenizer.fit_on_texts(encoder_input_train)

#     # 텍스트 시퀀스를 정수 시퀀스로 변환
#     encoder_input_train = src_tokenizer.texts_to_sequences(encoder_input_train) 
#     encoder_input_test = src_tokenizer.texts_to_sequences(encoder_input_test)
#     # print(encoder_input_train[:3])
    
#     # target Tokenizer
#     tar_vocab = 2000
#     tar_tokenizer = Tokenizer(num_words = tar_vocab) 
#     tar_tokenizer.fit_on_texts(decoder_input_train)
#     tar_tokenizer.fit_on_texts(decoder_target_train)
    
#     # 텍스트 시퀀스를 정수 시퀀스로 변환
#     decoder_input_train = tar_tokenizer.texts_to_sequences(decoder_input_train) 
#     decoder_target_train = tar_tokenizer.texts_to_sequences(decoder_target_train)
#     decoder_input_test = tar_tokenizer.texts_to_sequences(decoder_input_test)
#     decoder_target_test = tar_tokenizer.texts_to_sequences(decoder_target_test)
#     # print(decoder_input_train[:5])
    
#     drop_train = [index for index, sentence in enumerate(decoder_input_train) if len(sentence) == 1]
#     drop_test = [index for index, sentence in enumerate(decoder_input_test) if len(sentence) == 1]
#     print("drop:", drop_train, drop_test)
    
#     if len(drop_train) >0:
#         encoder_input_train = np.delete(encoder_input_train, drop_train, axis=0)
#         decoder_input_train = np.delete(decoder_input_train, drop_train, axis=0)
#         decoder_target_train = np.delete(decoder_target_train, drop_train, axis=0)
#     if len(drop_test) > 0:
#         encoder_input_test = np.delete(encoder_input_test, drop_test, axis=0)
#         decoder_input_test = np.delete(decoder_input_test, drop_test, axis=0)
#         decoder_target_test = np.delete(decoder_target_test, drop_test, axis=0)

#     print('훈련 데이터의 개수 :', len(encoder_input_train))
#     print('훈련 레이블의 개수 :',len(decoder_input_train))
#     print('테스트 데이터의 개수 :',len(encoder_input_test))
#     print('테스트 레이블의 개수 :',len(decoder_input_test))
    
#     text_maxlen = 2000
#     summary_maxlen = 1000
#     encoder_input_train = pad_sequences(encoder_input_train, maxlen = text_maxlen, padding='post')
#     encoder_input_test = pad_sequences(encoder_input_test, maxlen = text_maxlen, padding='post')
#     decoder_input_train = pad_sequences(decoder_input_train, maxlen = summary_maxlen, padding='post')
#     decoder_target_train = pad_sequences(decoder_target_train, maxlen = summary_maxlen, padding='post')
#     decoder_input_test = pad_sequences(decoder_input_test, maxlen = summary_maxlen, padding='post')
#     decoder_target_test = pad_sequences(decoder_target_test, maxlen = summary_maxlen, padding='post')
    
#     # Encoder
#     encoder_inputs = Input(shape=(None,))
#     encoder_emb = Embedding(vocab_size, embedding_dim)(encoder_inputs)
    
#     # encoder LSTM 1
#     encoder_lstm1 = LSTM(hidden_size, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
#     encoder_outputs1, _, _ = encoder_lstm1(encoder_emb)
    
#     # encoder LSTM 2
#     encoder_lstm2 = LSTM(hidden_size, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
#     encoder_outputs2, _, _ = encoder_lstm2(encoder_outputs1)
    
#     # # encoder LSTM 3
#     encoder_lstm3 = LSTM(hidden_size, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
#     encoder_outputs, state_h, state_c = encoder_lstm3(encoder_outputs2)
#     encoder_states = [state_h, state_c]

#     # Decoder
#     decoder_inputs = Input(shape=(None,))
#     decoder_embedding = Embedding(vocab_size, embedding_dim)
#     dec_emb = decoder_embedding(decoder_inputs)

#     # Decoder LSTM
#     decoder_lstm = LSTM(hidden_size, return_sequences=True, return_state=True, dropout = 0.4, recurrent_dropout=0.2)
#     decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)

#     # # Attention Mechanism
#     attention = Attention()
#     context_vector = attention([decoder_outputs, encoder_outputs])
#     decoder_concat = Concatenate(axis=-1)([decoder_outputs, context_vector])

#     # Decoder Output
#     decoder_softmax_layer = Dense(vocab_size, activation='softmax')
#     decoder_outputs = decoder_softmax_layer(decoder_concat) #decoder_outputs)

#     # Model
#     model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
#     # model.summary()
    
#     model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')

#     es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience = 2)
#     history = model.fit(x = [encoder_input_train, decoder_input_train], y = decoder_target_train, 
#           validation_data = ([encoder_input_test, decoder_input_test], decoder_target_test),
#           batch_size = 256, callbacks=[es], epochs = 50)
    
#     plt.plot(history.history['loss'], label='train')
#     plt.plot(history.history['val_loss'], label='test')
#     plt.legend()
#     plt.show()


# attention_summary_train('inputs/articles/articles_982to2979.json')