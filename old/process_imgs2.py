import numpy as np
import imutils
import cv2
from collections import Counter
import os
from random import sample
import pandas as pd
from string import ascii_uppercase as upper

def removeBW(img):
    m = np.mean(img,2)
    s = np.std(img,2)
    unicol = np.std([0,0,250])
    img2 = img.copy()
    img2[m<80] = [255,255,255]
    img2[s<15] = [255,255,255]
    img2[s>unicol] = [255,255,255]
    img2[(img2[:,:,1]>250)&(img2[:,:,0]<180)] = [255,255,255]
    return img2

def getMostFrequentPixel(img, x1,x2,y1,y2,bw=False,n=1):
    f = map(tuple,np.concatenate(np.stack(img[y1:y2,x1:x2,])))
    d = Counter(f)
    if bw:
        try:
            del d[(255,255,255)]
        except:
            pass
        try:
            del d[(0,0,0)]
        except:
            pass
    if n==1:
        return d.most_common(1)[0][0]
    else:
        return d.most_common(n)

def showCoord(img,coordStr):
    x1,x2,y1,y2 = coordDic[coordStr]
    cv2.imshow('',img[y1:y2,x1:x2])

def getHist(img,coordStr=None,removeWhite=False,returnWhite=False):
    global coordDic
    if coordStr is None:
        hist = cv2.calcHist([img], [0,1,2], None, [32,32,32],[0,256,0,256,0,256])
    else:
        v = coordDic[coordStr]
        hist = cv2.calcHist([img[v[2]:v[3],v[0]:v[1]]], [0,1,2], None, [32,32,32],[0,256,0,256,0,256])
    if returnWhite:
        nWhite = hist[31,31,31]
    if removeWhite:
        hist[31,31,31]=0
    hist = cv2.normalize(hist).flatten()
    if returnWhite:
        return nWhite, hist
    else:
        return hist

def getCategoryHists(img):
    global catFrames
    catx1,catx2,caty1,caty2,catDiff = catFrames[img.shape[0]]
    white = np.ones((24,24,3),np.uint8)*255
    d = [ (i, getHist(img[caty1+i*catDiff:caty2+i*catDiff,catx1:catx2]) ) for i in range(5)]
    d.append( ('NA',getHist(white) ) )
    return d

def findSwissContourImg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayShape = gray.shape
    i=0
    oldMaxVal = 0
    while True:
        gt = imutils.resize(gray,width=grayShape[1]-i*5)
        gtCanny = cv2.Canny(gt,50,100)
        result = cv2.matchTemplate(gtCanny, templateCanny, cv2.TM_CCOEFF)
        a, maxVal, t, maxLoc = cv2.minMaxLoc(result)
        # print maxVal, maxLoc
        if maxVal > oldMaxVal:
            oldMaxVal = maxVal
            oldMaxLoc = maxLoc
            i=i+1
            continue
        else:
            break
    newImg = imutils.resize(img,width=img.shape[1]-(i-1)*5)
    swiss = newImg[oldMaxLoc[1]:oldMaxLoc[1]+template.shape[0], oldMaxLoc[0]:oldMaxLoc[0]+template.shape[1],:]
    # cv2.rectangle(newImg, (oldMaxLoc[0], oldMaxLoc[1]),
    # 				(oldMaxLoc[0] + template.shape[1], oldMaxLoc[1] + template.shape[0]), (0, 0, 255), 2)
    # cv2.imshow('',newImg)
    return swiss

def partition(img):
    nd = dict(coordDic)
    for k,v in nd.items():
        nd[k] = img[v[2]:v[3],v[0]:v[1]]
    return nd

def setGlobals():
    global imgDir
    global homeDir
    global catFrames
    global template
    global templateGray
    global templateCanny
    global coordDic
    imgDir = '/Users/adrianoesch/Documents/opendata/slf/gifs/'
    homeDir = '/Users/adrianoesch/Documents/opendata/slf/'
    catFrames = {
        662 : [736,770,58,74,27],
        663 : [736,770,58,74,27],
        595 : [681,706,49,61,28],
        617 : [684,715,54,69,25],
        632 : [702,734,55,70,26],
        623 : [692,723,55,70,25]
    }
    cols = {0: (255, 255, 204), 1: (255, 204, 153), 2: (255, 153, 102), 3: (204, 102, 51), 4: (204, 51, 51), 'NA': None}
    cellSize=24
    x,template = cv2.VideoCapture(homeDir+'template_small.png').read()
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    templateGrid = np.array(template)
    templateGrid[[i for i in range(0,528,cellSize)],] = [50,50,50]
    templateGrid[:,[i for i in range(0,816,cellSize)]] =[50,50,50]
    templateCanny = cv2.Canny(template,50,100)
    coordDic = {a+str(b): (j*cellSize,(j+1)*cellSize,i*cellSize,(i+1)*cellSize) for i,a in enumerate(upper[:22]) for j,b in enumerate(range(1,35))}

def getDate(f):
    date = f.split('_')[0]
    y = date[:4]
    m = date[4:6]
    d = date[6:]
    return '-'.join([y,m,d])

def getOverlayMap(d,alpha=0.6,draw=False):
    t = templateGrid.copy()
    for k,v in coordDic.items():
        if d[k] is None or d[k] is 'NA':
            continue
        cv2.rectangle(t,(v[0]+1,v[2]+1),(v[1]-1,v[3]-1),color=cols[d[k]],thickness=-1)
    o = templateGrid.copy()
    cv2.addWeighted(o, alpha, t, 1 - alpha,0, t)
    if draw:
        cv2.imshow('',t)
    return o

def findCat(img,v,hists):
    x1,x2,y1,y2 = v
    img = img[v[2]:v[3],v[0]:v[1]]
    nWhite, hist = getHist(img,removeWhite=True,returnWhite=True)
    if nWhite > 288:
        return 'NA'
    corrs = [cv2.compareHist(hist,hists[i][1],cv2.cv.CV_COMP_CORREL) for i in range(len(hists))]
    return hists[corrs.index(max(corrs))][0]


def fileHandler(f):
    x,img = cv2.VideoCapture(imgDir+f).read()
    date = getDate(f)
    s = findSwissContourImg(img)
    s = removeBW(s)
    hists = getCategoryHists(img)
    d = [(date,k,findCat(s,v,hists)) for k,v in coordDic.items()]
    # o=getOverlayMap(d,draw=True)
    return d

if __name__=='__main__':
    setGlobals()
    files = os.listdir(imgDir)
    files.remove('.DS_Store')
    r = map(fileHandler,files)
    d = pd.DataFrame([j for i in r for j in i])
    d.to_csv(homeDir+'rawData.csv',index=False)
