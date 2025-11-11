import h5py
import numpy as np
import cv2
from image_data_dvp import ImageManager
from find_h5_dataset import get_h5_datasets

# load dataset from h5
filename = "C:\\Users\\YSpol\\Desktop\\251017_163457_IFC_measurement.h5"
data = get_h5_datasets(filename, dataset_index=0)
data = np.array(data)
data = np.squeeze(data)

# selecting a specific frame from the dataset
frame_index = 37   # 0 for first frame, 49 for the 50th, etc.

if data.ndim == 3:
    num_frames = data.shape[0]
    print(f"Dataset has {num_frames} frames. Using frame index: {frame_index}")
    if frame_index >= num_frames:
        raise ValueError(f"Frame index {frame_index} out of range (0–{num_frames-1})")
    image16bit = data[frame_index, ...]
elif data.ndim == 2:
    image16bit = data
else:
    raise RuntimeError(f"Unsupported dataset shape: {data.shape}")

H, W = image16bit.shape


im = ImageManager(dim_h=W, dim_v=H, roisize=64, Nchannels=1, dtype=np.uint16)
im.image[0, ...] = image16bit 

im.find_object(channel=0, min_object_area=10, max_object_area=200, norm_factor=4)
#print("Centroids X:", im.cx)
#print("Centroids Y:", im.cy)
#print("Num contours:", len(im.contours))


image8bit = (image16bit / 16).astype('uint8') 
annotated_image = im.draw_contours_on_image(image8bit)

# cv2.imshow("Input Image (8-bit view)", image8bit)
cv2.imshow("Annotated Image", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


