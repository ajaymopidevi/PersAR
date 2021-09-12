The code is optimized to run at 31.7 fps

## Optimizations: 
* Use cv2 functions to find the keypoints with a _Threshold= 40 and NonmaxSupression=True_. <br />
  If total keypoints is less than 300, reduce the threshold by 10 (till it is 0) and compute keypoints. 
* Use cv2 function to compute descriptors for the keypoints and finally match them
* After matching, use only 100 best matches for finding Homography matrix
* In findHomography, update the inliers_threshold = 0.8*N (80) from 0.9*N(90)
* Use cv2 function (warpPerspective) for warping 
* Instead of storing all the frames in a video, read and process the frame and continue to next frame.

**_All these optimizations achieve the similar performance with the original algorithm_**

## Profiling
1. Pre-processing:
   * "book_frames": 0.33844804763793945
   * "movie_frames": 0.2671029567718506
2. findCorrespondences:
   * "grayscale_conversion": 0.09944319725036621,
   * "features": 1.2347221374511719,
   * "findMatches": 1.730224847793579,
3. findHomography:
   * "H_ransac": 3.242617607116699,
4. projection:
   * "frame_resize": 0.15931916236877441,
   * "warping": 7.088443994522095,
   * "uint8_output": 0.5946335792541504,
5. Post-processing
* "write_frame": 0.5731518268585205

"total_time": 16.11925458908081 for 511 frames


**Please copy these files to python folder and use them**
