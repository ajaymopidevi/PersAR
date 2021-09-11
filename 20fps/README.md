The code is optimized to run at 6.45fps

## Optimizations: 
* Use cv2 functions to find the keypoints, descriptors and finally match them
* After matching, use only 100 best matches for finding Homography matrix
* Use cv2 function (warpPerspective) for warping 
* Instead of storing all the frames in a video, read and process the frame and continue to next frame.

**_All these optimizations achieve the similar performance with the original algorithm_**

## Profiling
1. Pre-processing:
   * "book_frames": 0.3345210552215576
   * "movie_frames": 0.24173760414123535
2. findCorrespondences:
   * "grayscale_conversion": 0.07948517799377441,
   * "features": 1.9628911018371582,
   * "findMatches": 5.395456552505493,
3. findHomography:
   * "H_ransac": 8.415274143218994,
4. projection:
   * "frame_resize": 0.19417428970336914,
   * "warping": 7.382027864456177,
   * "uint8_output": 0.631821870803833,
5. Post-processing
* "write_frame": 0.7568881511688232

"total_time": 26.32524585723877 for 511 frames


**Please copy these files to python folder and use them**
