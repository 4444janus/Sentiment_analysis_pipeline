from deepface import DeepFace
import cv2
import glob
import pandas as pd
import utils

models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "ArcFace"]
detectors = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]


# video_id = f"hqwGR86zoTI_all_frames"


# video_id = f"hqwGR86zoTI_100_frames"

def analyze(video_id, actions=["age", "gender", "emotion", "race"]):
    """analyze video with deepface
    param: video_id: str: the id of the video
    param: model: str: the model to use
    param: actions: list: the actions to perform
    """
    print(f"Analyzing video {video_id}")
    frames = glob.glob(f"frames/{video_id}/*.jpg")
    print(f"Frames: {frames}")
    df = pd.DataFrame()
    for frame in frames:
        analyze = DeepFace.analyze(img_path=frame, actions=actions, detector_backend="mtcnn", silent=True, enforce_detection=False)
        if analyze: #if list is not empty
            normalized = pd.json_normalize(analyze[0])
            df = df.append(normalized, ignore_index=True)

    utils.save_data_to_csv(df, video_id + "_normalized_mtcnn", text_or_video='video')
    print(f"Done analyzing video, data stored in {video_id + '_normalized_mtcnn.csv'}")

# analyze_video_deepface("hqwGR86zoTI_100_frames_compression_50")
# analyze_video_deepface("hqwGR86zoTI_all_frames")

# analyze_video_deepface("hqwGR86zoTI")
