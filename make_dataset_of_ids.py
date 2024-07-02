from pytube import Playlist
import pandas as pd
import utils
import os
import requests
import json

p = Playlist("put playlist link here")

def get_video_links(p):
    """Get the video links from the playlist
    param: playlist: str
    return: video_links: list
    """

    video_links = []
    for url in p.video_urls:
        video_links.append(url)
    return video_links

links = get_video_links(p)
api_key = os.environ.get('api_key')

def get_video_ids(p):
    """Get the video ids from the playlist
    param: playlist: str
    return: video_ids: list
    """
    video_ids = []
    for url in p.video_urls:
        video_id_split = url.split('=')
        video_id = video_id_split[1]
        video_ids.append(video_id)
    return video_ids


def get_video_category(video_id):
    """Get the video category from the video id
    param: video_id: str
    return: category: str
    """
    url = 'https://www.googleapis.com/youtube/v3/videos?id='+video_id+'&key='+api_key+'&part=snippet,contentDetails,statistics,status'
    response_info=requests.get(url).json()
    try:
        title = response_info['items'][0]['snippet']['title']
    except:
        title = None
    try:
        category = response_info['items'][0]['snippet']['categoryId']
    except:
        category = None
    try:
        tags = response_info['items'][0]['snippet']['tags']
    except:
        tags = None
    try:
        viewcounts = response_info['items'][0]['statistics']['viewCount']
    except:
        viewcounts = None
    try:
        commentcounts = response_info['items'][0]['statistics']['commentCount']
    except:
        commentcounts = None
    try: #get likes
        likes = response_info['items'][0]['statistics']['likeCount']
    except:
        likes = None
    try:
        # get dislikes
        url_api = "https://returnyoutubedislikeapi.com/votes?videoId=" + video_id
        response_API = requests.get(url_api)
        data = response_API.text
        parse_json = json.loads(data)
        number_dislikes = parse_json['dislikes']
    except:
        number_dislikes = None
    try:
        statistics = response_info['items'][0]['statistics']
    except:
        statistics = None
    try:
        duration = response_info['items'][0]['contentDetails']['duration']
    except:
        duration = None




    return title, category, tags, viewcounts, commentcounts, likes, number_dislikes, statistics, duration

ids = get_video_ids(p)

list_statistics = []
for id_ in ids:
    title, category, tags, viewcounts, commentcounts, likes, number_dislikes, statistics, duration = get_video_category(id_)
    list_statistics.append({'id': id_, 'title': title, 'category': category, 'tags': tags, 'viewcounts': viewcounts, 'commentcounts': commentcounts, 'likes': likes, 'number_dislikes': number_dislikes, 'statistics': statistics, 'duration': duration})


df_statistics = pd.DataFrame.from_records(list_statistics)
#delete row of commentcounts is None
df_statistics = df_statistics.dropna(subset=['commentcounts'])

print(df_statistics.to_string())
utils.save_data_to_csv(df_statistics, 'statistics_with_dislikes', 'video', 'data/')
