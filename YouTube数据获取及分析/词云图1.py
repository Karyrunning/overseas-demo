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

new_stop_words = []
with open("新增停用词补充.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        new_stop_words.append(line.strip())

def main1():
    # 绘制词云图
    df = pd.read_csv('./output/new_BP-评论数据.csv')

    def get_cut_words(x):
        data = pd.read_csv('./output/bp情感分析.csv')
        d = {}
        for number, url in zip(data['Unnamed: 0'], data['视频链接']):
            d[url] = number
        df1 = x
        name = [d for d in df1['视频链接']][0]

        name1 = d[name]

        comment = df1.comment_text_new
        str1 = " ".join(i for i in comment)
        tokens = [word.lower() for sent in nltk.sent_tokenize(str1) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # 过滤所有不含字母的词例（例如：数字、纯标点）
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                if token not in new_stop_words:
                    filtered_tokens.append(token)

        stylecloud.gen_stylecloud(text=','.join(filtered_tokens), max_words=100,
                                  collocations=False,
                                  font_path='simhei.ttf',
                                  icon_name='fas fa-cannabis',
                                  size=500,
                                  # palette='matplotlib.Inferno_9',
                                  output_name='./output/BP词云/{}.png'.format(name1))
        Image(filename='./output/BP词云/{}.png'.format(name1))

    new_df = df.groupby('视频链接').apply(get_cut_words)


def main2():
    # 绘制词云图
    df = pd.read_csv('./output/new_luckdraw-评论数据.csv')

    def get_cut_words(x):
        data = pd.read_csv('./output/luckdraw情感分析.csv')
        d = {}
        for number, url in zip(data['Unnamed: 0'], data['视频链接']):
            d[url] = number
        df1 = x
        name = [d for d in df1['视频链接']][0]

        name1 = d[name]

        comment = df1.comment_text_new
        str1 = " ".join(i for i in comment)
        tokens = [word.lower() for sent in nltk.sent_tokenize(str1) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # 过滤所有不含字母的词例（例如：数字、纯标点）
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                if token not in new_stop_words:
                    filtered_tokens.append(token)

        stylecloud.gen_stylecloud(text=','.join(filtered_tokens), max_words=100,
                                  collocations=False,
                                  font_path='simhei.ttf',
                                  icon_name='fas fa-certificate',
                                  size=500,
                                  # palette='matplotlib.Inferno_9',
                                  output_name='./output/luckydraw词云/{}.png'.format(name1))
        Image(filename='./output/luckydraw词云/{}.png'.format(name1))

    new_df = df.groupby('视频链接').apply(get_cut_words)


if __name__ == '__main__':
    main1()
    main2()

