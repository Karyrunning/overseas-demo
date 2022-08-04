# -*- coding: utf-8 -*-

import json
import os
import re
import string
import operator
import math
from PIL import Image 

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from langid import classify
import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

from collections import defaultdict,Counter
from wordcloud import WordCloud, ImageColorGenerator

import gensim
from gensim.corpora import Dictionary
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pdtext.tm import topic_words
from sklearn.decomposition import LatentDirichletAllocation

### Draw WordCloud
def WordCloudDraw(df_tfidf,words_range,picture_path,output_pic_path,root_dir,mode,wc_pattern):
    word_cn_list_2 = []
    
    for j in range(0,df_tfidf.shape[0]):
        word_cn = df_tfidf.iloc[j,0]
        if wc_pattern == 'tfidf':
            sub_word_cn_list = [word_cn] * (int(df_tfidf.iloc[j,1]*10000)+1)
        elif wc_pattern == 'count':
            sub_word_cn_list = [word_cn] * int(df_tfidf.iloc[j,1])
        word_cn_list_2.extend(sub_word_cn_list)

    word_counts = Counter(word_cn_list_2)
    print (word_counts)
        
    mask = np.array(Image.open(picture_path))
    wc = WordCloud(
        background_color='white',
        ### the font path should be adjusted for different operating system
        font_path="C:/Windows/Fonts/msyh.ttc",
        mask=mask, 
        max_words=words_range, 
        ### you could customize your output picture here
        max_font_size=64, 
        scale=32,  
        width = 400,
        height = 200,
        color_func = ImageColorGenerator(mask)
    )

    wc.generate_from_frequencies(word_counts)

    

    wc.to_file(output_pic_path) 
    if mode == 'show':
        plt.imshow(wc) 
        plt.axis('off') 
        plt.show() 

### TFIDF or count
def GetTFIDF(list_words,words_range,min_count,wc_pattern):
    doc_frequency=defaultdict(int)
    for word_list in list_words:
        for i in word_list:
            doc_frequency[str(i)]+=1
    word_tf={} 
    word_count = {}
    for i in doc_frequency:
        word_tf[str(i)]=doc_frequency[str(i)]/sum(doc_frequency.values())
        word_count[str(i)]=doc_frequency[str(i)]


    doc_num=len(list_words)
    word_idf={}
    word_doc=defaultdict(int) 
    for i in doc_frequency:
        for j in list_words:
            if i in j:
                word_doc[str(i)]+=1
    for i in doc_frequency:
        word_idf[str(i)]=math.log(doc_num/(word_doc[str(i)]+1))


    word_tf_idf={}
    for i in doc_frequency:
        if doc_frequency[str(i)] <= min_count:
            continue
        word_tf_idf[str(i)]= round(word_tf[str(i)]*word_idf[str(i)],4)

    words_count_dict=sorted(word_count.items(),key=operator.itemgetter(1),reverse=True)[:words_range]
    df_tf = pd.DataFrame(words_count_dict, columns=['word', 'count']) 
    df_tf.to_csv(os.path.join(root_dir,'wordcount_output.csv'),index=False)
    print (df_tf)

    dict_feature_select=sorted(word_tf_idf.items(),key=operator.itemgetter(1),reverse=True)[:words_range]
    df_tfidf = pd.DataFrame(dict_feature_select, columns=['word', 'TFIDF']) 
    df_tfidf.to_csv(os.path.join(root_dir,'tfidf_output.csv'),index=False)
    print (df_tfidf)

    if wc_pattern == 'tfidf':
        return df_tfidf
    elif wc_pattern == 'count':
        return df_tf

### choose words with target part of speech
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
#     elif treebank_tag.startswith('R'):
#         return wordnet.ADV
    else:
        return ''

### process of lemmatization
def merge(words,lmtzr,rejected_words,words_dict):
    words_list = []
    for word in words:
        # if word in rejected_words:
        #     continue
        if word  in words_dict:
            words_list.append(words_dict[word])
            continue
        tag = pos_tag(word_tokenize(word)) # tag is like [('bigger', 'JJR')]

        pos = get_wordnet_pos(tag[0][1])
        if pos:
            lemmatized_word = lmtzr.lemmatize(word, pos)
#                 print ([tag,pos,lemmatized_word])
            if lemmatized_word in rejected_words:
                continue
            words_dict[word] = lemmatized_word
            words_list.append(words_dict[word])
        # else:
        #     words_list.append(word)

    return words_list

### patterns that used to find or/and replace particular chars or words
def replace_abbreviations(text):
    new_text = text
    
    ### to find chars that are not a letter, a blank or a quotation
    pat_letter = re.compile(r'[^a-zA-Z \']+')
    new_text = pat_letter.sub(' ', text).strip().lower()
        
    ### to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
    new_text = pat_is.sub(r"\1 is", new_text)
    
    #### to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])\'s")
    new_text = pat_s.sub("", new_text)
    
    ### to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)\'s?")
    new_text = pat_s2.sub("", new_text)
    
    ### to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n\'t")
    new_text = pat_not.sub(" not", new_text)
    
    ### to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])\'d")
    new_text = pat_would.sub(" would", new_text)
    
    ### to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])\'ll")
    new_text = pat_will.sub(" will", new_text)
    
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])\'m")
    new_text = pat_am.sub(" am", new_text)
    
    ### to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])\'re")
    new_text = pat_are.sub(" are", new_text)
    
    ### to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])\'ve")
    new_text = pat_ve.sub(" have", new_text)
    
    new_text = new_text.replace('\'', ' ')
    
    return new_text


