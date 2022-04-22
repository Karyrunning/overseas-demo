import pandas as pd
from tqdm import tqdm
from googletrans import Translator
import time
data = pd.read_csv('./output/new_youtube1.csv',encoding="utf-8-sig",sep=',')


# df1 = pd.DataFrame()
# df1['translate_content'] = ['translate_content']
# df1['translate_language'] = ['translate_language']
# df1.to_csv('./output/store.csv', encoding="utf-8-sig",sep=',',mode='w',header=None,index=None)

translator = Translator()
df1 = pd.DataFrame()
for d in tqdm(data['comment_text_new']):
    try:
        translations = translator.translate(d, dest='en')
        df1['translate_content'] = [translations.text]
        df1['translate_language'] = [translations.src]
        df1.to_csv('./output/store.csv', encoding="utf-8-sig", sep=',', mode='a+', header=None, index=None)
        time.sleep(0.5)
    except:
        df1['translate_content'] = ['']
        df1['translate_language'] = ['']
        df1.to_csv('./output/store.csv', encoding="utf-8-sig", sep=',', mode='a+', header=None, index=None)
        time.sleep(120)
        continue

