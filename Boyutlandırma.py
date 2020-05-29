import os
import cv2
import PIL
from pathlib import Path
from PIL import Image
import  glob



def listDirectory(directory, fileExtList):
    fileList = [os.path.normcase(f)
            for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f)
            for f in fileList if os.path.splitext(f)[1] in fileExtList]
    return fileList


def processImage(imageName):
    img = Image.open(imageName)

    saveExt = '.jpg'

    rgb_img = img.convert('RGB')
    rgb_img = rgb_img.resize((60,100),Image.ANTIALIAS)
    print("Boyutlandırıldı...")
    rgb_img.save(os.path.splitext(imageName)[0] + saveExt)
    if os.path.splitext(imageName)[1] != saveExt:
        os.remove(imageName)





if __name__ == '__main__':
    directory = 'Klasör Yolu...'
    exts = ['.jpg','.png']
    imageNames = listDirectory(directory, exts)
    for imageName in imageNames:
        processImage(imageName)