import os
import pandas as pd
import glob
from youtube_transcript_api import YouTubeTranscriptApi

def get_comments(video_id):
    """Opens the comments file and returns a dataframe of comments
    :param video_id: the id of the video
    :return: dataframe of comments
    """
    csv_file = f'data/comments/{video_id}_comments.csv'
    comments = pd.read_csv(csv_file)
    return comments


def get_sentiment_data(video_id, file_path='data/calculated_sentiments/', text_or_video='text'):
    """Opens the sentiment file and returns a dataframe of sentiment data
    :param video_id: the id of the video
    :param text_or_video: whether the data is from text or video
    :return: dataframe of sentiment data
    """
    csv_file = f'{file_path+video_id}.csv'
    data = pd.read_csv(csv_file, sep=';')
    return data


def save_data_to_csv(data, file_name, text_or_video='text', file_path='data/calculated_sentiments/'):
    """Saves the data to a csv file
    :param data: the data to be saved
    :param file_name: the name of the file
    :param text_or_video: whether the data is from text or video
    """
    data.to_csv(f'{file_path+file_name +"-"+ text_or_video}.csv', index=False, sep=';', encoding='utf-8')


def get_paths(path='videos/*.mp4'):
    """Returns the paths of the data files
    :return: the paths of the data files
    """
    list_of_files = glob.glob(path)

    return list_of_files


def get_video_ids(file_path):
    """Returns all the video ids from the file path
    :param file_path: the path of the file
    :return: list of video ids
    """
    file_txt = open(file_path, 'r')
    video_ids = file_txt.read().splitlines()
    return video_ids


def make_folders():
    """Makes the folders for the data
    :return: None
    """
    folders = ['data', 'data/calculated_sentiments', 'data/calculated_sentiments_FER', 'data/calculated_srt', 'data/calculated_sentiments_huggingface', 'videos']
    for folder in folders:
        try:
            os.mkdir(folder)
            print(f"Folder {folder} created!")
        except FileExistsError:
            pass
    return None

def get_srt(video_id):
    """Get calculated_srt from video id
    param: video_id: str
    return: calculated_srt file as list of dictionaries
    """
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        srt = [{"text": "No srt available for this video", 'start': 0, 'duration': 0}]
    srt_ready = []
    for i in srt:
        srt_ready.append(i['text'].replace("\n", " "))

    return srt_ready

