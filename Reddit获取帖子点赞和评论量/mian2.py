import requests
import random
import pandas as pd
from tqdm import tqdm
import concurrent.futures
from lxml import etree

df = pd.read_csv('./input/Diablo_Immortal_Mobile - Jun 6, 2022 - 6 05 51 PM.csv',encoding='utf-16',sep='\t')


def chuli_url(x):
    x = str(x).split("?sort")
    x = x[0]
    return x


df['URL'] = df['URL'].apply(chuli_url)
df.drop_duplicates(subset=['URL'], keep='first', inplace=True)

new_df = df.groupby('Alternate Date Format').agg('sum')
print(new_df)