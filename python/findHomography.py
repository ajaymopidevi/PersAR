import numpy as np
import cv2


def computeH(x1, x2):
	#Compute the homography between two sets of points
	nPts = x1.shape[0]
	A = np.zeros(((nPts * 2), 9))
	idx = 0
	for i in range(nPts):
		pt1 = x1[i, :]
		pt2 = x2[i, :]
		pt1_x = pt1[0]
		pt1_y = pt1[1]
		pt2_x = pt2[0]
		pt2_y = pt2[1]
		A[idx, :] = np.array([
			-pt1_x,
			-pt1_y,
			-1,
			0,
			0,
			0,
			pt1_x * pt2_x,
			pt1_y * pt2_x,
			pt2_x
		])
		idx = idx + 1
		A[idx, :] = np.array([
			0,
			0,
			0,
			-pt1_x,
			-pt1_y,
			-1,
			pt1_x * pt2_y,
			pt1_y * pt2_y,
			pt2_y
		])
		idx = idx + 1

	U, S, V = np.linalg.svd(A)
	H = V.T[:, -1]

	H1to2 = H.reshape((3, 3))

	return H1to2


def computeH_norm(x1, x2):
	#Compute the centroid of the points
	# Shift the origin of the points to the centroid
	# Normalize the points so that the largest distance from the origin is equal to sqrt(2)

	mean1 = np.mean(x1, axis=0)
	mean2 = np.mean(x2, axis=0)

	x1_t = x1 - mean1
	x2_t = x2 - mean2

	max1 = np.sqrt(np.max(x1_t ** 2, 0))
	x1_t = x1_t / max1

	max2 = np.sqrt(np.max(x2_t ** 2, 0))
	x2_t = x2_t / max2

	# Similarity transform 1
	T1 = np.array([[1 / max1[0], 0, -mean1[0] / max1[0]], [0, 1 / max1[1], -mean1[1] / max1[1]], [0, 0, 1]])

	# Similarity transform 2
	T2 = np.array([[1 / max2[0], 0, -mean2[0] / max2[0]], [0, 1 / max2[1], -mean2[1] / max2[1]], [0, 0, 1]])

	# Compute homography
	H1to2 = computeH(x1_t, x2_t)

	# Denormalization
	H1to2 = np.matmul(np.linalg.inv(T2), np.matmul(H1to2, T1))
	H1to2 = H1to2 / H1to2[2, 2]

	return H2to1




def computeH_ransac(locs1, locs2):
	#Compute the best fitting homography given a list of matching points



	return bestH2to1, inliers



def compositeH(H2to1, template, img):
	
	#Create a composite image after warping the template image on top
	#of the image using the homography

	#Note that the homography we compute is from the image to the template;
	#x_template = H2to1*x_photo
	#For warping the template to the image, we need to invert it.
	

	#Create mask of same size as template

	#Warp mask by appropriate homography

	#Warp template by appropriate homography

	#Use mask to combine the warped template and the image
	
	return composite_img


