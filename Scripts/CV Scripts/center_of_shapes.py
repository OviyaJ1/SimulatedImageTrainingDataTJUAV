# import the necessary packages
import argparse
import sys
import imutils
import cv2

#image = cv2.imread(sys.argv[1]) #choose an image with the command line
image = cv2.imread("render%9.jpg") #manually choose an image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 145, 255, cv2.THRESH_BINARY)[1] #need to change threshold variables depending on the image
cv2.imwrite("Image.jpg", thresh)

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
#print(cnts)

# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	if M["m00"] != 0.0:
		#print(M["m10"], M["m00"])
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		# draw the contour and center of the shape on the image
		#cv2.drawContours(image, [c], -1, (0, 255, 0), 2) #draws countors in green
		cv2.circle(image, (cX, cY), 7, (255, 0, 255), -1) #draws centers in pink

cv2.imwrite("image_center.jpg", image)

