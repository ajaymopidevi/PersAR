# PersAR
 Simple AR application
 
 This is a part of the assignment for the [Computer Vision](https://www.cs.cmu.edu/~16385/) Course offfered bu CMU
 
 

https://user-images.githubusercontent.com/28349806/127646131-16042234-6a18-4c58-9dfd-6c7ed58fe783.mp4


## Algorithm:
1. **Detect the matching keypoints between the two frames**
   * Compute keypoints using FAST detector
   * Compute descriptors for each keypoint using BRIEF descriptor
   * Using the descriptors, find the matching keypoints between two images
     
     Used *FAST+BRIEF* to extract the features in realtime, while maintaining the performance similar to SIFT
     
2. **Find Homography Matrix using RANSAC**
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


