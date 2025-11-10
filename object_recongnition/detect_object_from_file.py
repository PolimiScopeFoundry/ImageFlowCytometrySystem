import numpy as np
import cv2
from image_data_dvp import ImageManager
from find_h5_dataset import  get_h5_datasets  

# load dataset from h5
filename ='C:.......h5'
image = get_h5_datasets(filename,dataset_index=332) 

im = ImageManager(256,256,roisize=64)
im.image[0,...] = image

im.find_object(channel=0, min_object_area=100, max_object_area=1000, norm_factor=16)

image8bit = (image/16).astype('uint8') 

annotated_image = im.draw_conturs_on_image(image8bit)

cv2.imshow("Annotated Image", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


