from cv2 import imread
import cv2
import os
from ynet import get_ynet
import keras
import numpy as np

def save(data, i, path):
    data = data.astype('float32')
    cv2.imwrite(path + str(i) + ".jpg",data)

def getImage(i, source, main_dir, ext, size):
    name = str(i) + ext
    #print(main_dir + source + name)

    path = os.path.join(main_dir, source , name)
    print(path)
    img = imread(path, 0)
    img = cv2.resize(img, size)
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype('float32')
    img /= 255
    return img

def ok(start,videoType):
    i = start
    dir = '..\\testing\\with_feedback\\' + str(videoType) + '\\y\\'
    frame_ext = '.jpg'
    audio_ext = '.png'
    x0 = getImage(i-1      , '', dir, frame_ext, (224, 224))
    x1 = getImage(i        , '', dir, frame_ext, (224, 224))
    x2 = getImage(int(i/30), '', dir, audio_ext, (224, 224))
    x3 = getImage(i        , '', dir, frame_ext, (224, 224))
    print("-------------------------------")

    x0 = x0.reshape((1, x0.shape[0], x0.shape[1], x0.shape[2]))
    x1 = x1.reshape((1, x1.shape[0], x1.shape[1], x1.shape[2]))
    x2 = x2.reshape((1, x2.shape[0], x2.shape[1], x2.shape[2]))
    x3 = x3.reshape((1, x3.shape[0], x3.shape[1], x3.shape[2]))


    return [x1, x2], x3, x1, x2, x0

def test():
    md = get_ynet()
    frames = 200
    n = int((frames + 2)/4)
    md.load_weights('..\\checkpoints\\ynet1.hdf5')
    for videoType in range(1,2):
        tag = '..\\testing\\with_feedback\\' + str(videoType) + '\\y\\'
        for start in range(1,n):
            for abc in range(1,3):
                h, hy, x1, x2, x0 = ok(start*4 - 3 + abc,videoType)
                
                hp = md.predict(h)
                
                if not os.path.exists(tag):
                    os.makedirs(tag)
                
                i = start*4 - 3 + abc
                for p, g in zip(hp, hy):
                    p *= 255;
                    g *= 255;
                    x0 *= 255;
                    x1 *= 255;
                    save(p.reshape((224, 224)), i+1, tag) #output
                    save(x1.reshape((224, 224)), i, tag)#input1
                    save(x0.reshape((224, 224)), i-1, tag)#input0
                    i += 1
test()
