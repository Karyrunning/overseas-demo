import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis.sklearn
import itertools
import numpy as np
import re
from gensim import corpora, models
import matplotlib.pyplot as plt


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
stop_words.extend(new_stop_words)

corpus = []
# 读取预料 一行预料为一个文档
for line in open('./output/C-class-fenci.txt', 'r', encoding='utf-8').readlines():
    corpus.append(line.strip())

dataset=pd.read_csv('./output/sum_youtube.csv')#Reading .csv file for a subcriber from the load file

# 建立词典
word_dict = corpora.Dictionary([[i] for i in dataset['translate_content_new']])  # 正面
# 建立语料库
word_corpus = [word_dict.doc2bow(j) for j in [[i] for i in dataset['translate_content_new']]]  # 正面


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
        lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练
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


#计算主题平均余弦相似度
word_k = lda_k(word_corpus, word_dict)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10,8),dpi=300)
plt.plot(word_k)
plt.title('LDA评论主题数寻优')
plt.xlabel('主题数')
plt.ylabel('平均余弦相似度')
plt.savefig('./output/LDA评论主题数寻优.png')
plt.show()


# -----------------------  第二步 计算TF-IDF值  -----------------------
n_features = 2000
tf_vectorizer = TfidfVectorizer(strip_accents='unicode',
                                max_features=n_features,
                                stop_words=stop_words,
                                max_df=0.99,
                                min_df=0.002)  # 去除文档内出现几率过大或过小的词汇

tf = tf_vectorizer.fit_transform(corpus)
# 设置主题数
n_topics = 3
lda = LatentDirichletAllocation(n_components=n_topics,
                                max_iter=100,
                                learning_method='online',
                                learning_offset=50,
                                random_state=42)
lda.fit(tf)
#
# 显示主题数 model.topic_word_
print(lda.components_)
# # 几个主题就是几行 多少个关键词就是几列
print(lda.components_.shape)
#
# 计算困惑度
print(u'困惑度：')
print(lda.perplexity(tf,sub_sampling=False))

# 主题-关键词分布
def print_top_words(model, tf_feature_names, n_top_words):
    for topic_idx,topic in enumerate(model.components_):  # lda.component相当于model.topic_word_
        print('Topic #%d:' % topic_idx)
        print(' '.join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
        print("")


topic_results = lda.transform(tf)
dataset['Topic'] = topic_results.argmax(axis=1)
dataset.to_csv("./output/sum_youtube_LDA.csv",encoding="utf-8-sig")
# 定义好函数之后 暂定每个主题输出前20个关键词
n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()

# 调用函数
print_top_words(lda, tf_feature_names, n_top_words)
data = pyLDAvis.sklearn.prepare(lda,tf,tf_vectorizer)
pyLDAvis.save_html(data,'./output/lda.html')