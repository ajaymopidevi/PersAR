import numpy as np

def Warping(H, template, img):
	imgShape = img.shape
	templateShape = template.shape

	for i in range(templateShape[0]):
		for j in range(templateShape[1]):
			idx1 = np.array([i, j, 1])
			idx2 = np.matmul(H, idx1)
			idx2 = idx2 / idx2[-1]
			if idx2[0] < 0:
				idx2[0] =0
			elif idx2[0] >= imgShape[0]:
				idx2[0] = imgShape[0]
			if idx2[1] < 0:
				idx2[1] = 0
			elif idx2[1] >= imgShape[1]:
				idx2[1] = imgShape[1]
			# Intially floor , but later use bilinear interpolation
			index = [np.int(idx2[0]), np.int(idx2[1])]
			composite_img[index[0], index[1], :] = template[i,j,:]

	return composite_img


def invWarping(H, template, img):
	imgShape = img.shape
	templateShape = template.shape

	invH = np.linalg.inv(H)

	composite_img = img
	for i in range(imgShape[0]):
		for j in range(imgShape[1]):
			idx1 = np.array([i, j, 1])
			idx2 = np.matmul(invH, idx1)
			idx2 = idx2 / idx2[-1]
			if idx2[0] >= 0 and idx2[1] >= 0 and idx2[0] < templateShape[0] and idx2[1] < templateShape[1]:
				# Intially floor , but later use bilinear interpolation
				index = [np.int(idx2[0]), np.int(idx2[1])]
				composite_img[i, j, :] = template[index[0], index[1], :]


	return composite_img
