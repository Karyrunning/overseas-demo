import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType
df = pd.read_csv('./output/sum_youtube_LDA.csv')

topic = df['Topic'].value_counts()
x_data = list(topic.index)
x_data1 = []
for x in x_data:
    x = x+1
    x_data1.append(x)
y_data = list(topic.values)
ls = [(j,int(k)) for j,k in zip(x_data1,y_data)]
ls.sort(key=lambda x:x[0],reverse=False)


c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
    .add(
        "",
        ls,
        rosetype="radius",
        radius="55%",
        center=["45%", "60%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="主题占比分布", pos_left="center",pos_top="10"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    .render("./output/主题占比分布.html")
)