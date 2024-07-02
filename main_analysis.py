import pandas as pd
import deepface_emotion_to_sentiment
import utils




def get_data(video_id):
    """get the data of the video
    :param video_id: the video id
    :return: the data of the video
    """
    try:
        video_data = utils.get_sentiment_data(video_id + '_normalized_mtcnn-video')
    except:
        print(f"video data of {video_id} not found")
    try:
        comments_data = utils.get_sentiment_data(video_id + '-text')
    except:
        print(f"comments data of {video_id} not found")
    try:
        srt_data = utils.get_sentiment_data(video_id + '-sentiment_srt', 'data/calculated_srt/')
    except:
        print(f"srt data of {video_id} not found")

    return video_data, comments_data, srt_data

def make_average_video(video_data):
    """make the average of the video data
    :return: the average of the video data
    """
    emotion_angry = video_data['emotion.angry'].mean()
    emotion_disgust = video_data['emotion.disgust'].mean()
    emotion_fear = video_data['emotion.fear'].mean()
    emotion_happy = video_data['emotion.happy'].mean()
    emotion_sad = video_data['emotion.sad'].mean()
    emotion_surprise = video_data['emotion.surprise'].mean()
    emotion_neutral = video_data['emotion.neutral'].mean()


    return emotion_angry, emotion_disgust, emotion_fear, emotion_happy, emotion_sad, emotion_surprise, emotion_neutral

def make_average_comments(comments_data):
    """make the average of the comments data
    :return: the average of the comments data
    """
    positive = comments_data['positive_score'].mean()
    neutral = comments_data['neutral_score'].mean()
    negative = comments_data['negative_score'].mean()
    return positive, neutral, negative


def make_average_srt(srt_data):
    """make the average of the srt data
    :return: the average of the srt data in positive, neutral and negative
    """
    srt_average = pd.DataFrame()
    positive = srt_data['positive'].mean()
    neutral = srt_data['neutral'].mean()
    negative = srt_data['negative'].mean()
    return positive, neutral, negative


def return_statistics(statistics, video_id):
    """return the statistics of the video_id
    :param statistics: the statistics of the data
    :param video_id: the video id
    :return: the statistics of the video_id
    """
    statistics_of_id = statistics[statistics['id'] == video_id]
    return statistics_of_id

def get_data_all_sentiments(video_id):
    """make a combined dataframe of the data
    :param video_id: the video id
    :return: the combined dataframe
    """
    video_data, comments_data, srt_data = get_data(video_id)
    emotion_angry, emotion_disgust, emotion_fear, emotion_happy, emotion_sad, emotion_surprise, emotion_neutral = make_average_video(video_data)
    comments_postive, comments_neutral, comments_negative = make_average_comments(comments_data)
    srt_positive, srt_neutral, srt_negative = make_average_srt(srt_data)
    return emotion_angry, emotion_disgust, emotion_fear, emotion_happy, emotion_sad, emotion_surprise, emotion_neutral, comments_postive, comments_neutral, comments_negative, srt_positive, srt_neutral, srt_negative

def main():
    statistics = utils.get_sentiment_data('statistics_with_dislikes-video', 'data/')
    for index, row in statistics.iterrows():
        video_id = row['id']
        emotion_angry, emotion_disgust, emotion_fear, emotion_happy, emotion_sad, emotion_surprise, emotion_neutral, comments_postive, comments_neutral, comments_negative, srt_positive, srt_neutral, srt_negative = get_data_all_sentiments(video_id)
        statistics.loc[statistics['id'] == video_id, 'emotion_angry'] = emotion_angry
        statistics.loc[statistics['id'] == video_id, 'emotion_disgust'] = emotion_disgust
        statistics.loc[statistics['id'] == video_id, 'emotion_fear'] = emotion_fear
        statistics.loc[statistics['id'] == video_id, 'emotion_happy'] = emotion_happy
        statistics.loc[statistics['id'] == video_id, 'emotion_sad'] = emotion_sad
        statistics.loc[statistics['id'] == video_id, 'emotion_surprise'] = emotion_surprise
        statistics.loc[statistics['id'] == video_id, 'emotion_neutral'] = emotion_neutral
        statistics.loc[statistics['id'] == video_id, 'comments_positive'] = comments_postive
        statistics.loc[statistics['id'] == video_id, 'comments_neutral'] = comments_neutral
        statistics.loc[statistics['id'] == video_id, 'comments_negative'] = comments_negative
        statistics.loc[statistics['id'] == video_id, 'srt_positive'] = srt_positive
        statistics.loc[statistics['id'] == video_id, 'srt_neutral'] = srt_neutral
        statistics.loc[statistics['id'] == video_id, 'srt_negative'] = srt_negative
    print(statistics.to_string())
    utils.save_data_to_csv(statistics, 'statistics_all_sentiments_appended', 'video', 'data/')

# make_combined_dataframe('0nhbe5Sv4hs')
# get_data('0nhbe5Sv4hs')
main()