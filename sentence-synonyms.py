#!/usr/bin/env python
# coding: utf-8

from gensim.models import KeyedVectors
import os
from tqdm import tqdm

filename = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)


def parse(j):
    j=j.lower()
    if j[-1] in [".",",",";","(",")"]:
        j=j[:-1]
    return j


def createFiles(fname, sub):
    #create output directory
    outdirname = sub+"output"
    path = os.path.join(fname, outdirname)
    try:
        os.mkdir(path) 
    except:
        pass
    #create output files
    outfnames = [os.path.join(path,x) for x in ["out1","out2","out3","out4","out5"]]
    fout = []
    for i in range(len(outfnames)):
        fout.append(open(outfnames[i],"w"))
    return fout


def getSimilarWords(words):
    global num_syn
    global cache
    temp = [[] for _ in range(num_syn)]

    for j in words:
        j = parse(j)
        try:
            try:
                temp = cache[j]
            except:
                #get k most similar words to query
                result = model.most_similar(positive=j, negative=[], topn=num_syn)
                temp = [k[0] for k in result]
                cache[j] = resultw
        except:
            #if not present, duplicate word and add to list
            temp = [j]*num_syn

    for k in range(num_syn):
        s[k].append(' '.join(map(str, temp[k]))) 
    return s


def writetofile(fname,sub):
    fullname = os.path.join(fname,sub)
    f=open(fullname,"r")
    print (fullname)
    dat = []
    for x in f.readlines():
        dat.append(x.strip("\n"))

    fout = createFiles(fname, sub)
    global s
    global it
    
    for p in tqdm(range(len(dat))):
        x=dat[p]
        words = x.split()
        s = getSimilarWords(words)

        #empty out cache after 100k iterations to avoid page faulting bc of large cache size
        it+=1
        if it%100000==0:
            cache = {}

        #write each sentence variant to 5 output files
        for i in range(5):
            fout[i].write("\n".join(s[i]))
            fout[i].write("\n")
        s=[[] for _ in range(num_syn)]

    #close output files
    for i in range(5):
        fout[i].close()

it = 0
num_syn = 5
cache = {}
s=[[] for _ in range(num_syn)]

#change according to directory path name and relative file name within where you want the outputs
fname = "./GYAFC_Corpus/Entertainment_Music/train/"
writetofile(fname,"formal")
writetofile(fname,"informal")
