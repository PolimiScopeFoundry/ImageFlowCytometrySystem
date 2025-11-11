import h5py
import numpy as np
import cv2
from image_data_dvp import ImageManager
from find_h5_dataset import  get_h5_datasets  

##############
def h5_tree(val, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if items == 0:
            # the last item
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                try:
                    print(pre + '└── ' + key + ' (%d)' % len(val))
                except TypeError:
                    print(pre + '└── ' + key + ' (scalar)')
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                try:
                    print(pre + '├── ' + key + ' (%d)' % len(val))
                except TypeError:
                    print(pre + '├── ' + key + ' (scalar)')
###################
# load dataset from h5
filename = "C:\\Users\\YSpol\\Desktop\\1.h5"
file = h5py.File(filename,'r') 
stack = file['measurement']['IFC_measurement']['t0']['c0']['stack']
print(type(stack))
# h5_tree(file)



image = get_h5_datasets(filename,dataset_index=0) 
image = (image/16).astype('uint8') 

im = ImageManager(256,256,roisize=64, Nchannels=1, dtype='uint8')
im.image = image[1,...]

cv2.imshow("Inputted Image", im.image)
cv2.waitKey(0)
cv2.destroyAllWindows()

im.find_object(channel=0, min_object_area=100, max_object_area=1000, norm_factor=16)
print(im.cx)
print(im.contours)

# image8bit = (image/16).astype('uint8') 

annotated_image = im.draw_contours_on_image(image)

cv2.imshow("Annotated Image", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


