import utils
import pandas as pd
from transformers import pipeline

def extract_scores(sentiment):
    scores = {}
    for item in sentiment[0]:
            scores[item['label']] = item['score']
    return scores


distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    return_all_scores=True
    )
def analyze(video_id):

    # video_id = "7Fnli0wc11g"
    comments = utils.get_comments(video_id)
    max_length = 500 #max lenght of the comments

    comments = comments[comments['Comments'].str.len() < max_length]

    comments['sentiment'] = comments['Comments'].apply(lambda x: distilled_student_sentiment_classifier(x))

    comments['positive_score'] = comments['sentiment'].apply(lambda x: extract_scores(x)['positive'])
    comments['neutral_score'] = comments['sentiment'].apply(lambda x: extract_scores(x)['neutral'])
    comments['negative_score'] = comments['sentiment'].apply(lambda x: extract_scores(x)['negative'])
    comments.drop('sentiment', axis=1, inplace=True)
    total_positive = comments['positive_score'].sum()
    total_neutral = comments['neutral_score'].sum()
    total_negative = comments['negative_score'].sum()

    print("Total positive score:", total_positive)
    print("Total neutral score:", total_neutral)
    print("Total negative score:", total_negative)

    comments['total_score'] = comments[['positive_score', 'neutral_score', 'negative_score']].sum(axis=1)

    comments['normalized_positive'] = (comments['positive_score'] - comments['positive_score'].min()) / (
                comments['positive_score'].max() - comments['positive_score'].min())
    comments['normalized_neutral'] = (comments['neutral_score'] - comments['neutral_score'].min()) / (
                comments['neutral_score'].max() - comments['neutral_score'].min())
    comments['normalized_negative'] = (comments['negative_score'] - comments['negative_score'].min()) / (
                comments['negative_score'].max() - comments['negative_score'].min())

    comments['normalized_total'] = (comments['total_score'] - comments['total_score'].min()) / (
                comments['total_score'].max() - comments['total_score'].min())

    mean_positive = comments['positive_score'].mean()
    std_positive = comments['positive_score'].std()

    mean_neutral = comments['neutral_score'].mean()
    std_neutral = comments['neutral_score'].std()

    mean_negative = comments['negative_score'].mean()
    std_negative = comments['negative_score'].std()

    mean_total = comments['total_score'].mean()
    std_total = comments['total_score'].std()

    comments['z_normalized_positive'] = (comments['positive_score'] - mean_positive) / std_positive
    comments['z_normalized_neutral'] = (comments['neutral_score'] - mean_neutral) / std_neutral
    comments['z_normalized_negative'] = (comments['negative_score'] - mean_negative) / std_negative
    comments['z_normalized_total'] = (comments['total_score'] - mean_total) / std_total

    utils.save_data_to_csv(comments, video_id, "text")
    print(f"Data saved to data/calculated_sentiments/{video_id}.csv")


def sentiment_srt(video_id):
    """Get sentiment from calculated_srt file
    param: video_id: str
    return: None
    """
    srt = utils.get_srt(video_id)
    list_srt = []
    for sentence in srt:
        sentiment = distilled_student_sentiment_classifier(sentence)

        list_srt.append({'sentence': sentence, 'positive': sentiment[0][0]['score'], 'neutral': sentiment[0][1]['score'], 'negative':sentiment[0][2]['score']})

    df_srt = pd.DataFrame.from_records(list_srt)

    print(df_srt.describe())



    utils.save_data_to_csv(df_srt, video_id, "sentiment_srt", "data/calculated_srt/")



# sentiment_srt('7Fnli0wc11g')
# sentiment_srt('hqwGR86zoTI')