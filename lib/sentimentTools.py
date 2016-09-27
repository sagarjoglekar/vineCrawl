
import numpy as np
import json
import os
import sys
from dataUtils import *
import cPickle as pickle


class UnpopularVids:
    
    def get_ANP_ID_List(self , pickleList , nameIdx):
        ANPs = []
        IDs = []
        for line in pickleList:
            ids = line.split(',')[0].split('/')[nameIdx].split('_')[0]
            IDs.append(ids)
            ANPs.append(line.split(',')[1])
        return IDs , ANPs

    def get_vid_senti(self , pickle , index , nameidx):
        oldId = pickle[index].split(',')[0].split('/')[nameidx].split('_')[0]
        seqDict = dict()
        indexList = []
        sequence = pickle[index].split(',')[0].split('/')[nameidx].split('_')[1].split('.')[0]
        seqDict[int(sequence)] = str(pickle[index].split(',')[1])
        indexList.append(index)
        index+=1
        #print index
        while (index < len(pickle) and (pickle[index].split(',')[0].split('/')[nameidx].split('_')[0] == oldId)):
            sequence = pickle[index].split(',')[0].split('/')[nameidx].split('_')[1].split('.')[0]
            seqDict[int(sequence)] = str(pickle[index].split(',')[1])
            indexList.append(index)
            index += 1
        seqDict['indexList'] = indexList
        return seqDict , oldId , index

    #This function maps each video with a dictionary entry that has list of all ANPS per frame
    #and an index list to find them
    def get_VID_ANP_List(self , pickle, nameidx):
        megaDict = dict()
        i = 0
        print len(pickle)
        while i < len(pickle):           
            subDict , postId , i = get_vid_senti(pickle , i , nameidx)
            megaDict[int(postId)] = subDict
        return megaDict


    def pruneMegaDict(self , megadict , filterindices):
        filteredList = dict()
        for entry in megadict:
            commns = set(megadict[entry]['indexList']).intersection(filterindices)
            if len(commns) >= 6:
                filteredList[entry] = megadict[entry]
        return filteredList

    def readJson(self , path):
        f = open(path)
        data = json.loads(f.read())
        return data

    
    
class PopularVids:
    def get_ANP_ID_List(self , pickleList , nameIdx):
        ANPs = []
        IDs = []
        for line in pickleList:
            ids = line.split(',')[0].split('/')[nameIdx].split('_')[0]
            IDs.append(ids)
            ANPs.append(line.split(',')[1])
        return IDs , ANPs

    def get_vid_senti(self , pickle , index , nameidx):
        oldId = pickle[index].split(',')[0].split('/')[nameidx].split('_')[0]
        seqDict = dict()
        indexList = []
        sequence = pickle[index].split(',')[0].split('/')[nameidx].split('_')[1].split('.')[0]
        seqDict[int(sequence)] = str(pickle[index].split(',')[1])
        indexList.append(index)
        index+=1
        #print index
        while (index < len(pickle) and (pickle[index].split(',')[0].split('/')[nameidx].split('_')[0] == oldId)):
            sequence = pickle[index].split(',')[0].split('/')[nameidx].split('_')[1].split('.')[0]
            seqDict[int(sequence)] = str(pickle[index].split(',')[1])
            indexList.append(index)
            index += 1
        seqDict['indexList'] = indexList
        return seqDict , oldId , index

    #This function maps each video with a dictionary entry that has list of all ANPS per frame
    #and an index list to find them
    def get_VID_ANP_List(self , pickle, nameidx):
        megaDict = dict()
        i = 0
        print len(pickle)
        while i < len(pickle):           
            subDict , postId , i = get_vid_senti(pickle , i , nameidx)
            megaDict[int(postId)] = subDict
        return megaDict


    def pruneMegaDict(self , megadict , filterindices):
        filteredList = dict()
        for entry in megadict:
            commns = set(megadict[entry]['indexList']).intersection(filterindices)
            if len(commns) >= 6:
                filteredList[entry] = megadict[entry]
        return filteredList

    def readJson(self , path):
        f = open(path)
        data = json.loads(f.read())
        return data