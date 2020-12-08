
from absl import app, flags, logging
import cv2
import os
import numpy as np
import csv 
import time
import pandas as pd

#from flask import Flask, request, Response, render_template, session, flash, redirect, \
 #   url_for, jsonify, abort
#import json
import math
#from pymongo import MongoClient
import os
from csv import writer 
from PIL import Image
from flask import Flask, request, Response, render_template, session, flash, redirect, \
    url_for, jsonify, abort
#from modules.models import RetinaFaceModel


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
logger = tf.get_logger()
logger.disabled = True
logger.setLevel(logging.FATAL)

#tells which url should be linked with that particular function 
model = tf.keras.models.load_model('my_model')


def face_detect(img_path):

    ###############################################################################
    def pad_input_image(img, max_steps):
        #pad image to suitable shape
        img_h, img_w, _ = img.shape

        img_pad_h = 0
        if img_h % max_steps > 0:
            img_pad_h = max_steps - img_h % max_steps

        img_pad_w = 0
        if img_w % max_steps > 0:
            img_pad_w = max_steps - img_w % max_steps

        padd_val = np.mean(img, axis=(0, 1)).astype(np.uint8)
        img = cv2.copyMakeBorder(img, 0, img_pad_h, 0, img_pad_w,
                                 cv2.BORDER_CONSTANT, value=padd_val.tolist())
        pad_params = (img_h, img_w, img_pad_h, img_pad_w)

        return img, pad_params


    def recover_pad_output(outputs, pad_params):
      #  recover the padded output effect
        img_h, img_w, img_pad_h, img_pad_w = pad_params
        recover_xy = np.reshape(outputs[:, :14], [-1, 7, 2]) * \
            [(img_pad_w + img_w) / img_w, (img_pad_h + img_h) / img_h]
        outputs[:, :14] = np.reshape(recover_xy, [-1, 14])

        return outputs
      
    try:
        img_raw = cv2.imread(img_path)
        img_height_raw, img_width_raw, _ = img_raw.shape
        img = np.float32(img_raw.copy())


        #if img.shape[0]<250 and img.shape[0]>180:
         #   img = cv2.resize(img, (0, 0), fx=0.3,
        #                                    fy=0.3,
         #                                   interpolation=cv2.INTER_LINEAR)
        if img.shape[0]>=8500:
            img = cv2.resize(img, (0, 0), fx=0.2,
                                            fy=0.2,
                                            interpolation=cv2.INTER_LINEAR)

        elif img.shape[0]<=250:
            img = cv2.resize(img, (0, 0), fx=0.38,
                                            fy=0.38,
                                            interpolation=cv2.INTER_LINEAR)
        else:
            img = cv2.resize(img, (0, 0), fx=0.28,
                                            fy=0.28,
                                            interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # pad input image to avoid unmatched shape problem
        img, pad_params = pad_input_image(img, max_steps=32)

        # run model
        outputs = model(img[np.newaxis, ...]).numpy()

        # recover padding effect
        outputs = recover_pad_output(outputs, pad_params)
    
   
        

        if len(outputs)>0:
            outputs=outputs.T
            percent=max(outputs[-1])
            if percent>0.5:
                return percent*100
                
                
                
            else:
                
                return None
        else:
            
            return None

    except:
        return None


