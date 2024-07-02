import utils
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy

from imageio.plugins import pillow

from ast import literal_eval
from wordcloud import WordCloud
from collections import Counter

time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")


def makeplots(data):
    data.sort_values(by=['category']).plot(x='category',
                                           y=['comments_positive', 'comments_neutral', 'comments_negative'], kind='bar')
    plt.title('All_Comments')
    plt.savefig(f'plots/comments_{time}.png')
    plt.show()

    data.sort_values(by=['category']).plot(x='id', y=['srt_positive', 'srt_neutral', 'srt_negative'], kind='bar')
    plt.title('All_SRT')
    plt.savefig(f'plots/srt_{time}.png')
    plt.show()

    data.sort_values(by=['category']).plot(x='id',
                                           y=['emotion_angry', 'emotion_disgust', 'emotion_fear', 'emotion_happy',
                                              'emotion_sad', 'emotion_surprise', 'emotion_neutral'], kind='bar')
    plt.title('All_Emotion')
    plt.savefig(f'plots/emotion_{time}.png')
    plt.show()


    for id in data['id']:
        data_id = data[data['id'] == id]
        data_id.plot(x='category', y=['comments_positive', 'comments_neutral', 'comments_negative'], kind='bar')
        plt.title(f'Comments_{id}')
        plt.savefig(f'plots/comments_{id}_{time}.png')
        # plt.show()

        data_id.plot(x='category', y=['srt_positive', 'srt_neutral', 'srt_negative'], kind='bar')
        plt.title(f'SRT_{id}')
        plt.savefig(f'plots/srt_{id}_{time}.png')
        # plt.show()

        data_id.plot(x='category',
                     y=['emotion_angry', 'emotion_disgust', 'emotion_fear', 'emotion_happy', 'emotion_sad',
                        'emotion_surprise', 'emotion_neutral'], kind='bar')
        plt.title(f'Emotion_{id}')
        plt.savefig(f'plots/emotion_{id}_{time}.png')
        # plt.show()


def describe_statistics(data):
    print(data.describe().to_string())

    print("more positive comments than negative comments:")
    print(data[data['comments_positive'] > data['comments_negative']].to_string())
    print("")
    print("more positive comments than negative comments and more likes than dislikes:")

    print(data[(data['comments_positive'] > data['comments_negative']) & (
                data['likes'] > data['number_dislikes'])].to_string())
    print("")
    print("more positive comments than negative comments and more dislikes than likes:")

    print(data[(data['comments_positive'] > data['comments_negative']) & (
                data['likes'] < data['number_dislikes'])].to_string())
    print("")
    print("more negative comments than positive comments and more likes than dislikes:")

    print(data[(data['comments_positive'] < data['comments_negative']) & (
                data['likes'] > data['number_dislikes'])].to_string())
    print("")
    print("more negative comments than positive comments and more dislikes than likes:")

    print(data[(data['comments_positive'] < data['comments_negative']) & (
                data['likes'] < data['number_dislikes'])].to_string())
    print("")
    print("")
    print(data['category'].unique())
    print(data['tags'].value_counts())


