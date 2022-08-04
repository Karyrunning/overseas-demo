import pandas as pd
import nltk
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# df1 = pd.read_csv('./output/new_youtube1.csv',encoding="utf-8-sig")
# df2 = pd.read_csv('./output/store.csv',encoding="utf-8-sig")
df1 = pd.read_csv('Apex_Mobile - Jun 29, 2022 - 10 29 45 AM.csv', encoding="UTF-16",sep='\t')
sid = SentimentIntensityAnalyzer()
sum_counts = 0
text_list = []

# df1['translate_content_new'] = list(df2['translate_content'].values)
# df1['translate_language_new'] = list(df2['translate_language'].values)
# df1 = df1.drop(['Unnamed: 0','comment_text_new_number'],axis=1)
df1 = df1.dropna(subset=['Headline'],axis=0)
# f = open('./output/C-class-fenci.txt', 'w', encoding='utf-8')
# for line in df1['translate_content_new']:
#     tokens = nltk.word_tokenize(line)
#     # 计算关键词
#     all_words = tokens
#     c = Counter()
#     for x in all_words:
#         if len(x) > 1 and x != '\r\n':
#             c[x] += 1
#     # Top50
#     output = ""
#     # print('\n词频统计结果：')
#     for (k, v) in c.most_common():
#         # print("%s:%d"%(k,v))
#         output += k + " "
#
#     f.write(output + "\n")
#
# else:
#     f.close()


def emotional_judgment(x):
    neg = x['neg']
    neu = x['neu']
    pos = x['pos']
    compound = x['compound']
    if compound == 0 and neg == 0 and pos == 0 and neu == 1:
        return 'neu'
    if compound > 0:
        if pos > neg:
            return 'pos'
        else:
            return 'neg'
    elif compound < 0:
        if pos < neg:
            return 'neg'
        else:
            return 'pos'


df1['scores'] = df1['Headline'].apply(lambda commentText: sid.polarity_scores(commentText))
df1['compound'] = df1['scores'].apply(lambda score_dict: score_dict['compound'])
df1['Negtive'] = df1['scores'].apply(lambda score_dict: score_dict['neg'])
df1['Postive'] = df1['scores'].apply(lambda score_dict: score_dict['pos'])
df1['Neutral'] = df1['scores'].apply(lambda score_dict: score_dict['neu'])
df1['comp_score'] = df1['scores'].apply(emotional_judgment)

df1.to_csv('sum_comment.csv',encoding="utf-8-sig")



