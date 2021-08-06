import numpy as np

def Warping(H2to1, template, img):
	imgShape = img.shape
	templateShape = template.shape

	composite_img = img
	for i in range(imgShape[0]):
		for j in range(imgShape[1]):
			idx1 = np.array([i, j, 1])
			idx2 = np.matmul(H2to1, idx1)
			idx2 = idx2 / idx2[-1]
			if idx2[0] >= 0 and idx2[1] >= 0 and idx2[0] < templateShape[0] and idx2[1] < templateShape[1]:
				# Intially floor , but later use bilinear interpolation
				index = [np.int(idx2[0]), np.int(idx2[1])]
				composite_img[i, j, :] = template[index[0], index[1], :]


	return composite_img

