import cv2,numpy as np
import os

class Rotate():

    def __init__(self):
        pass

    # Returns tuple, that contains center coordinates of image.
    def center(self, a, b):
        cent = (a/2,b/2)
        return cent

    # Function turns image on choosen angle
    # around its center.
    # Changes image height and width.
    def rotation(self, scaleF = 1.0,degrees = 0):
        height_o,width_o = self.img.shape[:2]
        M = cv2.getRotationMatrix2D(self.center(width_o,height_o),angle = degrees,scale = scaleF)

        height_n, width_n = width_o*scaleF,height_o*scaleF
        r = np.deg2rad(degrees)
        height_n,width_n = (abs(np.sin(r)*height_n)
                            +abs(np.cos(r)*width_n)
                            ,abs(np.sin(r)*width_n)
                            +abs(np.cos(r)*height_n))
        
        (tx,ty) = ((width_n-width_o)/2,(height_n - height_o)/2)
        M[0,2] += tx
        M[1,2] += ty

        rotatedImage = cv2.warpAffine(self.img,M,dsize = (int(width_n),int(height_n)),borderMode=cv2.BORDER_TRANSPARENT)
        return rotatedImage

    # Save to choosen folder.
    def saveFolder(self, name):
        self.folder = './{}/'.format(str(name))
        os.mkdir(self.folder)

    def run(self, PathToImages):
        PoolOfImages = os.listdir(PathToImages)
        
        for num,link in enumerate(PoolOfImages):
            inp_image = str(PathToImages) + '/' +str(link)
            self.img = cv2.imread(inp_image)
            for i in range(0,360,90):
                rotated = self.rotation(1.0,i)
                #cv2.imshow('',rotated)
                cv2.imwrite( (str(self.folder)+'deg'+str(i)+str(link)), rotated )
                cv2.waitKey(10)
        
cv2.waitKey(0)
cv2.destroyAllWindows()
