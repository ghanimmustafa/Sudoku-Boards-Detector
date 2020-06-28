# Mustafa Ghanim  Department of Electrical-Electronics Engineering 



# Import the required packages and designed functions
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

from extract_Sudoku_Board import *
from  detect_rectangules_directly import *
from applyPreprocessingWithPHT import * 
from my_display_actual_size import *



# Reading Images:
# if you do not want to folder/path based image reading/writing kindly use cv2.imread and cv2.imwrite directly
# folder_name contains the input images, change it accordingly if you wish
# folder_name should be at the same path where main.py is
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    print ("Number of images in the folder = \n", len(images))        
    return images

folder_name = 'input_images'
# output path used to store written images, output folder name is 'output_images' in my case
output_path = 'E:\My Google Drive/OZU/Spring2020/Computer Vision/Projects/First Project/final_codes/output_images'
input_images = load_images_from_folder(folder_name)

# Writing images to a specific path
def write_image(img,path, image_name):
    
    return cv2.imwrite(os.path.join(path , image_name), img)

img =  np.random.choice(input_images) # choosing a random image from the input folder, 
#img = input_images[key] works as well
#img = cv2.imread('image_name.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
board_img = extract_Sudoku_Board(gray_img) # its input must be gray-scale
PHT_input = board_img 

detected_Sudoku = detect_rectangules_directly(board_img) # Divide and Patch method
PHT = applyPreprocessingWithPHT(PHT_input) # Apply the method of Probabilistic Hough Transform

# Displaying results:

my_display_actual_size(img,'Input Image')
my_display_actual_size(detected_Sudoku,'Output Image With Rectangules Found Using Patching Method')
my_display_actual_size(PHT,'Detected Sudoku Inner Boxes Using PHT')

# Writing Images, comment if you don't want to write images on the output path
key = np.random.randint(2,1000,1) # a key to be included to the image name to avoid overwriting 

write_image(img,output_path,'input_'+str(key)+'.jpg')
write_image(detected_Sudoku,output_path,'output_directPatching_'+str(key)+'.jpg')
write_image(PHT,output_path,'output_PHT_'+str(key)+'.jpg')


# a simple function to show colour and  gray images with Python Based-scale (not used but useful) 
def show_image(img,title = 'title',color = False):
    if(color == True):
             plt.imshow(img)        
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title(title)
    plt.show()






