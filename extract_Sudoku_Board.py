# Mustafa Ghanim  Department of Electrical-Electronics Engineering 


import numpy as np
import cv2
from matplotlib import pyplot as plt


def image_preprocessing(img):
    # Performing preprocessing operations on the image to obtain better focused iamge by the main algorithm

    # Performing Guassian Filter to smooth and filter out the high frequency noises
    processed_image = cv2.GaussianBlur(img.copy(), (9, 9), 0)

    # Adaptive threshold with proper neighbour-looking kernal for binary conversion 
    processed_image = cv2.adaptiveThreshold(processed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

   # As mentioned in the report, we need to invert the binary image out in order 
   # to have grid lines pixels white and other obejcts mostly as black 
    binary_inverted_image = cv2.bitwise_not(processed_image)

    
    # image dilation to done to fill small holes that are supposed to be included to the detected lines
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
    dilated_image = cv2.dilate(binary_inverted_image, kernel)

    return dilated_image

    # A function that calculates the (x,y) coordinate system-based distance for two points
def find_distance (first_point, second_point):
    
    difference_in_y_axis = second_point[1] - first_point[1]
    difference_in_x_axis = second_point[0] - first_point[0]
    distance = np.sqrt((difference_in_x_axis ** 2) + (difference_in_y_axis ** 2))   
    return distance


def sudoku_corners_detection(img):
    
    # Checking the current OpenCV version to use the correct expression of cv2.findContours
    # findContours will obtain a list of contours detected in the image
    opencv_version = cv2.__version__.split('.')[0]
    if opencv_version == '3':
        _, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sotrting the Contours list in order to obtain the Puzzle's largest rectangle    
    contours = sorted(contours, key=cv2.contourArea, reverse=True) 
    largest_contour = contours[0]  # Largest rectangle

   # Using enumerate makes the code much simpler instead of writing many foor loops to look over the correct corners
   # min and  max functions are used to detect corners by the fact that:
   # while searching inside an image with i index for x-axis and j index for y-axis 
    # The Bottom-left corner has smallest (i - j) value
    # The Top-right corner has largest (i - j) value
    # The Bottom-right corner has the largest (i + j) value
    # The Top-left has corner smallest (i + j) value
    # lambda is anonymous  function that forces min/max functions to return the index of each resulted corner 
    bottom_left_corner, _= min(enumerate([point[0][0] - point[0][1] for point in largest_contour]), key= lambda elem: elem[1])
    top_right_corner,_= max(enumerate([point[0][0] - point[0][1] for point in largest_contour]),key= lambda elem: elem[1])
    bottom_right_corner,_= max(enumerate([point[0][0] + point[0][1] for point in largest_contour]), key= lambda elem: elem[1])#operator.itemgetter(1))
    top_left_corner,_= min(enumerate([point[0][0] + point[0][1] for point in largest_contour]), key= lambda elem: elem[1])
    
    # After finding the corner indexes return the corners array
    corners = [largest_contour[top_left_corner][0], largest_contour[top_right_corner][0], 
            largest_contour[bottom_right_corner][0], largest_contour[bottom_left_corner][0]]
    
    return corners

def create_square_mask_and_fit(img, corners):
   
    # Form the new mask's dimensions 
    top_left_corner = corners[0]
    top_right_corner = corners[1]
    bottom_right_corner = corners[2]
    bottom_left_corner = corners[3]

    # Create an array for the  mask that will be used for perspective transformation
    # This array is used to find maximum distance operations between all corner possibilities 
    rectangle_mask = np.array([top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner], dtype='float32')

    # Find the largest side length of the pissible square for the worst cases
    square_side = max([
        find_distance(bottom_right_corner, top_right_corner),
        find_distance(bottom_right_corner, bottom_left_corner),
        find_distance(top_left_corner, bottom_left_corner),
        find_distance(top_left_corner, top_right_corner)
    ])
    print("Longest Side Length of The Target Main Square \n",square_side)

    required_square = np.array([[0, 0], [square_side - 1, 0], [square_side - 1, square_side - 1],
                                [0, square_side - 1]], dtype='float32')
    # Finding the perspective matrix to be used in the target board square transformation
    perspective_transform_matrix = cv2.getPerspectiveTransform(rectangle_mask, required_square)
    print("Perspective Matrix\n",perspective_transform_matrix)
    # Finding the output square image (main ractangle) with crop/cut being done
    return cv2.warpPerspective(img, perspective_transform_matrix, (int(square_side), int(square_side)))

def extract_Sudoku_Board(img):    
    processed = image_preprocessing(img)
    sudoku_corners = sudoku_corners_detection(processed)
    extracted_board = create_square_mask_and_fit(img, sudoku_corners)
    return extracted_board