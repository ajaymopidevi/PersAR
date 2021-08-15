import numpy as np
import cv2
import imageio
import json
import time

#Import necessary functions
from findCorrespondences import cv2ExtractFeatures, cv2findMatches
from findHomography import computeH_ransac
from projection import cv2Warping

profiling ={}
profiling['book_frames'] =0
profiling['movie_frames'] =0
profiling['features'] = 0
profiling['grayscale_conversion'] = 0
profiling['findMatches'] = 0
profiling['H_ransac'] = 0
profiling['frame_resize'] = 0
profiling['warping'] = 0
profiling['uint8_output'] = 0
profiling['write_frame'] = 0
profiling['frames'] = 0
profiling['total_time'] = 0

start_time = time.time()


book_filename =r'..\data\book.mov'
movie_filename = r'..\data\ar_source.mov'
cv_cover_filename = r'..\data\cv_cover.jpg'

cv_cover_img = cv2.imread(cv_cover_filename, cv2.IMREAD_GRAYSCALE)
(height, width) = cv_cover_img.shape

cv_cover_des, locs1 = cv2ExtractFeatures(cv_cover_img)

writer1 = imageio.get_writer(r'..\results\PersAR_6fps.avi', fps=25)

book = cv2.VideoCapture(book_filename)
movie = cv2.VideoCapture(movie_filename)

if (book.isOpened() == False):
    print("Error opening book video stream or file")

if (movie.isOpened() == False):
    print("Error opening movie video stream or file")

frames = 0
while(book.isOpened() and movie.isOpened()):
    start = time.time()
    book_ret, book_frame = book.read()
    profiling['book_frames'] = profiling['book_frames'] + time.time() - start
    if book_ret == False:
        break

    start = time.time()
    movie_ret, movie_frame = movie.read()
    profiling['movie_frames'] = profiling['movie_frames'] + time.time() - start
    if movie_ret == False:
        break

    frames += 1

    start = time.time()
    I2 = cv2.cvtColor(book_frame, cv2.COLOR_RGB2GRAY)
    profiling['grayscale_conversion'] = profiling['grayscale_conversion'] + time.time() - start

    start = time.time()
    I2_des, locs2 = cv2ExtractFeatures(I2)
    profiling['features'] = profiling['features'] + time.time() - start

    start = time.time()
    # Matches
    matches = cv2findMatches(cv_cover_des, I2_des)
    profiling['findMatches'] = profiling['findMatches'] + time.time() - start

    start = time.time()
    x1 = np.array([locs1[mat.queryIdx].pt for mat in matches])
    x2 = np.array([locs2[mat.trainIdx].pt for mat in matches])
    H = computeH_ransac(x1, x2)
    profiling['H_ransac'] = profiling['H_ransac'] + time.time() - start

    start = time.time()
    resized_movie_frame = cv2.resize(movie_frame, (width, height), interpolation=cv2.INTER_LINEAR)
    profiling['frame_resize'] = profiling['frame_resize'] + time.time() - start

    start = time.time()
    output_frame = cv2Warping(H, resized_movie_frame, book_frame)
    profiling['warping'] = profiling['warping'] + time.time() - start

    start = time.time()
    output_frame = output_frame.astype('uint8')
    profiling['uint8_output'] = profiling['uint8_output'] + time.time() - start

    start = time.time()
    writer1.append_data(output_frame)
    profiling['write_frame'] = profiling['write_frame'] + time.time() - start

book.release()
movie.release()
writer1.close()

profiling['total_time'] = time.time() - start_time
profiling['frames'] = float(frames)

with open("profiling.json", "w") as outfile:
    json.dump(profiling, outfile, indent=4)
