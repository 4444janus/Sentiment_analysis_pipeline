import os
from googleapiclient.discovery import build
#python -m pip install --upgrade google-api-python-client
import json
import requests
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import utils
import warnings
warnings.filterwarnings('ignore')

api_key = os.environ.get('api_key')

youtube = build('youtube', 'v3', developerKey=api_key)
def get_comments_from_youtube(video_id):
    """Get comments from youtube api
    param: video_id: str
    return: all comments: list"""

    url = 'https://www.googleapis.com/youtube/v3/videos?id='+video_id+'&key='+api_key+'&part=snippet,contentDetails,statistics,status'
    response_info=requests.get(url).json()
    comments=[]
    for comment_count in response_info['items']:
        comments.append(comment_count['statistics'])
    for val in comments:
        total = int(val['commentCount'])
    print(f"amount of comments: {total}")
    if(total>=195000):
        print("Cannot retrieve more than 195,000 comments")


    return comments

def get_dislikes(video_id):
    url_api = "https://returnyoutubedislikeapi.com/votes?videoId="+video_id
    response_API=requests.get(url_api)
    data = response_API.text
    parse_json = json.loads(data)
    number_dislikes = parse_json['dislikes']
    print(f"number dislikes= {number_dislikes}")
    return number_dislikes


def getAllTopLevelCommentReplies(topCommentId, replies, token):
    max_pages = 10
    current_page = 0
    replies_response=youtube.comments().list(part='snippet',
                                               maxResults=100,
                                               parentId=topCommentId,
                                               pageToken=token).execute()

    for item in replies_response['items']:
        replies.append(item['snippet']['textDisplay'])
    if "nextPageToken" in replies_response:
        current_page += 1
        return getAllTopLevelCommentReplies(topCommentId, replies, replies_response['nextPageToken'])
    else:
        return replies

def get_comments(youtube, video_id, comments=[], token=''):
  totalReplyCount = 0
  replies=[]
  max_pages = 10
  current_page = 0
  video_response=youtube.commentThreads().list(part='snippet',
                                               videoId=video_id,
                                               pageToken=token).execute()
  for item in video_response['items']:
            comment = item['snippet']['topLevelComment']
            text = comment['snippet']['textDisplay']
            totalReplyCount = item['snippet']['totalReplyCount']
            if (totalReplyCount > 0):
               comments.extend(getAllTopLevelCommentReplies(comment['id'], replies, None))
            else:
               comments.append(text)
            replies = []

  if "nextPageToken" in video_response:
        current_page += 1
        return get_comments(youtube, video_id, comments, video_response['nextPageToken'])
  else:
        print(f"Amount of pages: {current_page}")
        return comments

#remove all special characters
def process_content(content):
    return " ".join(re.findall("[A-Za-z]+", content))

def preprocessing(video_id, df_from_yt):

    #remove emoji's
    df_from_yt = df_from_yt.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    df_from_yt

    #remove all urls
    df_from_yt['Comments'] = df_from_yt['Comments'].apply(lambda x: re.split('<a href="https:\/\/.*', str(x))[0])
    df_from_yt

    #remove all special characters
    # df_from_yt['Comments'] = df_from_yt['Comments'].apply(process_content)
    # df_from_yt

    #coverting to lower case
    df_from_yt['Comments'] = df_from_yt['Comments'].str.lower()
    df_from_yt

    #&#39; to '
    df_from_yt['Comments'] = df_from_yt['Comments'].str.replace('&#39;', "'")

    #remove <br>
    df_from_yt['Comments'] = df_from_yt['Comments'].str.replace('<br>', '')

    #remove semi-colon
    df_from_yt['Comments'] = df_from_yt['Comments'].str.replace(';', '')

    #removing empty rows
    df_from_yt['Comments'].replace('', np.nan, inplace=True)
    df_from_yt = df_from_yt.dropna()

    comments = []
    return df_from_yt


def get_comments_and_store(file_id):
    """Get comments from YouTube api and store in csv
    param: video_id: str
    return: None
    """
    print(f"Downloading comments for video: {file_id}")
    comments = get_comments(youtube, file_id)
    print(f"Amount of comments: {len(comments)}")
    df = pd.DataFrame(comments, columns=['Comments'])

    df_from_yt = preprocessing(file_id, df)

    df_from_yt.to_csv(f'data/comments/{file_id}_comments.csv', index=False)  # save comments from dataframe to csv file
    print(f"Download completed!!, stored in data/comments/{file_id}_comments.csv")