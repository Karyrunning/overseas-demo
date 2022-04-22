import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from imageio import imread
import nltk
import re
from nltk.stem.snowball import SnowballStemmer  # 返回词语的原型，去掉ing等
stemmer = SnowballStemmer("english")



stop_words = []
with open("常用英文停用词(NLP处理英文必备)stopwords.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        stop_words.append(line.strip())

new_stop_words = []
with open("新增停用词补充.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        new_stop_words.append(line.strip())


def tokenize_only(text):  # 分词器，仅分词
    # 首先分句，接着分词，而标点也会作为词例存在
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # 过滤所有不含字母的词例（例如：数字、纯标点）
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def main1():
    # 绘制词云图
    df = pd.read_csv('./output/sum_youtube.csv')
    sum_cotent = []
    df.to_csv('./output/词云总表.csv')
    df['translate_content_new'] = df['translate_content_new'].apply(tokenize_only)
    df['translate_content_new'].astype('str')

    stop_words.extend(new_stop_words)

    y_data1 = list(df['translate_content_new'])
    for d in y_data1:
        for i in d:
            if i not in stop_words:
                sum_cotent.append(i)


    counts = {}
    for s in sum_cotent:
        counts[s] = counts.get(s,0)+1
    ls = list(counts.items())
    ls.sort(key=lambda x:x[1],reverse=True)
    x_data = []
    y_data = []
    for key,values in ls[:200]:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data
    df1['counts'] = y_data
    df1.to_csv('./output/高频词(总).csv',encoding='utf-8-sig')

    contents_list = " ".join(sum_cotent)

    # 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
    wc = WordCloud(
        collocations=False,
        max_words=100,
        background_color="white",
        font_path=r"C:\Windows\Fonts\simhei.ttf",
        stopwords=stop_words,
        width=1080, height=1920, random_state=42,
        mask=imread('./input/1.png', pilmode="RGB"))
    wc.generate(contents_list)
    # 要读取的形状的图片
    wc.to_file("./output/热词-云图.png")



def main2():
    # 绘制词云图
    sum_cotent = []
    df = pd.read_csv('./output/sum_youtube.csv')
    df1 = df[df['comp_score'] == 'pos']
    df1.to_csv('./output/正向总表.csv')
    df1['translate_content_new'] = df1['translate_content_new'].apply(tokenize_only)
    df1['translate_content_new'].astype('str')

    stop_words.extend(new_stop_words)

    y_data1 = list(df1['translate_content_new'])
    for d in y_data1:
        for i in d:
            if i not in stop_words:
                sum_cotent.append(i)


    counts = {}
    for s in sum_cotent:
        counts[s] = counts.get(s, 0) + 1
    ls = list(counts.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls[:200]:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data
    df1['counts'] = y_data
    df1.to_csv('./output/高频词(正向).csv', encoding='utf-8-sig')


    contents_list = " ".join(sum_cotent)
    # 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
    wc = WordCloud(stopwords=STOPWORDS.add("一个"),
                   collocations=False,
                   max_words=100,
                   background_color="white",
                   font_path=r"C:\Windows\Fonts\simhei.ttf",
                   width=1080, height=1920, random_state=42,
                   mask=imread('./input/2.jpg', pilmode="RGB"))
    wc.generate(contents_list)
    # 要读取的形状的图片
    wc.to_file("./output/pos-云图.jpg")



def main3():
    # 绘制词云图
    sum_cotent = []
    df = pd.read_csv('./output/sum_youtube.csv')
    df1 = df[df['comp_score'] == 'neg']
    df1.to_csv('./output/负向总表.csv')
    df1['translate_content_new'] = df1['translate_content_new'].apply(tokenize_only)
    df1['translate_content_new'].astype('str')

    stop_words.extend(new_stop_words)

    y_data1 = list(df1['translate_content_new'])
    for d in y_data1:
        for i in d:
            if i not in stop_words:
                sum_cotent.append(i)

    counts = {}
    for s in sum_cotent:
        counts[s] = counts.get(s, 0) + 1
    ls = list(counts.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls[:200]:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data
    df1['counts'] = y_data
    df1.to_csv('./output/高频词(负向).csv', encoding='utf-8-sig')

    contents_list = " ".join(sum_cotent)
    # 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
    wc = WordCloud(stopwords=STOPWORDS.add("一个"),
                   collocations=False,
                   max_words=100,
                   background_color="white",
                   font_path=r"C:\Windows\Fonts\simhei.ttf",
                   width=1080, height=1920, random_state=42,
                   mask=imread('./input/3.png', pilmode="RGB"))
    wc.generate(contents_list)
    # 要读取的形状的图片
    wc.to_file("./output/neg-云图.png")


def main4():
    # 绘制词云图
    sum_cotent = []
    df = pd.read_csv('./output/sum_youtube.csv')
    df1 = df[df['comp_score'] == 'neu']
    df1.to_csv('./output/中立总表.csv')
    df1['translate_content_new'] = df1['translate_content_new'].apply(tokenize_only)
    df1['translate_content_new'].astype('str')

    stop_words.extend(new_stop_words)

    y_data1 = list(df1['translate_content_new'])
    for d in y_data1:
        for i in d:
            if i not in stop_words:
                sum_cotent.append(i)

    counts = {}
    for s in sum_cotent:
        counts[s] = counts.get(s, 0) + 1
    ls = list(counts.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    x_data = []
    y_data = []
    for key, values in ls[:200]:
        x_data.append(key)
        y_data.append(values)

    df1 = pd.DataFrame()
    df1['word'] = x_data
    df1['counts'] = y_data
    df1.to_csv('./output/高频词(中立).csv', encoding='utf-8-sig')

    contents_list = " ".join(sum_cotent)
    # 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
    wc = WordCloud(stopwords=STOPWORDS.add("一个"),
                   collocations=False,
                   max_words=100,
                   background_color="white",
                   font_path=r"C:\Windows\Fonts\simhei.ttf",
                   width=1080, height=1920, random_state=42,
                   mask=imread('./input/1.png', pilmode="RGB"))
    wc.generate(contents_list)
    # 要读取的形状的图片
    wc.to_file("./output/neu-云图.png")


if __name__ == '__main__':
    main1()
    main2()
    main3()
    main4()

