import pandas as pd
# 数据处理库
import nltk
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os

if not os.path.exists("./图虫"):
        os.mkdir("./图虫")

df = pd.read_csv('./output/Kmeans_data.csv')
df = df.dropna(subset=['new_comment'],axis=0)
f = open('./input/kmeans-fenci.txt', 'w', encoding='utf-8-sig')
for line in tqdm(df['new_comment']):
    tokens = nltk.word_tokenize(line)
    # 计算关键词
    all_words = tokens
    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n' and x != '\n':
            c[x] += 1
    # Top50
    output = ""
    # print('\n词频统计结果：')
    for (k, v) in c.most_common():
        # print("%s:%d"%(k,v))
        output += k + " "

    f.write(output + "\n")

else:
    f.close()

#第一步 计算TFIDF
# 文档预料 空格连接
corpus = []
# 读取预料 一行预料为一个文档
for line in open('./input/kmeans-fenci.txt', 'r',encoding='utf-8-sig').readlines():
    corpus.append(line.strip())
# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()
# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()
# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来 元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()
# 打印特征向量文本内容
print('Features length: ' + str(len(word)))

#第二步 聚类Kmeans

print('Start Kmeans:')

number = 3

clf = KMeans(init='k-means++',n_clusters=number, n_init=10)
print(clf)
pre = clf.fit_predict(weight)
print(pre)

result = pd.concat((df, pd.DataFrame(pre)), axis=1)
result.rename({0: '聚类结果'}, axis=1, inplace=True)
result.to_csv('./output/Kmeans_data.csv',encoding="utf-8-sig",index=None)

# 中心点
print(clf.cluster_centers_)
print(clf.inertia_)

#第三步 图形输出 降维



pca = PCA(n_components=number)  # 输出两维
newData = pca.fit_transform(weight)  # 载入N维

x = [n[0] for n in newData]
y = [n[1] for n in newData]
plt.figure(figsize=(9,6),dpi = 300)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(x, y, c=pre, s=100)
plt.title("词性聚类图")
plt.savefig('./output/词性聚类图.png')
plt.show()