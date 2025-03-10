import pandas as pd
import re
import numpy as np
from tqdm import tqdm
import time
# from nltk.stem.snowball import SnowballStemmer  # 返回词语的原型，去掉ing等
# stemmer = SnowballStemmer("english")

data = pd.read_csv('./output/清洗过后的数据.csv')

stop_words = []
with open('常用英文停用词(NLP处理英文必备)stopwords.txt','r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        stop_words.append(line.strip().replace("'",""))


def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def gettext(x):
    import string
    punc = string.punctuation
    for ch in punc:
        txt = str(x).replace(ch,"")
    return txt


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' ', tweet)
    tweet = re.sub(r'#GTCartoon:', ' ', tweet)
    return tweet





def clean_text(tweet):
    processed_tweet = []
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' ', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', ' ', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', ' ', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', ' ', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with either EMO_POS or EMO_NEG
    tweet = handle_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    # 去掉数字
    tweet = re.sub(r'\d+', ' ', tweet)
    # 标点符号
    tweet = re.sub(r'[^A-Z^a-z^0-9^]', ' ', tweet)
    # processed_tweet.append(tweet)
    words = tweet.lower().split()
    words = [w for w in words if w not in stop_words]
    for word in words:
        # word = preprocess_word(stemmer.stem(word))
        # if is_valid_word(word):
        processed_tweet.append(word)
    if len(processed_tweet) != 0:
        return ' '.join(processed_tweet)
    else:
        return np.NAN


data['new_comment'] = data['内容信息']
data['new_comment'] = data['new_comment'].apply(gettext)
data['new_comment'] = data['new_comment'].apply(preprocess_word)
data['new_comment'] = data['new_comment'].apply(clean_text)
 # data = data.dropna(how='any')
# new_data = data.reset_index(drop=True)
data.to_csv('./output/new_data.csv',encoding="utf-8-sig",sep=',',index=None)