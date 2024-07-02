import os

import cv2


# frames_to_skip = 100  # Save every nth frame

def convert_to_frames(video_id, frames_to_skip=100, compression=50):
    """make frames from video and stores them in a folder
    param: video_id: str: the id of the video
    param: frames_to_skip: int: the number of frames to skip
    param: compression: int: the compression quality 0 to 100
    """
    print(f"Making frames from video {video_id}")
    frame_count = 0
    directory = f"frames/{video_id}"

    if not os.path.exists(directory):
        os.mkdir(directory)
    video_path = f"videos/{video_id}.mp4"

    video = cv2.VideoCapture(video_path)

    frames_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {frames_total}")

    for i in range(frames_total):
        ret, frame = video.read()
        if ret:
            if frame_count % frames_to_skip == 0:
                image_path = f"{directory}/image_{i}.jpg"
                cv2.imwrite(image_path, frame, [cv2.IMWRITE_JPEG_QUALITY, compression])
                print(f"Saved frame {i} as {image_path}")
            frame_count += 1

    video.release()

    print("Done with making frames!")

# make_frames_from_video('hqwGR86zoTI', 100, 50)