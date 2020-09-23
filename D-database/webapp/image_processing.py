#! /usr/bin/env python3
from PIL import Image
import numpy as np


def img2arr(image_data):
    image = image_data
    image_as_array = np.asarray(image,dtype="int8")
    return image_as_array

def arr2img(array,w,h,c,filename):
    array = np.fromstring(array,dtype='int8').reshape(w, h, c)
    image = Image.fromarray(array,'RGB')
    return image


def crop_image(image):
    image=Image.open(image)
    w,h = image.size
    print(image.size)
    peers = 4
    left,right = 0,w/2
    top,bottom = 0,h/2
    peer_images = []
    images=[]
    for i in range(2):
        for j in range(2):
            cropped_image = image.crop((left,top,right,bottom))
            images.append(cropped_image)
            peer_images.append(img2arr(cropped_image))
            left,right = right,right*2
        left,right = 0,w/2
        top,bottom = bottom,bottom*2
    return images

def join_image(images,w,h):
    peers = 4
    Final_image=Image.new('RGB',(w,h),)
    c=0
    left,right = 0,w/2
    top,bottom = 0,h/2
    for i in range(2):
        for j in range(2):
            Final_image.paste(images[c],(int(left),int(top),int(right),int(bottom)))
            left,right = right,right*2
            c+=1
        left,right = 0,w/2
        top,bottom = bottom,bottom*2
    return Final_image
