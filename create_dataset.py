import os, cv2
import numpy as np
import time
from tqdm import tqdm

ye,mon,day,hour,mins,_,_,_,_ = time.localtime()

class Dataset():
    # Load link of training folder.
    # Get all values inside of training folder.
    def __init__(self, folderLink, name=('Dataset. Created in:{}:{}_{}.{}.{}'.format(hour,mins,ye,mon,day))):
        self.folderLink = folderLink
        self.classes = None
        self.folder = os.listdir(self.folderLink)
        self.data = None
        self.label = None
        self.name = name

    # Create list for data
    def createData(self, bw = False, verbose = False):
        data = []
        for subfolder in tqdm(self.folder):
            for sfimage in os.listdir(str(self.folderLink)+str(subfolder)):
                if bw == True:
                    # For b/w image
                    image = cv2.imread('{}/{}/{}'.format(self.folderLink,subfolder,sfimage),0)
                else:
                    # For color image
                    image = cv2.imread('{}/{}/{}'.format(self.folderLink,subfolder,sfimage))
                if verbose == True:
                    print(sfimage)
                    print(np.shape(image))
                try:
                    iY,iX,iZ = np.shape(image)
                    stringImage = np.ndarray.tolist(np.reshape(image, (1, iX*iY*iZ)))
                except:
                    iY,iX = np.shape(image)
                    stringImage = np.ndarray.tolist(np.reshape(image, (1, iX*iY)))
                data.append(stringImage)
        data = np.array(data)
        self.data = data
        return data

    # Create list for labels.
    # All subfolders turns to numbers.
    # Each label of image equals number of subfolder.
    def createLabels(self, verbose = False):
        label = []
        self.classes = len(self.folder)
        for number,element in enumerate(tqdm(self.folder)):
            print(element)
            for subImage in os.listdir(str(self.folderLink)+str(element)):
                if verbose == True:
                    print(subImage)
                label.append(number)
        self.label = label
        return label

    # Make dataset with previously created data and label arrays.
    # Gives more verbosity.
    def createDataset(self):
        newDictionary = {"data":self.data,
                      "label":self.label,
                      "descr":"{}".format(self.name)}
        dataset = Dictionary(newDictionary)
        return dataset

    # Function that automaticaly makes dataset.
    def get(self):
        newDictionary = {"data":self.createData(),
                      "label":self.createLabels(),
                      "descr":"{}".format(self.name)}
        dataset = Dictionary(newDictionary)
        return dataset


# Creating class to get dictionary values by keys
# implemented as attributes.
class Dictionary(object):
    # Turns dictionary into class

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

