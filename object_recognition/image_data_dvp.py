import time
import numpy as np
import cv2



class ImageManager:
    '''
    Class to be used to store the acquired images split in N channels and methods useful for object identification and roi creation
    '''

    def __init__(self, dim_h, dim_v,
                 roisize,
                 Nchannels = 2, dtype=np.uint16, debug=False):

        self.image = np.zeros((Nchannels,dim_v,dim_h),dtype) # original 16 bit images from the N channels   
        self.dim_h = dim_h
        self.dim_v = dim_v
        
        self.contours = []        # list of contours of the detected objects
        self.cx = []             # list of the x coordinates of the centroids of the detected object
        self.cy = []             # list of the y coordinates of the centroids of the detected object
         
        self.roisize = roisize
        self.debug = debug    

    def clear_countours(self):
        self.contours = []        
        self.cx = []             
        self.cy = []
        
    
    def find_object(self, channel=0, min_object_area=100, max_object_area=1000, bitdepth=12, norm_factor=None):    # ch: selected channel       
        """ Input: 
             channel: channel to use to create the 8 bit image to process
        Determines if a region avove thresold is a object, generates contours of the objects and their centroids cx and cy      
        """          
        im = self.image[channel]
        if norm_factor is None:
            norm_factor = (2**(bitdepth)-1) /255
        image8bit = (im/norm_factor).astype('uint8')
        

        _ret,thresh_pre = cv2.threshold(image8bit,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # ret is the threshold that was used, thresh is the thresholded image.     
        kernel  = np.ones((3,3),np.uint8)
        thresh = cv2.morphologyEx(thresh_pre,cv2.MORPH_OPEN, kernel, iterations = 1)
        # morphological opening (removes noise)

        if self.debug:
            self.image8bit = thresh

        cnts, _hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cx = []
        cy = []            
        contours = []
        roisize = self.roisize
        l = image8bit.shape
        
        for cnt in cnts:
            
            M = cv2.moments(cnt)
            if M['m00'] >  int(min_object_area) and M['m00'] < int(max_object_area): 
                # (M['m00'] gives the contour area, also as cv2.contourArea(cnt)
                x0 = int(M['m10']/M['m00']) 
                y0 = int(M['m01']/M['m00'])
                x = int(x0 - roisize//2) 
                y = int(y0 - roisize//2)
                w = h = roisize
        
                if x>0 and y>0 and x+w<l[1]-1 and y+h<l[0]-1:    # only rois far from edges are considered
                    cx.append(x0)
                    cy.append(y0)
                    contours.append(cnt)
        
        self.cx = cx
        self.cy = cy 
        self.contours = contours  

    
    def copy(self):
        """
        Returns a deep copy of the ImageManager instance.
        """
        new_im = ImageManager(
            self.dim_h,
            self.dim_v,
            self.roisize,
            Nchannels=self.image.shape[0],
            dtype=self.image.dtype
        )
        new_im.image = self.image.copy()
        new_im.contours = [cnt.copy() for cnt in self.contours]
        new_im.cx = self.cx.copy()
        new_im.cy = self.cy.copy()
        return new_im


    def draw_contours_on_image(self, image8bit):        
        """ Input: 
        img8bit: monochrome image, previously converted to 8bit
            Output:
        displayed_image: RGB image with rectangle annotations
        """  
        
        cx = self.cx
        cy = self.cy 
        roisize = self.roisize
        contours = self.contours
      
        displayed_image = cv2.cvtColor(image8bit,cv2.COLOR_GRAY2RGB)      
        
        for indx, _val in enumerate(cx):       
    
            x = int(cx[indx] - roisize//2) 
            y = int(cy[indx] - roisize//2)
         
            w = h = roisize
            
            displayed_image = cv2.drawContours(displayed_image, [contours[indx]], 0, (0,256,0), 2) 
            
            if indx == 0:
                color = (256,0,0)
            else: 
                color = (0,0,256)
                
            cv2.rectangle(displayed_image,(x,y),(x+w,y+h),color,1)
            
        return displayed_image
    
    
    
    def extract_rois(self, ch, cx, cy):
        """ Input: 
        ch: selected channel
        args: centroids cx and cy, if specified
            Output:
        rois: list of rois in the frame
        """          
        image16bit = self.image[ch]
    
        roisize = self.roisize
        rois = []
        
        for indx, _val in enumerate(cx):
            x = int(cx[indx] - roisize//2) 
            y = int(cy[indx] - roisize//2)
            w = h = roisize
            detail = image16bit [y:y+w, x:x+h]
            rois.append(detail)
                    
        return rois
   
    
    def highlight_channel(self,displayed_image):
        
         cv2.rectangle(displayed_image,(0,0),(self.dim_h-1,self.dim_v-1),(255,255,0),3) 
   
            
            
        