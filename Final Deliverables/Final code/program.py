import threading
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from playsound import playsound
import numpy as np
from keras.models import load_model
from twilio.rest import Client

model = load_model(r"model.h5")
alarm = False
video = cv2.VideoCapture(
    "Forest with fire.mp4")


def startAlarm():
    playsound("audio.mp3")


t2 = threading.Thread(target=startAlarm)


def startPredict():
    alarm = False
    while (1):
        success, frame = video.read()
        if (success == False):
            break
        img1 = cv2.resize(frame, (64, 64))
        y = np.array(img1)
        x = np.expand_dims(y, axis=0)
        pred = model.predict(x)
        list1 = pred.tolist()
        p = int(list1[0][0])
        if (p == 1):
            if not alarm:
                alarm = True
                # account_sid = 'AC0d867d9f5e0579512d7c416374f37f73'
                # auth_token = '98128d00b5c44a698b429671b7bb4861'
                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                #     body='Forest fire Detected, stay alert',
                #     from_='+14246221689',
                #     to='+916385526318')
                t2.start()
                print('Fire Detected')
                print('SMS sent')
        else:
            print('No Fire')

        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


t1 = threading.Thread(target=startPredict)
t1.start()
