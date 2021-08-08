import numpy as np
import cv2
import skimage.io 
import skimage.color
from findCorrespondences import corner_detection, computeBrief, briefMatch
from matchPics import matchPics
from findHomography import computeH_ransac
from projection import Warping, invWarping, cv2Warping



#Test the Algorithm
cv_cover = cv2.imread('../data/cv_cover.jpg')
cv_desk = cv2.imread('../data/cv_desk.png')
hp_cover = cv2.imread('../data/hp_cover.jpg')


matches, locs1, locs2 = matchPics(cv_cover, cv_desk)

x1 =[]
x2=[]
for i in range(matches.shape[0]):
    x1.append(locs1[matches[i, 0]])
    x2.append(locs2[matches[i, 1]])

locs1 = np.float32(x1)
locs2 = np.float32(x2)

H = computeH_ransac(locs1, locs2)

#As cv_cover is used for estimating Homography matrix,
#hp_cover should be of same size as cv_cover
height = cv_cover.shape[0]
width = cv_cover.shape[1]
resized_hp_cover = cv2.resize(hp_cover,(width, height), interpolation=cv2.INTER_LINEAR)

output = Warping(H,resized_hp_cover, cv_desk)
cv2.imwrite("WarpingProjection.png",output)

#output = invWarping(H,resized_hp_cover, cv_desk)
#cv2.imwrite("InverseWarpingProjection.png",output)
