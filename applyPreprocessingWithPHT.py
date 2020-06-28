# Mustafa Ghanim  Department of Electrical-Electronics Engineering 

import cv2
import numpy as np
def applyPreprocessingWithPHT(img,guassian_kernal_size = 15, adaptive_filter_kernal_size = 15):
    # The most important parameters for this approach can by set by the user at main function
    

    # input image should be in the Gray-scale form
    blurred_img = cv2.GaussianBlur(img, (guassian_kernal_size, guassian_kernal_size), 0)

    adaptive_thr_img = cv2.adaptiveThreshold(blurred_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,adaptive_filter_kernal_size,1)


    binary_img = cv2.bitwise_not(adaptive_thr_img)


    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype = np.uint8)
    #dilated_img = cv2.dilate(binary_img, kernel)

    eroted_img = cv2.erode(binary_img,kernel,iterations = 1)


    img_color = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB) # to see colourful lines on the image


    lines = cv2.HoughLinesP(eroted_img, 1 , np.pi / 180, 100,minLineLength=100, maxLineGap=10)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img_color, (x1, y1), (x2, y2), (255, 0, 0),1)
    return img_color
    
    
# show_image(blurred_img,'Blurred Input Image')
# show_image(adaptive_thr_img,'Blurred Image After Adaptive Threshold')
#show_image(binary_img,'Binary Image')
# show_image(dilated_img,'Dilated Image')
# show_image(eroted_img,'Eroted Image')

  