from pytube import YouTube
import os

def download(video_id, save_path="videos/"):
    """Download videos from YouTube and save them in specified path
    :param video_id: the id of the video
    :param save_path: the path to save the video
    :return: None
    """

    link = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(link)



    print(f"Downloading: {yt.title} ----- with id: {video_id}")
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(save_path, filename=video_id+".mp4")
    print("Download completed!!")

    return None
