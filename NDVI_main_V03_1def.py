
##########################################################################
############ Astro Pi 22-23 Mission Space Lab Live on Earth  #############
############        INS Escola Industrial de Sabadell        #############
############                 Indus121 team                   #############   
##########################################################################

# The code needs the OpenCV (cv2), os and numpy libraries.
# The code loads the images (png and jpg) that are in the data photos folder
# Then it displays the original image and the image with the ndvi applied.

# ############ STANDARD LIBRAIRIES ###########

import cv2                                # open cv
import numpy as np                        # library for handling vectors.
from fastiecm import fastiecm



def calc_ndvi(image):
    b, g, r = cv2.split(image) # separate the image into 3 arrays for each color channel
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r.astype(float)) / bottom
    return ndvi 

def rescaling_ndvi_absolute(im):

    # This function rescales the NDVI to values between 0 and 255 taking into account that
    # that the extreme values are -1 (lowest possible ndvi) and 1 (highest possible ndvi)
    # By using this function you lose color resolution but gain that you can   
    # compare the values of the images with each other. The red will be the highest value (1) 
    # and gray will be the lowest (-1) ndvi value.

    in_min = -1.0
    in_max = 1.0

    out_min = 0.0
    out_max = 255.0
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))

    return out  

def rescaling_ndvi_relative(im):

    # This function rescales the NDVI to values between 0 and 255 taking into account
    # that the largest and smallest values in the image. For example if in the image the highest value 
    # the highest value is 0.7 and the lowest -0.3, 0.7 will be the highest value (255) and -0.3 the lowest (0).
    # Using this function you gain color resolution but you can't compare the images with each other. 
    # red will not be the highest value of ndvi but the highest value of a particular image.

    in_min = np.min(im)
    in_max = np.max(im)

    out_min = 0.0
    out_max = 255.0
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))

    return out 

def display_2_img(img1, img2):
    
    # Resize images to half their original size
    img1 = cv2.resize(img1, (int(img1.shape[1]/2), int(img1.shape[0]/2)))
    img2 = cv2.resize(img2, (int(img2.shape[1]/2), int(img2.shape[0]/2)))

    # Create a combined image
    combined_image = np.zeros((max(img1.shape[0], img2.shape[0]), 
                            img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)

    # Insert the original image in the left half of the merged image
    combined_image[:img1.shape[0], :img1.shape[1], :] = img1

    # Insert the filtered image in the right half of the merged image
    combined_image[:img2.shape[0], img1.shape[1]:, :] = img2

    # Display images in two split windows
    cv2.namedWindow('mapped_image', cv2.WINDOW_NORMAL) # original and filtered image
    cv2.imshow('mapped_image', combined_image) # original and filtered image
    cv2.imwrite('mapped_image.png', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def filter_earth(original_image):

    # you can choose between light or dark image statistical data. There does not seem to be much difference
    # light image statistics data (305)

    mean_red = 103
    std_red = 13.9
    mean_green = 121
    std_green = 10
    mean_blue = 120
    std_blue = 10

    # Statistical image data dark (299)
    # mean_red = 120
    # std_red = 16
    # mean_green = 134
    # std_green = 16
    # mean_blue = 133
    # std_blue = 16

    sigma_times = 5

    # Define maximum and minimum values for each RGB channel

    min_red = mean_red - sigma_times * std_red
    max_red = mean_red + sigma_times * std_red

    min_green = mean_green - sigma_times * std_green
    max_green = mean_green + sigma_times * std_green

    min_blue = mean_blue - sigma_times * std_blue
    max_blue = mean_blue + sigma_times * std_blue

    filtered_image = original_image.copy()

    # We apply a pixel value to obtain a NDVI = -1 (the lowest of all)

    filtered_image[ (original_image[..., 0] < min_blue) | (original_image[..., 0] > max_blue) |
                    (original_image[..., 1] < min_green) | (original_image[..., 1] > max_green) |
                    (original_image[..., 2] < min_red) | (original_image[..., 2] > max_red)] = [0, 0, 255]

    return filtered_image

def main():
    
    # load image
    original_image = cv2.imread('./indus121_selected/imagenoir305.jpg')

    # filter image
    filtered_image = filter_earth(original_image)

    # Calculate NDVI
    image_ndvi = calc_ndvi(filtered_image)

    # Apply NDVI contrast
    ndvi_contrast = rescaling_ndvi_absolute(image_ndvi)
    #ndvi_contrast = rescaling_ndvi_relative(image_ndvi)

    # Convert image to uint8 (0-255)
    image_ndvi_prep = ndvi_contrast.astype(np.uint8) 

    # Apply the color map
    color_mapped_image = cv2.applyColorMap(image_ndvi_prep, fastiecm)

    display_2_img(original_image,color_mapped_image)

if __name__ == "__main__":
    main()


