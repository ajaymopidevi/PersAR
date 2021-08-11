import numpy as np
import cv2
#Import necessary functions
from loadVid import loadVid
from findCorrespondences import corner_detection, computeBrief, briefMatch
from matchPics import matchPics
from findHomography import computeH_ransac
from projection import Warping, invWarping, cv2Warping
import time
import imageio


#Write script for Q3.1
book =r'..\data\book.mov'
ar_source = r'..\data\ar_source.mov'
cv_cover = r'..\data\cv_cover.jpg'

cv_cover_img = cv2.imread(cv_cover, cv2.IMREAD_GRAYSCALE)
(height, width) = cv_cover_img.shape

book_frames = loadVid(book)
ar_source_frames = loadVid(ar_source)
frames = np.min([book_frames.shape[0],ar_source_frames.shape[0]])


cv_cover_kp = corner_detection(cv_cover_img)
cv_cover_des, locs1 = computeBrief(cv_cover_img, cv_cover_kp)


writer1 = imageio.get_writer('AR.avi', fps=25)


for i in range(frames):
    print("Frame:",i)
    I2 = cv2.cvtColor(book_frames[i],cv2.COLOR_RGB2GRAY)
    I2_kp = corner_detection(I2)
    I2_des, locs2 = computeBrief(I2,I2_kp)
    #Matches
    matches = briefMatch(cv_cover_des, I2_des)
    x1=[]
    x2=[]
    for j in range(matches.shape[0]):
        x1.append(locs1[matches[j, 0]])
        x2.append(locs2[matches[j, 1]])
    x1 = np.array(x1)
    x2 = np.array(x2)
    H = computeH_ransac(x1, x2)
    resized_frame = cv2.resize(ar_source_frames[i], (width, height), interpolation=cv2.INTER_LINEAR)

    output_frame = invWarping(H,resized_frame,book_frames[i])
    #output_frame = compositeH(H, resized_frame, book_frames[i])
    output_frame = output_frame.astype('uint8')
    writer1.append_data(output_frame)

writer1.close()
