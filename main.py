import utils
import youtube_video_download
import get_comments
import make_frames_from_video
# import fer_emotion_to_sentiment
# import utils
import huggingface_text_model
# import huggingface_picture_model
# import sentiment_analysis_text
import deepface_video_sentiment_analysis
# import deepface_emotion_to_sentiment
# import fer_emotion_to_sentiment

def main():
    id_done = open('data/ids_done.txt', 'r').read().splitlines()
    print(id_done )
    all_ids = utils.get_sentiment_data('statistics_with_dislikes-video', 'data/')

    for index, row in all_ids.iterrows():
        if row['id'] not in id_done:
            print(f"index: {index} row: {row['id']}")
            video_id = row['id']
            try:
                youtube_video_download.download(video_id)
            except:
                print(f"video with id: {video_id} could not be downloaded")
                continue
            get_comments.get_comments_and_store(video_id)
            make_frames_from_video.convert_to_frames(video_id, 100, 80)
            deepface_video_sentiment_analysis.analyze(video_id)
            huggingface_text_model.analyze(video_id)
            huggingface_text_model.sentiment_srt(video_id)

            #remove video id form all_ids
            id_done.append(video_id)
            #append to text file the ids
            with open('data/ids_done.txt', 'a') as f:
                f.write(video_id + '\n')

if __name__ == "__main__":
    main()
