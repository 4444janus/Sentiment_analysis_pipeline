import pandas as pd

import utils


def make_plot_data(video_id_1, video_id_2, video_id_3):
    import matplotlib.pyplot as plt
    import numpy as np
    df1 = utils.get_sentiment_data(video_id_1)
    df2 = utils.get_sentiment_data(video_id_2)
    df3 = utils.get_sentiment_data(video_id_3)
    print(df1.to_string())

    average_df1 = df1['dominant_emotion'].value_counts()
    average_df2 = df2['dominant_emotion'].value_counts()
    average_df3 = df3['dominant_emotion'].value_counts()
    print(average_df1, average_df2, average_df3)

    plt.plot(df1['dominant_emotion'].value_counts().values, df1['dominant_emotion'].value_counts().index)
    plt.xlabel('Dominant Emotion')
    plt.ylabel('Frequency')
    plt.title('Dominant Emotion')
    plt.show()

    face_confidence_df1 = df1['face_confidence'].describe()
    face_confidence_df2 = df2['face_confidence'].describe()
    face_confidence_df3 = df3['face_confidence'].describe()
    print(face_confidence_df1, face_confidence_df2, face_confidence_df3)
    face_confidence_counts_df1 = df1['face_confidence'].value_counts()
    face_confidence_counts_df2 = df2['face_confidence'].value_counts()
    face_confidence_counts_df3 = df3['face_confidence'].value_counts()
    print(face_confidence_counts_df1, face_confidence_counts_df2, face_confidence_counts_df3)

    print(df3['face_confidence'])
    df3 = df3[df3['face_confidence'] != 0]
    print(df3['face_confidence'].to_string())





def emotion_to_sentiment(video_id):
    data = utils.get_sentiment_data(video_id)

    average_age = data['age'].mean()
    print(f"average_age: {average_age}")
    average_emotion_angry = data['emotion.angry'].mean()
    print(f"mean_emotion_angry: {average_emotion_angry}")
    average_emotion_disgust = data['emotion.disgust'].mean()
    print(f"mean_emotion_disgust: {average_emotion_disgust}")
    average_emotion_fear = data['emotion.fear'].mean()
    print(f"mean_emotion_fear: {average_emotion_fear}")
    average_emotion_happy = data['emotion.happy'].mean()
    print(f"mean_emotion_happy: {average_emotion_happy}")
    average_emotion_sad = data['emotion.sad'].mean()
    print(f"mean_emotion_sad: {average_emotion_sad}")
    average_emotion_surprise = data['emotion.surprise'].mean()
    print(f"mean_emotion_surprise: {average_emotion_surprise}")
    average_emotion_neutral = data['emotion.neutral'].mean()
    print(f"mean_emotion_neutral: {average_emotion_neutral}")

    most_common_dominant_emotion = data['dominant_emotion'].value_counts().idxmax()
    print(f"most_common_dominant_emotion: {most_common_dominant_emotion}")

    print("")
    print("#" * 50)
    print("")

    data['sentiment'] = data['dominant_emotion'].apply(lambda x: 'neutral' if x == 'neutral' else 'positive' if x == 'happy' else 'negative')
    print(data['sentiment'])
    print(data['sentiment'].value_counts())

    most_common_sentiment = data['sentiment'].value_counts().idxmax()
    print(f"most_common_sentiment: {most_common_sentiment}")
    return
# emotion_to_sentiment('hqwGR86zoTI_60_frames_normalized-video')
# emotion_to_sentiment('45pTq0ADz6o_normalized_mtcnn-video')
# emotion_to_sentiment('1aA1WGON49E_normalized_mtcnn-video')
# emotion_to_sentiment('annotated_normalized_mtcnn-video')
# emotion_to_sentiment('happy_normalized_mtcnn-video')

# make_plot_data('hqwGR86zoTI_100_frames_compression_50_normalized__-video', 'hqwGR86zoTI_100_frames_compression_50_normalized_-video', 'hqwGR86zoTI_100_frames_compression_50_normalized-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_all_frames_normalized-video')


# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_mtcnn-video')
# make_plot_data('-kBdZSjSwjg_normalized_mtcnn-video', '_lyQmMnOV_E_normalized_mtcnn-video', 'hqwGR86zoTI_all_frames_normalized-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
# make_plot_data('hqwGR86zoTI_60_frames_normalized-video', 'hqwGR86zoTI_100_frames_normalized-video', 'hqwGR86zoTI_normalized_huggingface-video')
