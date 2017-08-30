import csv, json, pickle
from create_dataset import *
import sys

folderLink = './data/TestImages/'

# Provide:
# - link to folder with images
# - description string
d = Dataset(folderLink, 'description ...')

# Verbose method:
# (Methods returns labels, data.
# So you can see them before you apply method 'createDataset')
label = d.createLabels()
print('[Labels created]')
data = d.createData()
print('[Data created]')
dataset = d.createDataset()
print('[Dataset created]')

filename_p = "./dataset.p"
pickle.dump(dataset, open(filename_p, 'wb'))

# To load dataset:
# dataset = pickle.load( open('./tomato_dataset_vol02.p', 'rb') )


