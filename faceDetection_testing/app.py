import os
import datetime
# from datetime import timezone
import numpy as np
import cv2
from flask import Flask, request, Response, render_template, session, flash, redirect, \
    url_for, jsonify, abort
import json
import math
#from pymongo import MongoClient
import uuid
import requests

from dateutil.tz import *
from PIL import Image
import sys,traceback
#from Crypto.Cipher import AES
from difflib import SequenceMatcher

from difflib import SequenceMatcher
# from flask_pymongo import PyMongo
# sys.path.append('..')
import base64


import pandas as pd
import base64
import cv2
import time
import random
import multiprocessing
from multiprocessing import Process, Manager
from pathlib import Path

# from RSAI.utils import make_bb, crop_face

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from face import *


app = Flask(__name__)
secret_key='6722838e-2501-4b8c-9162-ba625e9a9784'
app.config['SECRET_KEY'] = secret_key
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


script_address = os.path.dirname(__file__)


results=[]

def get_unique_id():
    return str(uuid.uuid4())


def utc_to_local(utc_dt):
    utc_dt = datetime.datetime.strptime(utc_dt.split(".")[0], "%Y-%m-%d %H:%M:%S")
    return str(utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).split('+')[0]




@app.route('/', methods=['POST'])
def face_verify_pictures():
   
    if(request.method == 'POST'):
        print("FACE VERIFICATION START")
        uid = get_unique_id()
        userId=request.form.get('userId')
        if userId==None:
            userId=''
        url_stat=request.form.get('url_stat')        
 
        if url_stat=='1':
             if(not 'image' in request.form):
                print("Front File  not Found")
                return jsonify([{"transactionId":str(uid),'status':'4002','message': 'Image missing'}]), 200
             try:
                        file=request.form.get('image')
                        file_name=uid+'.png'
                        convertedFile=uid+'.jpg'
                        f_pri = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                        r = requests.get(file, allow_redirects=True)
                        open(f_pri, 'wb').write(r.content)
                        f_convert=os.path.join(app.config['UPLOAD_FOLDER'], convertedFile)
                        im = Image.open(f_pri).convert("RGB")
                        im.save(f_convert,"jpeg")
                        image = cv2.imread(f_convert)
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        grayName=uid+'_gray'+'.jpg'
                        grayFile=os.path.join(app.config['UPLOAD_FOLDER'],grayName)
                        cv2.imwrite(grayFile,gray)
                        frontFile=f_convert
                        frontName=convertedFile
             except:
                    traceback.print_exc(file=sys.stdout)
                    return jsonify({"transactionId":str(uid),'status':'4002','message': 'Image file url is corrupt'}), 200
        else:    
            if(not 'image' in request.files):
                print("Primary File not Found")

                return jsonify({"transactionId":str(uid),'status':'4002','message': 'Image missing'}), 200

            file = request.files['image']
            
            file.filename = uid + ".jpg"

            file_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            file.save(file_name)
            frontFile=file_name
            frontName=file.filename
            fileSize=Path(frontFile).stat().st_size
            if fileSize<2:
                return jsonify({"transactionId":str(uid),'status':'8','message': 'Image file url is empty'}), 200
       # image_pri_upload = s3_client.upload_file(frontFile, clientName, frontName)
        
        face=face_detect(frontFile)
        print(face)
        x=str(datetime.datetime.now())
        if face!=None:
            try:

                #mo = pickle.load(open('/home/invoid/liveness/svm3_2.pickle','rb'))
                #res=predict_image(mo,frontFile)
                ret={"probability":face}
                #     "score":random.randint(1,5)+(random.randint(5,10)/3.786)}
               # rec={"transactionId":uid,"data":ret,"status":"1","message":"Success","userId":userId,
                #     "utcTimestamp":x,"apiId":"live"}
               # db.masterRecord.insert_one(rec)
                y=jsonify({"transactionId":uid,"data":ret,"status":"1","message":"Success","userId":userId,
                     "utcTimestamp":x}), 200
                return y
               # return jsonify({"transactionId":uid,"data":ret,"status":"1","message":"Success","userId":userId,
                #     "utcTimestamp":x}), 200
            except:
                traceback.print_exc(file=sys.stdout)
                y=jsonify({"transactionId":uid,"data":{},"status":"7","message":"face could'nt be detected","userId":userId ,"utcTimestamp":x}),200
                return y
               # return jsonify({"transactionId":uid,"data":{},"status":"7","message":"face could'nt be detected","userId":userId ,"utcTimestamp":x}),200
        else:
                y=jsonify({"transactionId":uid,"data":{},"status":"3","message":"FACE NOT FOUND: Face detector cannot find face in image","userId":userId ,"utcTimestamp":x}),200
                return y
               # return jsonify({"transactionId":uid,"data":{},"status":"3","message":"FACE NOT FOUND: Face detector cannot find face in image","userId":userId ,"utcTimestamp":x}),200
            

    else:
        abort(405)



        

if __name__ == "__main__":
    app.run()
