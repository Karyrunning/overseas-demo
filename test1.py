import nltk
from nltk.tokenize import sent_tokenize

str1 ='All work and no play makes jack dull boy. All work and no play makes jack a dull boy.'

def english_phrase(str1):
    list_phrase = []
    phrase = sent_tokenize(str1)
    for p in phrase:
        #进行分词
        tokens = nltk.wordpunct_tokenize(p)
        #寻找双连词短语
        bigram = nltk.bigrams(tokens)
        content = list(bigram)
        for c in content:
            content1 = ' '.join(c)
            list_phrase.append(content1)
    return list_phrase


print(english_phrase(str1))