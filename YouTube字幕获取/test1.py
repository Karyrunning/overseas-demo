import re
import os
bad_words = ['-->','</c>']

name = os.listdir('data')

for n in name:
    with open('./data/{}'.format(n)) as oldfile, open('./newtxt/new_{}.txt'.format(n), 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                newfile.write(line)


    with open('./newtxt/new_{}.txt'.format(n)) as result:
        uniqlines = set(result.readlines())
        with open('./output/sub_{}.txt'.format(n), 'w') as rmdup:
            mylst = map(lambda each: each.strip("&gt;&gt;"), uniqlines)
            mylst = map(lambda each: each.strip("WEBVTT"), mylst)
            mylst = map(lambda each: each.strip("Kind: captions"), mylst)
            mylst = map(lambda each: each.strip("Language: en"), mylst)
            mylst = map(lambda each: each.strip(" "), mylst)
            # mylst = map(lambda each: each.strip("\n"), mylst)
            print(mylst)
            rmdup.writelines(set(mylst))