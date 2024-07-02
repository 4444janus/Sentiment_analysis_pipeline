import cv2
from fer import FER
from fer import Video
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import utils
import os
import sys

videofile = "videos/hqwGR86zoTI.mp4"
video_id = "hqwGR86zoTI"
# Face detection
emotion_detector = FER(mtcnn=True)

# Video predictions
video = Video(videofile)

# Output list of dictionaries
raw_data = video.analyze(emotion_detector, display=False)

# Convert to pandas for analysis
df = video.to_pandas(raw_data)
df = video.get_first_face(df)
df = video.get_emotions(df)
# Save data to csv
utils.save_data_to_csv(df, video_id, text_or_video='video_FER', file_path='data/calculated_sentiments_FER/')

print(df)
# Plot emotions
fig = df.plot(figsize=(20, 16), fontsize=26).get_figure()
# Filename for plot
fig.savefig(f'fig_{video_id}_FER.png')

