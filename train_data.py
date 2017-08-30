import keras
import tensorflow as tf
from network.convnet import NikNet, NikNet_01, NikNet_02, NikNet_03, NikNet_04
from sklearn.cross_validation import train_test_split
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import numpy as np
import cv2, h5py, pickle

from create_dataset import *

keras.backend.get_session().run(tf.initialize_all_variables())
keras.backend.get_session().run(tf.global_variables_initializer())

# Function for displaying images.
def show(image):
    cv2.imshow('',image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
# Create Dataset.
# Choose folder with subfolders, that contains training images.
# Comment this block if you already have dataset.
folderLink = '/data/'
d = Dataset(folderLink, 'description')
label = d.createLabels()
print('[Labels created]')
data = d.createData()
print('[Data created]')
dataset = d.createDataset()
print('[Dataset created]')
#-------------------------------------------------

dataset = pickle.load( open('./dataset.p', 'rb') )

# Load any type of datasets (with b/w or colorfull images).
try:
    data = dataset.data.reshape((dataset.data.shape[0], 100, 100));
    data = data[:, np.newaxis, :, :]
    depth_ = 1
    print(np.shape(data))
    (trainData , testData, trainLabels, testLabels) = train_test_split(
        data/255.0 , dataset.label, test_size = 0.30)
except:
    depth_ = 3
    data = dataset.data.reshape((dataset.data.shape[0], depth_, 100, 100));
    print(np.shape(data))
    (trainData , testData, trainLabels, testLabels) = train_test_split(
        data , dataset.label, test_size = 0.30)

# Check depth of loaded images.
print('||| Depth: {}'.format(depth_))

# Training and testing labels will be look like [0, 1, 0]
trainLabels = np_utils.to_categorical(trainLabels, 3)
testLabels = np_utils.to_categorical(testLabels, 3)

# Initialize the optimizer and model
#opt = SGD(lr = 0.01)       # Stochastic gradient descent
#opt = Adam(lr = 0.004)     # Adaptive moment estimation
opt = 'rmsprop'             # Root mean square propagation

model = NikNet_04.structure(width = 100, height = 100, depth = depth_, classes = 3)

model.compile(loss = "categorical_crossentropy", optimizer = opt,
              metrics = ["accuracy"])
print("||| Model compiled.")

print("||| Training in progress.")
model.fit(trainData, trainLabels, batch_size = 220, nb_epoch = 200,
          verbose = 1)

print("||| Evaluating.")
(loss, accuracy) = model.evaluate(testData, testLabels,
                                  batch_size = 100, verbose = 1)
print("||| Accuracy: {:.2f}%".format(accuracy * 100))

# Saving weights in hdf5.
model.save_weights('.//color_weights_{}%acc.h5'.format(int(accuracy*100)))

# Randomly select a few samples from testing part of data.
for i in np.random.choice(np.arange(0, len(testLabels)), size = (10,)):
    #Classify the object
    probs = model.predict(testData[np.newaxis, i])
    prediction = probs.argmax(axis = 1)

    # Merge 3 channels to see correct image.
    if depth_ == 1:
        image = (testData[i][0]*255).astype("uint8")
        image = cv2.merge([image]*3)
    # Multiply image by 255 to return original color values from normalized.
    elif depth_ == 3:    
        image = (np.reshape(testData[i], (100,100,3))*255)
        
    cv2.putText(image, str(prediction[0]),(5,20),
                cv2.FONT_HERSHEY_DUPLEX, 1, (230, 230, 230), 2)

    def check(val):
        if int(val) == 0:
            return('Object_1')
        if int(val) == 1:
            return('Object_2')
        if int(val) == 2:
            return('Other')

    print("||| Predicted -> {} | {} <- Actual".format(check(prediction[0]),
                                                check(np.argmax(testLabels[i]))))
    cv2.imshow("Object", image)
    cv2.waitKey(0)
