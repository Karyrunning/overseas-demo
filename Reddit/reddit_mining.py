import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import praw
import requests
from datetime import datetime
from pytz import timezone
import pytz

CLIENT_ID = 'vYU1DCgD1cAvyG_rjdj6JA'
SECRET_KEY = 'NY2rC7yLYFVJGGd56Hz3KneO9KwzLw'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

# my credentials
data = {
    'grant_type': 'password',
    'username': 'DorriyaRan',
    'password': 'dorriya0101'
}

headers = {'User-Agent': 'MYAPI/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth = auth, data = data, headers = headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers toour requests
requests.get('https://oauth.reddit.com/api/v1/me', headers = headers)

res = requests.get("https://oauth.reddit.com/r/halloween/new/", 
                   headers = headers, 
                   params = {'limit': '10'})

res.json()

df = pd.DataFrame()

for post in res.json()['data']['children']:
    
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'author_id': post['data']['name'],
        'reddit_http_id': post['data']['id'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'category': post['data']['link_flair_text'],
        'local_created_time_pst': datetime.utcfromtimestamp(post['data']['created']).astimezone(timezone('US/Pacific')),
        'utc_created_time_pst': datetime.utcfromtimestamp(post['data']['created_utc']).astimezone(timezone('US/Pacific')),
        'num_comments': post['data']['num_comments'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index = True)
