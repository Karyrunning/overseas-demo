import pandas as pd
# 数据处理库
import re
from gensim import corpora, models
import matplotlib.pyplot as plt
import numpy as np
import itertools

def lda_tfidf():
    df = pd.read_csv('./output/new_data.csv')
    df = df.dropna(subset=['new_comment'], axis=0)
    fr = open('./input/kmeans-fenci.txt', 'r', encoding='utf-8')
    train = []

    for line in fr.readlines():
        line = [word for word in line.split(' ') if word != '\n']
        train.append(line)

    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]

    # 构造主题数寻优函数
    def cos(vector1, vector2):  # 余弦相似度函数
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return (None)
        else:
            return (dot_product / ((normA * normB) ** 0.5))

        # 主题数寻优

    def lda_k(x_corpus, x_dict):
        # 初始化平均余弦相似度
        mean_similarity = []
        mean_similarity.append(1)

        # 循环生成主题并计算主题间相似度
        for i in np.arange(2, 11):
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict,passes=50)  # LDA模型训练
            for j in np.arange(i):
                term = lda.show_topics(num_words=50)
            # 提取各主题词
            top_word = []
            for k in np.arange(i):

                top_word.append([''.join(re.findall('"(.*)"', i)) \
                                 for i in term[k][1].split('+')])  # 列出所有词

            # 构造词频向量
            word = sum(top_word, [])  # 列出所有的词
            unique_word = set(word)  # 去除重复的词

            # 构造主题词列表，行表示主题号，列表示各主题词
            mat = []
            for j in np.arange(i):
                top_w = top_word[j]
                mat.append(tuple([top_w.count(k) for k in unique_word]))

            p = list(itertools.permutations(list(np.arange(i)), 2))
            l = len(p)
            top_similarity = [0]
            for w in np.arange(l):
                vector1 = mat[p[w][0]]
                vector2 = mat[p[w][1]]
                top_similarity.append(cos(vector1, vector2))

            # 计算平均余弦相似度
            mean_similarity.append(sum(top_similarity) / l)
        return (mean_similarity)

    # 计算主题平均余弦相似度
    word_k = lda_k(corpus, dictionary)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 8), dpi=300)
    plt.plot(word_k)
    plt.title('LDA评论主题数寻优')
    plt.xlabel('主题数')
    plt.ylabel('平均余弦相似度')
    plt.savefig('./output/LDA评论主题数寻优.png')
    plt.show()

    topic_lda = word_k.index(min(word_k)) + 1
    print(topic_lda)
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)

    list3 = []
    list2 = []
    for i in lda.get_document_topics(corpus)[:]:
        listj = []
        list1 = []
        for j in i:
            list1.append(j)
            listj.append(j[1])
        list3.append(list1)
        bz = listj.index(max(listj))
        # print(i[bz][0])
        list2.append(i[bz][0])

    df['主题类型'] = list2
    df.to_csv('./output/lda_data.csv',encoding='utf-8-sig',index=None)


if __name__ == '__main__':
    lda_tfidf()
