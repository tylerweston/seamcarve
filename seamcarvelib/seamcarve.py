import os
import sys
import subprocess
import shutil
import cv2
import ffmpeg

# Based on code from:
# https://github.com/AlexZeGamer/distort-video


def carve_seams(in_file, out_file, distort_percentage=60, silent=False):
    # define paths
    path = os.path.abspath(os.path.join(sys.argv[0], os.pardir))
    result_dir_path = os.path.join(path, 'result')

    video_name = os.path.join(path, in_file)
    if not os.path.isfile(in_file):
        raise FileNotFoundError(f'Input file not found: {in_file}')
    frames_path = os.path.join(result_dir_path, 'frames')
    distorted_frames_path = os.path.join(result_dir_path, 'distortedFrames')

    # define video variables
    capture = cv2.VideoCapture(video_name)
    fps = capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_size = (
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    # create output directories
    os.makedirs(result_dir_path, exist_ok=True)
    os.makedirs(frames_path, exist_ok=True)
    os.makedirs(distorted_frames_path, exist_ok=True)
    for elem in os.listdir(frames_path):
        os.remove(os.path.join(frames_path, elem))
    for elem in os.listdir(distorted_frames_path):
        os.remove(os.path.join(distorted_frames_path, elem))

    # convert video to frames
    if not silent:
        print('Converting video into frames...')
    frame_number = 0
    while True:
        if not silent:
            print(f'{frame_number}/{total_frames}', end='\r')
        success, frame = capture.read()

        if not success:
            break

        # naming the file with an appropriate number of leading zeros
        filename = f'frame_{str(frame_number).zfill(len(str(total_frames)))}.jpg'
        cv2.imwrite(os.path.join(frames_path, filename), frame)
        frame_number += 1
    capture.release()

    # distortion of frames
    if not silent:
        print('Distorting frames...')
    for i, elem in enumerate(os.listdir(frames_path), start=1):
        if not silent:
            print(f'{i}/{total_frames}', end="\r")
        current_frame_path = os.path.join(frames_path, elem)
        distorted_frame_path = os.path.join(distorted_frames_path, elem)
        cmd = f"magick {current_frame_path}\
            -liquid-rescale {100-distort_percentage}x{100-distort_percentage}%\\!\
            -resize {video_size[0]}x{video_size[1]}\\! {distorted_frame_path}"
        exit_code, command_output = subprocess.getstatusoutput(cmd)

        if exit_code != 0:
            raise os.error(f'Error while distorting frame {i}/{total_frames}:\n{command_output}\n')

    # Assembling frames back into a video
    if not silent:
        print('Creating video...')
    img_array = [cv2.imread(os.path.join(distorted_frames_path, elem))
                 for elem in sorted(os.listdir(distorted_frames_path))]
    distorted_video_path = os.path.join(path, "distorted_" + out_file)
    out = cv2.VideoWriter(distorted_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, video_size)

    if not silent:  # Check here so we're not checking per frame
        print('Writing video...')
        for i in range(len(img_array)):
            print(f'{i}/{total_frames}', end="\r")
            out.write(img_array[i])
    else:
        for i in range(len(img_array)):
            out.write(img_array[i])
    out.release()

    # Add sounds from original video to distorted video
    if not silent:
        print("Adding sound to distorted video..")
    video = ffmpeg.input(distorted_video_path).video
    audio = ffmpeg.input(video_name).audio
    try:
        result_video_path = os.path.join(path, out_file)
        (
            ffmpeg
            .concat(video, audio, v=1, a=1)     # v = video stream, a = audio stream
            .output(result_video_path)
            .run(overwrite_output=True, quiet=True)
            # Documentation : https://kkroening.github.io/ffmpeg-python/
        )
    except ffmpeg.Error as e:
        raise os.error(f"Problem with ffmpeg while concatenating audio: {e}")
    finally:
        if not silent:
            print("Removing generated files...")
        try:
            shutil.rmtree(result_dir_path)
            os.remove(distorted_video_path)
        except OSError as e:
            raise os.error(f"Error while removing generated files: {e}")

    if not silent:
        print(f"Done! Wrote new video to: {result_video_path}")
