import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import ast
import text2emotion as te

#download the vader lexicon before first use
nltk.download('vader_lexicon')
video_id = "hqwGR86zoTI"


def open_comments_file(video_id):
    """Opens the comments file and returns a list of comments"""
    comments_list = []
    with open(f'data/comments_{video_id}.txt', 'r', encoding='utf-8') as f:
        file = f.read()

        file = ast.literal_eval(file)

        for item in file['items']:
            comments_list.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    return comments_list

def sentiment_scores(sentence):
    sid = SentimentIntensityAnalyzer()
    sentiment_dict = sid.polarity_scores(sentence)
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    print(f"Emotion = {te.get_emotion(sentence)}")
    print(f"sentence: {sentence}")
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")

    elif sentiment_dict['compound'] <= - 0.05:
        print("Negative")

    else:
        print("Neutral")
    print("")




if __name__ == "__main__":

    comments = open_comments_file(video_id)
    print(len(comments))
    for comment in comments:
        sentiment_scores(comment)

