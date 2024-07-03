from django.shortcuts import render

# Create your views here.
from deepface import DeepFace
#liveness
import tensorflow as tf
import cv2, numpy, datetime, pygame, keyboard
import xlwings as xw
model = 'liveness.model'
model = tf.keras.models.load_model(model)