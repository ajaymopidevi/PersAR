# PersAR
 Simple AR application
 
 
 
 





https://user-images.githubusercontent.com/28349806/134354609-fc7a13c0-d915-47ab-ab79-4c90e5d367fa.mp4





## Basic Algorithm:
1. **findCorrespondences**: Detect the matching keypoints between the two frames
   * Compute keypoints using FAST detector
   * Compute descriptors for each keypoint using BRIEF descriptor
   * Using the descriptors, find the matching keypoints between two images
     
     Used *FAST+BRIEF* to extract the features in realtime, while maintaining the performance similar to SIFT
     
2. **findHomography**: Homography Matrix using RANSAC
   * Minimum of 4 matching keypoints are required to compute Homography Matrix (8 DOF)
   * Randomly select M keypoints (M>=4) and find Homgraphy Matrix H using SVD
   * Compute the inliers where ||pi’, Hpi|| < ε i.e reprojection_error < threshold
   * Repeat the previous two steps for N times
   * Return the H with maximum inliers  
   
3. **Apply homography matrix to project the movie frames on top of the main video**
   * Create a binary mask with same shape as the image (Set all to 1)
   * Using Homography matrix, warp the movie frame.
   * Repeat the previous step for binary mask. This creates an 2D array with 1 at movie frame and 0 at the book frame
   * Using binary mask combine the movie frame and book frame


Problems with results/PersAR.avi :
1. Discontinued border lines 
2. Flickering 
Both fixed by Gaussian Blending

## Profiling for 30fps:
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


For the 30fps algorithm, each frame takes 31.5ms i.e 31.7 fps

NOTE: The input videos are from [Computer Vision](https://www.cs.cmu.edu/~16385/) Course offfered by CMU
