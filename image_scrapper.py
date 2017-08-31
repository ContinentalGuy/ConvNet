import os
import urllib
import requests
import argparse

class Scrapper():
    def __init__(self, url, fname, divideNum, number):
        # Imagenet url with links of images choosen category.
        self.url = url
        # First part of image names.
        self.fname = fname
        # Name of directory that will be created.
        # Equals to names of images in this folder,
        # But printed in CAPS.
        self.directory = fname.upper()
        # Int, that divides whole list of urls.
        self.divideNum = divideNum
        # Value that gives one part of divided dataset. - to GUI!
        self.number = number

    def link(self):
        return self.directory

    # Function that divides pool of urls and returns its for choosen part.
    def divide_urls(self, pool_, divNum, partNum, help = 'divNum - (integer) number of parts you want to divide your pool. partNum - (integer) number of part you wnt to get from divided pool.'):
        if partNum <= divNum:
            urls_ = []
            nElements = int((len(pool_))/divNum)
            start = nElements * (partNum - 1)
            stop = nElements * partNum
            for element in pool_[start:stop]:
                urls_.append(element)
            return urls_
        else:
            print('Cannot correctly divide pool. Try to change parameters.')
            pass

    def RUN(self):
        try:
            os.mkdir('./{}'.format(self.directory))
        except:
            pass
        '''
        # Creating a request to url.
        site = requests.get(str(url))
        # Getting content as string.
        text = site.text
        
        
        # List with image URLs.
        urlPool = text.split('\r\n')
        #'''

        # Open .txt file if connection to ImageNet is to weak or slow.
        with open('./imagenet.synset.geturls.txt') as file:
            text = []
            for line in file.readlines():                
                text.append(line[:-1])

        urlPool = text
        # Function that divides pool of urls and returns its
        # for choosen part.
        part = self.divide_urls(urlPool, self.divideNum, self.number)

        # Print how many images will be loaded. Ask about it.

        #print('||| Images: {}. ~{} Mb'.format( str(len(part)), str(len(part)*4)))
        #print('||| Are you ready to load? y/n')
        #ready = input()
        #if ready == 'y':

        # List for number of saved images.
        pool = []
        # Create request to save content by its urls
        file = urllib.request.URLopener()
        
        for num, name in enumerate(part):
            print(name)
            try:
                file.retrieve(name,filename = str(self.directory)+'/'+
                              str(self.fname)+str(num)+'.jpg')
                pool.append('>  Done')
            except:
                print('|||  Picture was not saved.')
                pass

        #print('||| Saved: {} pic. from {}.'.format(len(pool),Im_range))
        #else:
        #    print('||| Ok.\n    Exit.')
        #    exit()

# Basic test.
'''
url = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07734017'
#directory = 'Tomato'
fname = 'tomatoes'
divideNumber = 4
number = 3

s = Scrapper(url, fname, divideNumber, number)
s.RUN()
#'''
