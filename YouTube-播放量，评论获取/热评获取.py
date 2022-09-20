# URL can be a channel or a video, to extract comments
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import urllib.parse as p
import pandas as pd
import os
import pickle
import re
from tqdm import tqdm


SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

#身份验证函数
def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # 这里如果出问题了，那么说明是验证失效了，建议把token.pickle这个文件删掉，重新运行一遍程序
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build(api_service_name, api_version, credentials=creds)


youtube = youtube_authenticate()

#获取视频的id信息
def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")


#获取评论的线程列表，用于调用线程的使用
def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()

#获取视频评论内容信息
def get_youtube_comments(url,maxResults=20,n_pages=2):
    # url = "https://www.youtube.com/watch?v=WUMtFWa-sXI"
    # that's a video
    video_id = get_video_id_by_url(url)

    params = {
        'videoId': video_id,
        #获取评论的最大返回数量默认为20，最大可以返回100
        'maxResults': maxResults,
        'order': 'relevance', # default is 'time' (newest)
    }
    #获取视频的页数
    list_comment = []
    list_update = []
    list_like = []
    list_reply = []
    list_url = []
    for i in range(n_pages):
        # make API call to get all comments from the channel (including posts & videos)
        response = get_comments(youtube, **params)
        items = response.get("items")
        # if items is empty, breakout of the loop
        if not items:
            break
        for item in items:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comment1 = re.sub(r'(<.*?>)', '', comment)
            comment2 = re.sub(r'(&#39;[a-zA-Z])', '', comment1)
            updated_at = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
            like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            totalReplyCount = item["snippet"]["totalReplyCount"]
            list_comment.append(comment2)
            list_update.append(updated_at)
            list_like.append(like_count)
            list_reply.append(totalReplyCount)
            list_url.append(url)
            print(f"""\
            Comment: {comment}
            Likes: {like_count}
            Updated At: {updated_at}
            ==================================\
            """)
        if "nextPageToken" in response:
            # if there is a next page
            # add next page token to the params we pass to the function
            params["pageToken"] = response["nextPageToken"]
        else:
            # must be end of comments!!!!
            break
        print("*"*70)

    df2 = pd.DataFrame()
    df2['视频链接'] = list_url
    df2['评论内容'] = list_comment
    df2['评论点赞'] = list_like
    df2['评论回复'] = list_reply
    df2['视频时间'] = list_update
    df2.to_csv('./output/评论数据.csv',mode='a+', encoding='utf-8-sig', sep=',', index=None,header=None)

if __name__ == '__main__':
    # authenticate to YouTube API

    # url = 'https://www.youtube.com/watch?v=2J7ZhmE7d_w'
    # get_youtube_comments(url,2,2)
    #返回的最大结果内容数量
    result2 = 100
    #返回的页数
    page = 3
    df2 = pd.DataFrame()
    df2['视频链接'] = ['视频链接']
    df2['评论内容'] = ['评论内容']
    df2['评论点赞'] = ['评论点赞']
    df2['评论回复'] = ['评论回复']
    df2['视频时间'] = ['视频时间']
    df2.to_csv('./output/评论数据.csv',mode='w',encoding='utf-8-sig', sep=',', index=None,header=None)
    # df = pd.read_csv('./output/Youtube.csv')
    # df = df.sort_values(by=['观看次数'],ascending=False)
    # for url,number in tqdm(zip(df['链接'],df['评论数'])):
    #     if number != 0:
    #         # page = int(number / 10)
    #         get_youtube_comments(url, result2, page)
    #     else:
    #         pass
    for url in tqdm(['https://www.youtube.com/watch?v=lDjQ_RHH01Q','https://www.youtube.com/watch?v=Z1lEkbbNYLo']):
        get_youtube_comments(url, result2, page)