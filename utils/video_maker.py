from os import system
import numpy as np
import cv2

'''
    Creates an animation
    Given 
        - point_values: the colors of the points for each frame
        - h: the height of the video
        - w: the width of the video
        - bg: the bnw value of the background (0-255)
    Returns
        - The frames in a numpy object of shape (n_frames, height, width, 3)
                where the colors are in 0-255 BGR uint8 format
'''
def create_animation(point_values, h, w, bg):
    n_frames, n_pts, _ = point_values.shape
    rad = (h-20)/n_pts/2
    if not w:
        w = int(2*rad) + 10
    video = np.full((n_frames, h, w, 3), bg, dtype="uint8")

    for frame, pts in zip(video, point_values):
        for i, pt in enumerate(pts):
            r,g,b = pt
            cv2.circle(
                frame,
                (int(w/2), int(h-i*2*rad-rad-10)),
                int(rad)-2,
                color=(int(b),int(g),int(r)),
                thickness=-1
            )

    return video


'''
    Creates a video file in .avi format
    Given:
        - The frames in a numpy object of shape (n_frames, height, width, 3)
            where the colors are in 0-255 BGR uint8 format
        - The video file name
        - The file name of the audio file
        - The fps
'''
def create_video_file(frames, filename, audio_file, fps, transpose=True):
        length, height, width, channels = frames.shape

        print(f"Video:\n\tfps:\t\t{fps}\n\tFrames:\t\t{length}\n\tDuration:\t{length/fps} s")

        try:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height), True)

            for frame in frames:
                out.write(frame)
        except:
            raise
        finally:
            out.release()
            system('ffmpeg -y -loglevel warning -i ' + filename + ' -i ' + audio_file + ' -c copy -map 0:v:0 -map 1:a:0 ' + filename[:-3] + 'avi')
            if transpose:
                system('ffmpeg -y -loglevel warning -i ' + filename[:-3] + 'avi -vf "transpose=1" ' + filename[:-3] + '2.avi')
            system('rm ' + filename)