"""
TODO: handle library
1. opencv
2. os
3. numpy

TODO: handle data structure
1. handle path ke dataset
2. jika tidak ada pathnya print("dataset path not defined")
3. Ambil gambar dari dataset menggunakan path tersebut
4. gunakan logika for loop untuk membaca gambar
5. ambil label dari dataset lalu normalisasi
6. gunakan algoritma patch bacth training

TODO:patch batch training
1. dalam 1 gambar pecah gambar tersebut menjadi beberapa bagian dengan resolusi 640x640
Probelem:
1. gambar yang di pecah banyak yang non label 
"""
import os
import numpy as np
import glob
import cv2 as cv

#handle path
dataset_path = ""
label_path = ""
if os.path.exists(dataset_path):
    img=cv.imread(dataset_path)
else:
    print("dataset path not defined")

#handle label
boxes=[]
if os.path.exists(label_path):
    with open(label_path, 'r') as f:
        for line in f.readlines():
            cls,x,y,w,h=map(line.strip().split(' '))
            x1=(x-w/2)*img.shape[1]
            x2=(x+w/2)*img.shape[1]
            y1=(y-h/2)*img.shape[0]
            y2=(y+h/2)*img.shape[0]
        boxes.append([cls,x1,y1,x2,y2])
else:
    print("label path not defined")
