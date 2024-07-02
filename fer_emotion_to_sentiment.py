import utils

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = utils.get_sentiment_data('hqwGR86zoTI-video_FER', 'data/calculated_sentiments_FER/','video_FER', )
data1 = utils.get_sentiment_data('hqwGR86zoTI_normalized_huggingface-video')


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def get_data_from_df(data):
    """get the data from the dataframe
    :param data: the dataframe
    :return: the data
    """

    total_angry = data['angry'].sum()
    total_sad = data['sad'].sum()
    total_fear = data['fear'].sum()
    total_happy = data['happy'].sum()
    total_surprise = data['surprise'].sum()
    total_disgust = data['disgust'].sum()
    total_neutral = data['neutral'].sum()
    print(f"disgust: {total_disgust:.2f}")
    print(f"angry: {total_angry:.2f}")
    print(f"sad: {total_sad:.2f}")
    print(f"fear: {total_fear:.2f}")
    print(f"happy: {total_happy:.2f}")
    print(f"surprise: {total_surprise:.2f}")
    print(f"neutral: {total_neutral:.2f}")
    print("")
    positive = total_happy + total_surprise
    negative = total_angry + total_sad + total_fear + total_disgust
    print(f"positive: {positive:.2f}")
    print(f"negative: {negative:.2f}")
    print(f"positive percentage: {percentage(positive, positive + negative)}")
    print(f"negative percentage: {percentage(negative, positive + negative)}")
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.pie(data[['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']].mean(), labels=data[['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']].columns, autopct='%1.1f%%')
    ax.set_title('Emotion distribution')

    plt.show()

# get_data_from_df(data)
# get_data_from_df(data1)