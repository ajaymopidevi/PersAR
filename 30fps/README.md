The code is optimized to run at 20.62 fps

## Optimizations: 
* Use cv2 functions to find the keypoints with a _Threshold= 25 and NonmaxSupression=True_
* Use cv2 function to compute descriptors for the keypoints and finally match them
* After matching, use only 100 best matches for finding Homography matrix
* Use cv2 function (warpPerspective) for warping 
* Instead of storing all the frames in a video, read and process the frame and continue to next frame.

**_All these optimizations achieve the similar performance with the original algorithm_**

## Profiling
1. Pre-processing:
   * "book_frames": 0.3064250946044922
   * "movie_frames": 0.22094511985778809
2. findCorrespondences:
   * "grayscale_conversion": 0.09019780158996582,
   * "features": 2.0005733966827393,
   * "findMatches": 6.222008466720581,
3. findHomography:
   * "H_ransac": 6.559981346130371,
4. projection:
   * "frame_resize": 0.16079449653625488,
   * "warping": 7.252535820007324,
   * "uint8_output": 0.4972050189971924,
5. Post-processing
* "write_frame": 0.5810785293579102

"total_time": 24.78570556640625 for 511 frames


**Please copy these files to python folder and use them**
