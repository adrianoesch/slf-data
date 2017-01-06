import numpy as np
import cv2
from collections import Counter

catFrames = {
    663 : [736,770,58,74,27],
    595 : [681,706,49,61,28],
    618 : [684,715,54,69,25]
}

def removeBW(img):
    m = np.mean(img,2)
    s = np.std(img,2)
    unicol = np.std([0,0,250])
    img2 = img
    img2[s<10] = [255,255,255]
    img2[s>unicol] = [255,255,255]
    return img2

def getMostFrequentPixel(img, x1,x2,y1,y2,bw=False):
    f = map(tuple,np.concatenate(img[y1:y2,x1:x2]))
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
    return d.most_common(1)[0][0]

def getCategoryPixels(img):
    global catFrames
    catx1,catx2,caty1,caty2,catDiff = catFrames[img.shape[0]]
    d = { i : getMostFrequentPixel(catx1,catx2,caty1+i*catDiff,caty2+i*catDiff,bw=True) for i in range(5)}
    return d


gif = cv2.VideoCapture('/Users/adrianoesch/Documents/opendata/slf/gifs/raw/20011110_hn1_de_c.gif')
ret,frame = gif.read()
