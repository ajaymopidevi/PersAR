import numpy as np
import cv2
import imageio
import json
import time

#Import necessary functions
from loadVid import loadVid
from findCorrespondences import corner_detection, computeBrief, briefMatch
from matchPics import matchPics
from findHomography import computeH_ransac
from projection import Warping, invWarping, cv2Warping
profiling ={}
profiling['book_frames'] =0
profiling['ar_source_frames'] =0
profiling['feature_detection'] = 0
profiling['descriptor'] = 0
profiling['grayscale_conversion'] = 0
profiling['findMatches'] = 0
profiling['H_ransac'] = 0
profiling['frame_resize'] = 0
profiling['warping'] = 0
profiling['uint8_output'] = 0
profiling['write_frame'] = 0
start_time = time.time()

book =r'..\data\book.mov'
ar_source = r'..\data\ar_source.mov'
cv_cover = r'..\data\cv_cover.jpg'

cv_cover_img = cv2.imread(cv_cover, cv2.IMREAD_GRAYSCALE)
(height, width) = cv_cover_img.shape
start = time.time()
book_frames = loadVid(book)
profiling['book_frames'] = time.time() - start

start = time.time()
ar_source_frames = loadVid(ar_source)
profiling['ar_source_frames'] = time.time() - start
frames = np.min([book_frames.shape[0],ar_source_frames.shape[0]])

start = time.time()
cv_cover_kp = corner_detection(cv_cover_img)
profiling['feature_detection'] = profiling['feature_detection'] + time.time()-start

start = time.time()
cv_cover_des, locs1 = computeBrief(cv_cover_img, cv_cover_kp)
profiling['descriptor'] = profiling['descriptor'] + time.time() - start

writer1 = imageio.get_writer(r'..\results\PersAR.avi', fps=25)


for i in range(frames):
    print("frame:", i)
    start = time.time()
    I2 = cv2.cvtColor(book_frames[i],cv2.COLOR_RGB2GRAY)
    profiling['grayscale_conversion'] = profiling['grayscale_conversion'] + time.time()-start
    start = time.time()
    I2_kp = corner_detection(I2)
    profiling['feature_detection'] = profiling['feature_detection'] + time.time() - start

    start = time.time()
    I2_des, locs2 = computeBrief(I2,I2_kp)
    profiling['descriptor'] = profiling['descriptor'] + time.time() - start

    start = time.time()
    #Matches
    matches = briefMatch(cv_cover_des, I2_des)
    profiling['findMatches'] = profiling['findMatches'] + time.time() - start

    start = time.time()
    x1=[]
    x2=[]
    for j in range(matches.shape[0]):
        x1.append(locs1[matches[j, 0]])
        x2.append(locs2[matches[j, 1]])
    x1 = np.array(x1)
    x2 = np.array(x2)
    H = computeH_ransac(x1, x2)
    profiling['H_ransac'] = profiling['H_ransac'] + time.time() - start

    start = time.time()
    resized_frame = cv2.resize(ar_source_frames[i], (width, height), interpolation=cv2.INTER_LINEAR)
    profiling['frame_resize'] = profiling['frame_resize'] + time.time() - start

    start = time.time()
    output_frame = invWarping(H,resized_frame,book_frames[i])
    profiling['warping'] = profiling['warping'] + time.time() - start

    start = time.time()
    output_frame = output_frame.astype('uint8')
    profiling['uint8_output'] = profiling['uint8_output'] + time.time() - start

    start = time.time()
    writer1.append_data(output_frame)
    profiling['write_frame'] = profiling['write_frame'] + time.time() - start



writer1.close()
profiling['total_time'] = time.time() - start_time
profiling['total_frames'] = float(frames)

with open("../profiling.json", "w") as outfile:
    json.dump(profiling, outfile, indent=4)
