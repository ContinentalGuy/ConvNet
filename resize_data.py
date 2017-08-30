import cv2
import os
import argparse

# Parse arguments from command line.
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--src', help = 'Source folder')
parser.add_argument('-d', '--dst', help = 'Destination folder')
parser.add_argument('-r', '--resize', help = 'Scale value')
args = vars(parser.parse_args())

# Function that resizes images from source folder and
# saves into destination folder.
def resize(folder_with_images, xS, yS, folder_for_resized):
    for image_link in os.listdir(folder_with_images):
        print(image_link)
        try:
            image = cv2.imread('{}/{}'.format(folder_with_images, image_link))
            resized_image = cv2.resize(image, (xS, yS), interpolation = cv2.INTER_CUBIC)
            cv2.imwrite('{}/{}'.format(folder_for_resized, image_link), resized_image)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    
    folder_with_images = str(args['src'])
    folder_for_resized = str(args['dst'])
    scale = str(args['resize'])
    try:
        os.mkdir(folder_for_resized)
    except:
        pass

    xS,yS = [scale,scale]

    resize(folder_with_images, xS, yS, folder_for_resized)
