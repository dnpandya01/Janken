import cv2
from model import SignPredictionModel
import numpy as np
import tensorflow as tf

model = SignPredictionModel("RPS_2_Resnet_model.json", "RPS_2_Resnet_model_weight.h5")

font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
        
    def get_frame(self, string):
        _, fr = self.video.read()
        
        crop_fr = fr[100:300, 100:300]
        crop_fr = tf.keras.applications.resnet_v2.preprocess_input(crop_fr)
        roi = cv2.resize(crop_fr, (200, 200))
        pred = model.predict_sign(roi[np.newaxis, :, :])
        
        cv2.rectangle(fr, (100,100), (300,300), (255,0,0), 2)
        cv2.putText(fr, pred, (150, 90), font, 1, (255, 255, 0), 2)
        cv2.putText(fr, string, (350, 250), font, 1, (255, 255, 0), 2)
            
        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes(), roi
    
    def get_res(self, roi):
        pred = model.predict_sign(roi[np.newaxis, :, :])
        return pred