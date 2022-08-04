import pandas as pd

df = pd.read_csv('./output/BP-Youtube.csv')

list_number = []
for i in df['评论总数']:
    cisu = int(i / 50)
    print(cisu)