def get_words(text,rejected_words,words_dict):  
    lmtzr = WordNetLemmatizer()
    words_list = (merge(replace_abbreviations(text).split(),lmtzr,rejected_words,words_dict))
    text = ' '.join(words_list)
    return text

def text_prepare(text,rejected_words,not_related_words,words_dict,special_words):
    text = text.lower() 
    special_words_list = []
    for word in special_words:
        if word not in text:
            continue
        print (word, ' has been matched!')
        pattern_special = re.compile(word)
        result_list = pattern_special.findall(text)
        special_words_list.extend(result_list)
        text = re.sub(pattern_special, ' ', text)
    for word in replace_words.keys():
        if word not in text:
            continue
        print ('{} is replaced by {}'.format(word,replace_words[word]))
        text = text.replace(word,replace_words[word])
    ### text primary cleaning    
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@#+,;]') 
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    text = REPLACE_BY_SPACE_RE.sub(' ',text) 
    text = BAD_SYMBOLS_RE.sub(' ',text) 
    remove = str.maketrans('','',string.punctuation) 
    text = text.translate(remove)
    for not_related_word in not_related_words:
        if not_related_word in text.split():
            return []
    text = get_words(text,rejected_words,words_dict)   
    STOPWORDS = set(stopwords.words('english'))
    words = [w for w in replace_abbreviations(text).split() if w not in STOPWORDS and len(w)>1]
    words.extend(special_words_list)
    return words

### LDA model
def LDAModel(texts,num_topics,min_count):
    ### to get CountVectorizer, max_df means you do not the most frequent top 10% words which probably are meaningless
    ### max_features is to select the most frequent 1000 words
    vect = CountVectorizer(min_df=min_count, 
                       max_df=0.9,
                      max_features=1000)
    vect.fit(texts)
    tf = vect.transform(texts)
    ### https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
    lda_model = LatentDirichletAllocation(n_components   = num_topics,
                                        max_iter       = 10,
                                    #   evaluate_every = 5,
                                    #   verbose = 2,
                                    #   n_jobs= 2,
                                     )
    lda_model.fit(tf)
    topic_df = topic_words(lda_model, vect)
    return topic_df

if __name__ == '__main__':
    
    ### path setting
    root_dir = './'
    picture_path = root_dir+'module.jpg'
    output_pic_path = root_dir+'output.png'
    df = pd.read_csv(root_dir+'total_comments_.csv')
    
    setting_json_path = root_dir+'setting.json'

    if os.path.exists(setting_json_path):
        with open(setting_json_path,"r") as load_f:
            setting_dict = json.load(load_f)
            print("loading setting...")
    else:
        print ('please configure the setting!')
        exit()

    ### the name of feature to use text mining
    text_field = setting_dict['text_field']
    ### the speical words will be gotten in priority
    special_words = setting_dict['special_words']
    ### the words to replace, but be careful in mind as you could replace some string in other words!
    replace_words = setting_dict['replace_words']
    ### this shoud differ case by case. 
    ### for pokemon: 'pokemon','poekmonunite','unite','nintendoswitch','game','play','pok','mon'
    rejected_words = setting_dict['rejected_words']
    ### this not_related_words means it is not topic in this context. For instance, age of empirie could be documentary instead of 
    ### the game series, you could use this to filter the text with the same key word but in other context.
    not_related_words = setting_dict['not_related_words']
    ### the number of words to get the final word count dataframe and for wordcloud
    words_range = setting_dict['words_range']
    ### the number of counts to be get into statistics
    min_count = setting_dict['min_count']
    ### the pattern for word cloud, you could choose from tfidf and count
    wc_pattern = setting_dict['wc_pattern']
    ### the number of topics for LDA model
    num_topics = setting_dict['num_topics']
    ### the number of words for LDA model for each topic
    num_words = setting_dict['num_words']

    text_list = df[text_field]

    words_dict = {}
    ### text cleaning
    text_list = [text_prepare(x,rejected_words,not_related_words,words_dict,special_words) for x in text_list]
    text_list = [x for x in text_list if len(x)>0 ]
    # print (text_list[:10])
    print ("the number of texts after primary cleaning: ",len(text_list))
    ### TF-IDF value calculatation
    df_wc = GetTFIDF(text_list,words_range,min_count,wc_pattern)
    ### wordcloud
    WordCloudDraw(df_wc,words_range,picture_path,output_pic_path,root_dir,'show',wc_pattern)

    ### the another version LDA model
    dictionary = Dictionary(text_list)
    corpus = [dictionary.doc2bow(text) for text in text_list]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20) 
    print(ldamodel.print_topics(num_topics=num_topics, num_words=num_words))

    ### LDA model
    topic_df = LDAModel([' '.join(i) for i in text_list],num_topics,min_count)
    print (topic_df)



    