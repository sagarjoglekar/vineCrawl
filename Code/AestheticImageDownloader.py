import os
import sys
from subprocess import call
import imghdr

dataFile = "/datasets/sagarj/aestheticImages/photonet_dataset.txt"
imageDir = "/datasets/sagarj/aestheticImages/images_6_and_above/"

baseURL = "http://gallery.photo.net/photo/"

rating_thresh = 6.0

def verify(imagePath):
    form = imghdr.what(imagePath)
    print form
    if form == 'jpeg':
        return True
    else :
        return False

def filterList(dataLines, meanRating):
    imageId = []
    for line in dataLines:
        comps = line.split(" ")
        if float(comps[3]) > meanRating:
            imageId.append(comps[1])
    return imageId

def downloadImage(imageId , imageDir):
    downloadUrl = baseURL + imageId + "-md.jpg"
    imageName = imageDir + imageId + ".jpg"
    argsVideo = ['curl','-o' , imageName , downloadUrl]
    call(argsVideo)
    return imageName

if __name__=="__main__":
    dataLines = []
    with open(dataFile) as f:
        dataLines = f.readlines()

    if not os.path.exists(imageDir):
        print "Download Dir missing, Making one"
        os.makedirs(imageDir)

    filteredImages = filterList(dataLines , rating_thresh)
    print "Downloading %d images from photoNet!!! "%len(filteredImages)

    for image in filteredImages:
        name = downloadImage(image,imageDir)
        if not verify(name):
            try:
                os.remove(name)
            except OSError:
                pass

    print "Verifying final contents of %s" %(imageDir)
    downloaded = os.listdir(imageDir)
    count = 0
    failed = []
    for image in downloaded:
        sanity = verify(imageDir + image)
        if sanity:
            count+=1
        else:
            failed.append(image)

    if count == len(downloaded):
        print "All downloaded images are Sane"
    else:
        print "Found some malformed images, Cleaning them!! "
        print failed
        for img in failed:
            try:
                os.remove(imageDir + img)
            except OSError:
                pass




