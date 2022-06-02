import pandas as pd
import re
import numpy as np
from tqdm import tqdm
from googletrans import Translator

data = pd.read_csv('./output/new_youtube.csv')


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
    # processed_tweet.append(tweet)
    words = tweet.lower().split()
    words = [w for w in words]
    for word in words:
        word = preprocess_word(word)
        # if is_valid_word(word):
        processed_tweet.append(word)
    if len(processed_tweet) != 0:
        return ' '.join(processed_tweet)
    else:
        return np.NAN


data['comment_text_new'] = data['content']
data['comment_text_new'] = data['comment_text_new'].apply(gettext)
data['comment_text_new'] = data['comment_text_new'].apply(preprocess_word)
data['comment_text_new'] = data['comment_text_new'].apply(clean_text)
data = data.dropna(how='any')
new_data = data.reset_index(drop=True)
new_data.to_csv('./output/new_youtube1.csv',encoding="utf-8-sig",sep=',')


# df1 = pd.DataFrame()
# df1['translate_content'] = ['translate_content']
# df1['translate_language'] = ['translate_language']
# df1.to_csv('./output/store.csv', encoding="utf-8-sig",sep=',',mode='w',header=None,index=None)