def plot_all(data):
    Education29 = data[data['category'] == 27]
    howto_and_style26 = data[data['category'] == 26]
    News_and_Politics25 = data[data['category'] == 25]
    Entertainment24 = data[data['category'] == 24]
    PeopleAndBlogs22 = data[data['category'] == 22]
    Sports17 = data[data['category'] == 17]
    Science_Technology28 = data[data['category'] == 28]
    nonprofits_activism29 = data[data['category'] == 29]
    list_all = [Education29, howto_and_style26, News_and_Politics25, Entertainment24, PeopleAndBlogs22, Sports17,
                Science_Technology28, nonprofits_activism29]
    for category in list_all:
        if category.iloc[0]['category'] == 29:
            name = 'Nonprofits & Activism ID:29'
        elif category.iloc[0]['category'] == 28:
            name = 'Science & Technology ID:28'
        elif category.iloc[0]['category'] == 27:
            name = 'Education ID:27'
        elif category.iloc[0]['category'] == 26:
            name = 'Howto & Style ID:26'
        elif category.iloc[0]['category'] == 25:
            name = 'News & Politics ID:25'
        elif category.iloc[0]['category'] == 24:
            name = 'Entertainment ID:24'
        elif category.iloc[0]['category'] == 22:
            name = 'People & Blogs ID:22'
        elif category.iloc[0]['category'] == 17:
            name = 'Sports ID:17'
        else:
            name = 'unknown'


        print(category.to_string())
        print(category['emotion_angry'])
        print(category['emotion_disgust'])
        print(category['emotion_fear'])
        print(category['emotion_happy'])
        print(category['emotion_sad'])
        print(category['emotion_surprise'])
        print(category['emotion_neutral'])
        ax = plt.axes()
        plt.boxplot([category['emotion_angry'], category['emotion_disgust'], category['emotion_fear'],
                     category['emotion_happy'], category['emotion_sad'], category['emotion_surprise'],
                     category['emotion_neutral']])
        plt.title(f'{name}')
        ax.set_xticklabels(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
        plt.ylabel('Emotion percentage')
        plt.xlabel('Emotion')

        plt.savefig(f"plots/boxplot_{category.iloc[0]['category']}_{time}.png")
        plt.show()



def parse_tags(data):
    tags = data['tags']
    all_tags = []

    for tag in tags:
        if type(tag) is str:
            my_list = literal_eval(tag)
            all_tags.extend(my_list)
    final = [x for x in all_tags if x.isascii()]
    return final


def make_wordcloud(all_tags, name='tags'):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(
        ' '.join(all_tags))

    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(name)
    plt.show()


def most_common_words(data):
    total_word_counts = Counter()
    word_count = Counter(data)

    top_n = 1000  # Change this number to get a different number of top words

    most_common_words = word_count.most_common(top_n)
    return most_common_words


def make_average_sentiments(data):
    list_tags = []

    dataframe_all_averages = pd.DataFrame(columns=['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
    Education29 = data[data['category'] == 27]
    howto_and_style26 = data[data['category'] == 26]
    News_and_Politics25 = data[data['category'] == 25]
    Entertainment24 = data[data['category'] == 24]
    PeopleAndBlogs22 = data[data['category'] == 22]
    Sports17 = data[data['category'] == 17]
    Science_Technology28 = data[data['category'] == 28]
    nonprofits_activism29 = data[data['category'] == 29]
    list_all = [Education29, howto_and_style26, News_and_Politics25, Entertainment24, PeopleAndBlogs22, Sports17,
                Science_Technology28, nonprofits_activism29]
    for category in list_all:
        if category.iloc[0]['category'] == 29:
            name = 'Nonprofits & Activism'
        elif category.iloc[0]['category'] == 28:
            name = 'Science & Technology'
        elif category.iloc[0]['category'] == 27:
            name = 'Education'
        elif category.iloc[0]['category'] == 26:
            name = 'Howto & Style'
        elif category.iloc[0]['category'] == 25:
            name = 'News & Politics'
        elif category.iloc[0]['category'] == 24:
            name = 'Entertainment'
        elif category.iloc[0]['category'] == 22:
            name = 'People & Blogs'
        elif category.iloc[0]['category'] == 17:
            name = 'Sports'
        else:
            name = 'unknown'
        words = parse_tags(category)
        print(f'name = {name}')
        print(words)
        most_common = most_common_words(parse_tags(category))

        list_tags.append(most_common)

        dataframe_all_averages._set_value(f'{name}', 'angry', category['emotion_angry'].mean())
        dataframe_all_averages._set_value(f'{name}', 'disgust', category['emotion_disgust'].mean())
        dataframe_all_averages._set_value(f'{name}', 'fear', category['emotion_fear'].mean())
        dataframe_all_averages._set_value(f'{name}', 'happy', category['emotion_happy'].mean())
        dataframe_all_averages._set_value(f'{name}', 'sad', category['emotion_sad'].mean())
        dataframe_all_averages._set_value(f'{name}', 'surprise', category['emotion_surprise'].mean())
        dataframe_all_averages._set_value(f'{name}', 'neutral', category['emotion_neutral'].mean())

    dataframe_tags = pd.DataFrame(columns=['tags', 'count'])
    for list_ in list_tags:
        for tag in list_:
            dataframe_tags.loc[len(dataframe_tags)] = tag


if __name__ == "__main__":
    data = utils.get_sentiment_data('statistics_all_sentiments_appended_v3', 'data/')

    make_average_sentiments(data)

