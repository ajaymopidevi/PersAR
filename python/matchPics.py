import numpy as np
import cv2
import skimage.color
from findCorrespondences import briefMatch
from findCorrespondences import computeBrief
from findCorrespondences import corner_detection
from findCorrespondences import plotMatches


def matchPics(I1, I2):
    # I1, I2 : Images to match

    # Convert Images to GrayScale
    I1_gray = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
    I2_gray = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)

    # Detect Features in Both Images
    I1_kp = corner_detection(I1_gray)
    I2_kp = corner_detection(I2_gray)

    # Obtain descriptors for the computed feature locations
    I1_des, locs1 = computeBrief(I1_gray, I1_kp)
    I2_des, locs2 = computeBrief(I2_gray, I2_kp)

    # Match features using the descriptors
    matches = briefMatch(I1_des, I2_des)

    return matches, locs1, locs2


if __name__ == "__main__":
    # match ratio=0.8 had 3 outliers. The outliers can be removed by redcing the ratio to 0.7
    # However 0.7  has only 18 matches comapred to 61 matches(58 inliers) found when ratio is 0.8.

    I1 = cv2.imread(r'..\data\cv_cover.jpg')
    I2 = cv2.imread(r'..\data\cv_desk.png')

    matches, locs1, locs2 = matchPics(I1, I2)
    plotMatches(I1, I2, matches, locs1, locs2)

