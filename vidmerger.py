import os
import subprocess
#import cv2
import skvideo.io
import json



# 1) Find all videos in a given folder.
path = '/media/aleksejs/DataHDD/work/videos-dominik/VGlut_4_100418/'  # Don't forget / at the end
ext = '.avi'
rezfilename = 'merged_video_3' + ext
tmpfilename = path + 'tmp_vidmerger_list.txt'
framefilename = path + 'framecount3.txt'

tmpfile = open(tmpfilename, 'w')
framefile = open(framefilename, 'w')

for filename in os.listdir(path):
    if filename.endswith(ext):
        # Write paths to all videos to be merged into a single text file
        pathfilename = os.path.join(path, filename)
        tmpfile.write("file '" + pathfilename + "'\n")

        # Determine the frame count of each video and save it into a log file
        metadata = skvideo.io.ffprobe(pathfilename)
        # print(metadata.keys())
        # print(json.dumps(metadata["video"], indent=4))

        framefile.write(metadata["video"]["@nb_frames"] + " " + filename + "\n")

tmpfile.close()
framefile.close()

# 2) Concatenate files using ffmpeg
subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", tmpfilename, "-c", "copy", rezfilename])

# 3) Remove temporary file
os.remove(tmpfilename)
