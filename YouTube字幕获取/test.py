import youtube_dl
import os
import webbrowser
import pandas as pd



df = pd.read_csv('Youtube.csv', encoding="UTF-16",sep='\t')
df['youtube_view'] = df['youtube_view'].astype(int)
df1 = df.sort_values(by=['youtube_view'],ascending=False)
quanbuURLS = df1['URL'][0:20]
print(quanbuURLS)
# count = 1
# for url in quanbuURLS:
#     print('开始下载第{}个'.format(count))
#
#     #os.system("youtube-dl --write-auto-sub \
#     #--sub-lang es --write-auto-sub  -f m4a " + url)
#
#
#     # 下载音频
#     # os.system("youtube-dl -f m4a " + url)
#     # 下载中文字幕
#     # os.system("youtube-dl --write-sub --sub-lang en --skip-download " + url)
#     # os.system("youtube-dl --write-sub --sub-lang zh-Hans --skip-download " + url)
#     # os.system("youtube-dl --write-sub --sub-lang zh-Hant --skip-download " + url)
#     try:
#         os.system("youtube-dl --write-auto-sub --sub-lang en --skip-download "+ url)
#         os.chdir(r"data")
#     except:
#         pass
#
#     print('第{}个下载完成,已完成{:.3f}'.format(count, count / len(quanbuURLS)))
#     count += 1