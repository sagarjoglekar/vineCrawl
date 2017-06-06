import os
import sys
import multiprocessing as mp
from shutil import copyfile



root = ""

scoredFile = root + "insta6000.csv"

sourceFolder = "insta6000Samples/"
newFolder = root + "insta6000remaining/"



def readcsv(fileName):
    with open(fileName) as g:
        featureLines = g.readlines()
    return featureLines

def getProcessed(filename , sep):
    lines = readcsv(filename)
    processed = []
    for line in lines: 
        comps = line.split(sep)
        processed.append(comps[0])
    return processed

def findUnprocessed(fileList , Processed):
    unProcessed = list(set(fileList) - set(Processed))
    print len(unProcessed)
    return unProcessed

def copyList(listOfFiles):
    for f in listOfFiles:
        src = sourceFolder + f
        dst = newFolder + f
        copyfile(src , dst)
    
if __name__ == "__main__":
    
    procFiles = getProcessed(scoredFile,"|")
    allFiles = os.listdir(sourceFolder)
    
    unproc = findUnprocessed(allFiles,procFiles)
    copyList(unproc)
    
    
                         
                        


