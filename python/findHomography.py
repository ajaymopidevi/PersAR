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

	return H1to2




def computeH_ransac(locs1, locs2):
	# Compute the best fitting homography given a list of matching points
	N = locs1.shape[0]
	Pts = list(np.arange(N))
	inliers = 0
	inliers_threshold = int(0.9 * N)
	maxiter = 100
	distance_threshold = 5

	bestH = np.zeros((3, 3))
	for i in range(maxiter):
		samples = random.sample(Pts, 4)

		x1 = []
		x2 = []
		for j in samples:
			x1.append(locs1[j, :])
			x2.append(locs2[j, :])
		x1 = np.array(x1)
		x2 = np.array(x2)
		H = computeH_norm(x1, x2)

		# Find the inliers
		# Instead of calculating for each point, it can be done for all locs1 together
		x1 = np.ones((N, 3))
		x1[:, :-1] = locs1
		x1 = x1.transpose()
		pred_x2 = np.matmul(H, x1)

		# Dividing by w
		pred_x2 = pred_x2.transpose()
		pred_x2 = pred_x2[:, :-1] / (pred_x2[:, -1].reshape((N, 1)))
		diff = np.sum((pred_x2 - locs2) ** 2, axis=1)
		n_inliers = len(np.where(diff < distance_threshold)[0])

		# This condition can be varied
		if (n_inliers >= inliers_threshold):
			return H
		elif (n_inliers > inliers):
			inliers = n_inliers
			bestH = H

	# print("Inliers percentage: ",inliers/N)
	return bestH

