import pandas as pd

df = pd.read_csv('sum_comment.csv')
new_df = df['comp_score'].value_counts()
print(new_df)