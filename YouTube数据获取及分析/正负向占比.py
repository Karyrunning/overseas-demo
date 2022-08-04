import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('./output/sum_new_lucky draw-评论数据.csv')

comp_score = df['comp_score'].value_counts()
x_data = list(comp_score.index)
y_data = list(comp_score.values)
print(x_data)
print(y_data)

df1 = pd.DataFrame({
    'Word':x_data,
    'count':y_data
})
df1.to_csv('./output/正负向占比统计.csv')
plt.style.use('fast')

plt.figure(figsize=(9,6),dpi=300)
plt.bar(x_data,y_data,color='#3498DB')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title("lucky draw-正向与负向占比")
plt.xlabel("类别")
plt.ylabel("数量")
plt.savefig('./output/lucky draw-正向与负向占比.jpg')
plt.show()



