# Mustafa Ghanim  Department of Electrical-Electronics Engineering 

import cv2

# Function used to do patching operations on the image with drawing lines
def detect_rectangules_directly(img,scale = 9):
    # Convert the detected enclosed Sudoku back to RGB 
    #(colors may not be the same but the point is to see colorful lines)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    imgheight = img.shape[0]
    imgwidth = img.shape[1]
    y1 = 0
    M = imgheight//scale # only integer resulting division is allowed
    N =  imgheight//scale
    cv2.rectangle(img,(0,0),(imgwidth,imgheight),(0,255,0),10)
    for y in range(5,imgheight,M - 1): # 5 is a biasing value that can be changed to fit the lines properly
        for x in range(5, imgwidth, N - 1):
            y1 = y + M
            x1 = x + N
            cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0))
                    
    #my_display_actual_size(img,'Output Image With Rectangules Found Using Patching Method')
    return img