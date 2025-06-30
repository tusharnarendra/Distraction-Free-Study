import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe_visualization import draw_landmarks_on_image, plot_face_blendshapes_bar_graph
import numpy as np
import os
from tqdm import tqdm  # <-- added

# Creating the face landmarker object
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

#helper function to convert landmark object to a 2D numpy array
def get_landmark_coords(landmarks, idx):
    lm = landmarks[idx]  
    return np.array([lm.x, lm.y])

#Function that extracts the features of interest 
def extract_features(landmarks):
    # Key landmarks indices determined from MediaPipe Face Mesh landmark map
    nose_tip_index = 1
    left_eye_indices = [33, 133]
    right_eye_indices = [362, 263]
    left_eye_iris_index = 468
    right_eye_iris_index = 473
    left_ear_index = 234
    right_ear_index = 454

    # Extracting the points corresponding to the landmarks above
    nose = get_landmark_coords(landmarks, nose_tip_index)
    left_eye = np.mean([get_landmark_coords(landmarks, i) for i in left_eye_indices], axis=0)
    right_eye = np.mean([get_landmark_coords(landmarks, i) for i in right_eye_indices], axis=0)
    left_eye_iris = get_landmark_coords(landmarks, left_eye_iris_index)
    right_eye_iris = get_landmark_coords(landmarks, right_eye_iris_index)
    left_ear = get_landmark_coords(landmarks, left_ear_index)
    right_ear = get_landmark_coords(landmarks, right_ear_index)

    # Distance function
    def dist(a, b):
        return np.linalg.norm(a - b)

    # Calculate features

    #Rotation around y-axis
    yaw = right_eye[0] - left_eye[0]

    #Rotation around x-axis
    pitch = nose[1] - (left_eye[1] + right_eye[1]) / 2  # vertical difference

    #Additional features
    nose_to_left_eye = dist(nose, left_eye)
    nose_to_right_eye = dist(nose, right_eye)
    ear_distance = dist(left_ear, right_ear)
    eye_distance = dist(left_eye, right_eye)

    face_detected = 1

    #Creting the feature list
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


#Detecting the facial landmarks
parent_folder = '../dataset'

#The features list
X = []
failed_detections = []

# Loop through each item in the parent folder
for folder_name in os.listdir(parent_folder):
    folder_path = os.path.join(parent_folder, folder_name)

    # Check if this item is a directory (folder)
    if os.path.isdir(folder_path):
        # List files in this folder
        frame_files = sorted(os.listdir(folder_path))

        # Wrap with tqdm for progress bar
        for file_name in tqdm(frame_files, desc=f"Processing {folder_name}"):
            img_path = os.path.join(folder_path, file_name)
            image = cv2.imread(img_path)
            if image is None:
                failed_detections.append(file_name)
                continue

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            result = detector.detect(mp_image)

            if result.face_landmarks:
                landmarks = result.face_landmarks[0]
                features = extract_features(landmarks)
            else:
                failed_detections.append(file_name)
                features = [0]*21 
            X.append(features)

#Convert to numpy array
X = np.array(X)

#Save the features list
np.save('features.npy', X)

#Handle faield detections
with open("failed_detections.txt", "w") as f:
    for filename in failed_detections:
        f.write(filename + "\n")
