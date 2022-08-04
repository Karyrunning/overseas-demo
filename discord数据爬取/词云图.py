import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from imageio import imread
import nltk
import re
from nltk.stem.snowball import SnowballStemmer  # 返回词语的原型，去掉ing等
import stylecloud
from IPython.display import Image

stemmer = SnowballStemmer("english")

stop_words = []
with open("常用英文停用词(NLP处理英文必备)stopwords.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        stop_words.append(line.strip())

# with open("新增停用词补充.txt", 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for line in lines:
#         stop_words.append(line.strip())

def main1():
    # 绘制词云图
    df = pd.read_csv('./output/new_data.csv')
    df = df.dropna(subset=['new_comment'],axis=0)
    comment = df.new_comment
    str1 = " ".join(i for i in comment)
    tokens = [word.lower() for sent in nltk.sent_tokenize(str1) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # 过滤所有不含字母的词例（例如：数字、纯标点）
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in stop_words:
                filtered_tokens.append(stemmer.stem(token))
    d = {}
    for f in filtered_tokens:
        d[f] = d.get(f,0)+1

    ls = list(d.items())
    ls.sort(key=lambda x:x[1],reverse=True)
    list_word = []
    list_count = []
    for key,values in ls[0:200]:
        list_word.append(key)
        list_count.append(values)
    data = pd.DataFrame()
    data['word'] = list_word
    data['counts'] = list_count
    data.to_csv('./output/高频词.csv',encoding='utf-8-sig')
    stylecloud.gen_stylecloud(text=','.join(filtered_tokens), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-cannabis',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./output/{}.png'.format(name1))
    Image(filename='./output/{}.png'.format(name1))


def main2(number):
    # 绘制词云图
    df = pd.read_csv('./output/Kmeans_data.csv')
    df = df.dropna(subset=['new_comment'],axis=0)
    df = df[df['聚类结果'] == number]
    comment = df.new_comment
    str1 = " ".join(i for i in comment)
    tokens = [word.lower() for sent in nltk.sent_tokenize(str1) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # 过滤所有不含字母的词例（例如：数字、纯标点）
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in new_stop_words:
                filtered_tokens.append(stemmer.stem(token))
    d = {}
    for f in filtered_tokens:
        d[f] = d.get(f,0)+1

    ls = list(d.items())
    ls.sort(key=lambda x:x[1],reverse=True)
    list_word = []
    list_count = []
    for key,values in ls:
        list_word.append(key)
        list_count.append(values)
    data = pd.DataFrame()
    data['word'] = list_word
    data['counts'] = list_count
    data.to_csv('./output/{}-高频词.csv'.format(name1),encoding='utf-8-sig')
    stylecloud.gen_stylecloud(text=','.join(filtered_tokens), max_words=100,
                              collocations=False,
                              font_path='simhei.ttf',
                              icon_name='fas fa-cannabis',
                              size=500,
                              # palette='matplotlib.Inferno_9',
                              output_name='./output/{}.png'.format(name1))
    Image(filename='./output/{}.png'.format(name1))


if __name__ == '__main__':
    name1 = '高频词'
    # main2(2)
    main1()


