import utils
import pandas as pd
import glob
from transformers import pipeline

facial_emotions_image_detection = pipeline(model="dima806/facial_emotions_image_detection")

def analyze_video_deepface(video_id):
    """analyze video with huggingface model
    param: video_id: str: the id of the video
    return: dataframe of sentiment data
    """

    frames = glob.glob(f"frames/{video_id}/*.jpg")
    df = pd.DataFrame(columns=['sad', 'disgust', 'happy', 'angry', 'neutral', 'surprise', 'fear'])
    for frame in frames:
        fer = facial_emotions_image_detection(frame)
        print(fer)

        scores_dict = {entry['label']: entry['score'] for entry in fer}
        df = df.append(scores_dict, ignore_index=True)

        print(df)

    print(df)
    utils.save_data_to_csv(df, video_id + "_normalized_huggingface", text_or_video='video')


# analyze_video_deepface("hqwGR86zoTI")
