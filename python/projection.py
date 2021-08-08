import numpy as np
import cv2

def Warping(H, template, img):
	imgShape = img.shape
	templateShape = template.shape

	composite_img = img
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

def cv2Warping(H2to1, template, img):
	# Create a composite image after warping the template image on top
	# of the image using the homography

	# Note that the homography we compute is from the image to the template;
	# x_template = H2to1*x_photo
	# For warping the template to the image, we need to invert it.

	templateShape = template.shape
	imgShape = img.shape
	h = imgShape[0]
	w = imgShape[1]
	# Create mask of same size as template
	mask = np.ones(templateShape)

	# Warp mask by appropriate homography
	transform_mask = cv2.warpPerspective(mask, H2to1, (w,h))
	transform_mask = np.where(transform_mask < 1, 0, transform_mask)

	# Warp template by appropriate homography
	composite_img = cv2.warpPerspective(template, H2to1, (w,h))

	# Use mask to combine the warped template and the image
	composite_img = composite_img + (1 - transform_mask.astype(int)) * img

	return composite_img
