import os
import cv2
import numpy as np
from network.convnet import NikNet, NikNet_01

# Turns image to (1,width*height*depth) array.
def image_processing(image_link, size, bw = False):
    if bw == True:
        image = cv2.imread(image_link, 0)
        image = cv2.resize(image, (size, size), interpolation = cv2.INTER_CUBIC)
        iY, iX = np.shape(image)
        iZ = 1
        image = np.reshape(image, [1,iZ,iX,iY])
    else:
        
        image = cv2.imread(image_link)
        #print('Original shape: {}'.format(np.shape(image)))
        
        image = cv2.resize(image, (size, size))
        #print('Reshaped array: {}'.format(np.shape(image)))
        
        iY, iX, iZ = np.shape(image)
        image = np.reshape(image, [1,iZ,iX,iY])
        #print('Tensorflow shape: {}'.format(np.shape(image)))

    return image, iZ

# Loads image, checks its depth, loads weight, gives prediction.
def predict(imlink):
    # If 3-d parameter is True, image will be loaded in bw mode
    image, depth = image_processing(imlink, 100)#, True)
    
    # Returns class name.
    def check(val):
            if int(val) == 0:
                return('Object_1')
            if int(val) == 1:
                return('Object_2')
            if int(val) == 2:
                return('Other')

    if depth == 3:
        weightsPath = './color_weight.h5'
        
    elif depth == 1:                
        weightsPath = './bw_weight.h5'
        
    model = NikNet_01.structure(width = 100, height = 100, depth = depth, classes = 3)

    opt = 'rmsprop'
    model.compile(loss = "categorical_crossentropy", optimizer = opt,
              metrics = ["accuracy"])

    model.load_weights(weightsPath)
    
    probs = model.predict(image)
    prediction = probs.argmax(axis = 1)

    print('||| Predicted: {}'.format(check(prediction[0])))

    resize_val = 100
    
    cv2.imshow("Object", cv2.resize(image.reshape(100,100,depth), (resize_val,resize_val), interpolation = cv2.INTER_CUBIC))    
    cv2.waitKey()
    cv2.destroyAllWindows()

# Test predictions:
#imlink = './images/object.jpg'
#predict(imlink)
