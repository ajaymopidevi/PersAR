import numpy as np
import cv2
import imageio

#Import necessary functions
from findCorrespondences import cv2ExtractFeatures, cv2findMatches
from findHomography import computeH_ransac
from projection import cv2Warping


book_filename =r'..\data\book.mov'
movie_filename = r'..\data\ar_source.mov'
cv_cover_filename = r'..\data\cv_cover.jpg'

cv_cover_img = cv2.imread(cv_cover_filename, cv2.IMREAD_GRAYSCALE)
(height, width) = cv_cover_img.shape

cv_cover_des, locs1 = cv2ExtractFeatures(cv_cover_img)

writer1 = imageio.get_writer(r'..\results\PersAR_20fps.avi', fps=25)

book = cv2.VideoCapture(book_filename)
movie = cv2.VideoCapture(movie_filename)

if (book.isOpened() == False):
    print("Error opening book video stream or file")

if (movie.isOpened() == False):
    print("Error opening movie video stream or file")

frames = 0
while(book.isOpened() and movie.isOpened()):
    book_ret, book_frame = book.read()
    if book_ret == False:
        break

    movie_ret, movie_frame = movie.read()
    if movie_ret == False:
        break

    frames += 1

    I2 = cv2.cvtColor(book_frame, cv2.COLOR_RGB2GRAY)
    I2_des, locs2 = cv2ExtractFeatures(I2)
    # Matches
    matches = cv2findMatches(cv_cover_des, I2_des)
    x1 = np.array([locs1[mat.queryIdx].pt for mat in matches])
    x2 = np.array([locs2[mat.trainIdx].pt for mat in matches])

    #Homography
    H = computeH_ransac(x1, x2)
    resized_movie_frame = cv2.resize(movie_frame, (width, height), interpolation=cv2.INTER_LINEAR)

    #Warping
    output_frame = cv2Warping(H, resized_movie_frame, book_frame)
    output_frame = output_frame.astype('uint8')
    writer1.append_data(output_frame)

book.release()
movie.release()
writer1.close()

