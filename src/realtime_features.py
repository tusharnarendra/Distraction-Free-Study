
"""
This file does the same as face_features.py in the features folder. This has been reorganized to a class to aid the real time detection:
Descriptive comments can be found in the original file.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
from tqdm import tqdm


class xFeatures:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='../features/face_landmarker.task')
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def get_landmark_coords(self, landmarks, idx):
        lm = landmarks[idx]
        return np.array([lm.x, lm.y])

    def extract_features(self, landmarks):
        nose_tip_index = 1
        left_eye_indices = [33, 133]
        right_eye_indices = [362, 263]
        left_eye_iris_index = 468
        right_eye_iris_index = 473
        left_ear_index = 234
        right_ear_index = 454

        nose = self.get_landmark_coords(landmarks, nose_tip_index)
        left_eye = np.mean([self.get_landmark_coords(landmarks, i) for i in left_eye_indices], axis=0)
        right_eye = np.mean([self.get_landmark_coords(landmarks, i) for i in right_eye_indices], axis=0)
        left_eye_iris = self.get_landmark_coords(landmarks, left_eye_iris_index)
        right_eye_iris = self.get_landmark_coords(landmarks, right_eye_iris_index)
        left_ear = self.get_landmark_coords(landmarks, left_ear_index)
        right_ear = self.get_landmark_coords(landmarks, right_ear_index)

        def dist(a, b):
            return np.linalg.norm(a - b)

        yaw = right_eye[0] - left_eye[0]
        pitch = nose[1] - (left_eye[1] + right_eye[1]) / 2

        nose_to_left_eye = dist(nose, left_eye)
        nose_to_right_eye = dist(nose, right_eye)
        ear_distance = dist(left_ear, right_ear)
        eye_distance = dist(left_eye, right_eye)

        face_detected = 1

        features = [nose[0], nose[1],
                    left_eye[0], left_eye[1],
                    right_eye[0], right_eye[1],
                    left_ear[0], left_ear[1],
                    right_ear[0], right_ear[1],
                    left_eye_iris[0], left_eye_iris[1],
                    right_eye_iris[0], right_eye_iris[1],
                    yaw, pitch,
                    nose_to_left_eye, nose_to_right_eye,
                    ear_distance, eye_distance,
                    face_detected]

        return features
    
    #Slightly adapted from previous version as this only process a singular image/frame
    def process_frame(self, img):
        if img is None:
            return np.array([0]*21)
        
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        result = self.detector.detect(mp_image)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            features = self.extract_features(landmarks)
        else:
            features = [0]*21

        return np.array(features)
