#coding: utf-8
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

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

results=[]
dataset=pd.read_csv('./output/sum_youtube.csv')#Reading .csv file for a subcriber from the load file
cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')# Assign the value for max and min allowance stopwords
dtm = cv.fit_transform(dataset['translate_content_new'])# Transforming commentText to tfdif formula
LDA = LatentDirichletAllocation(n_components=3,random_state=42)#Assigning number of topics
LDA.fit(dtm)

for index,topic in enumerate(LDA.components_):
    print(f'THE TOP 15 WORDS FOR TOPIC #{index}')
    result=([cv.get_feature_names()[i] for i in topic.argsort()[-10:]])
    results.append(result)
    print('\n')

topic_results = LDA.transform(dtm)
dataset['Topic'] = topic_results.argmax(axis=1)
dataset.to_csv("./output/sum_youtube_LDA.csv",encoding="utf-8-sig")


# -----------------------  第二步 计算TF-IDF值  -----------------------
n_features = 2000

tf_vectorizer = TfidfVectorizer(strip_accents='unicode',
                                max_features=n_features,
                                stop_words=stop_words,
                                max_df=0.99,
                                min_df=0.002)  # 去除文档内出现几率过大或过小的词汇

tf = tf_vectorizer.fit_transform(corpus)

# # 设置主题数
# n_topics = 3
# lda = LatentDirichletAllocation(n_components=n_topics,
#                                 max_iter=100,
#                                 learning_method='online',
#                                 learning_offset=50,
#                                 random_state=42)
LDA.fit(tf)

# 显示主题数 model.topic_word_
print(LDA.components_)
# 几个主题就是几行 多少个关键词就是几列
print(LDA.components_.shape)

# 计算困惑度
print(u'困惑度：')
print(LDA.perplexity(tf,sub_sampling = False))


# 主题-关键词分布
def print_top_words(model, tf_feature_names, n_top_words):
    for topic_idx,topic in enumerate(model.components_):  # lda.component相当于model.topic_word_
        print('Topic #%d:' % topic_idx)
        print(' '.join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
        print("")

# 定义好函数之后 暂定每个主题输出前20个关键词
n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()

# 调用函数
print_top_words(LDA, tf_feature_names, n_top_words)
data = pyLDAvis.sklearn.prepare(LDA,tf,tf_vectorizer)
print(data)
pyLDAvis.save_html(data,'./output/lda.html')