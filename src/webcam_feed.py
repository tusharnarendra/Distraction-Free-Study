import cv2
from PIL import Image, ImageTk
from realtime_features import xFeatures
from mediapipe_visualization import draw_landmarks_on_image
import joblib
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from ultralytics import YOLO

class WebcamFeed:
    def __init__(self, tk_label, width=960, height=540, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.tk_label = tk_label
        self.width = width
        self.height = height
        self.running = False
        self.classifier = joblib.load('../classification_models/random_forest_model.pkl')
        self.sc = joblib.load('../classification_models/X_scaler.pkl')
        self.extractor = xFeatures()
        self.model = YOLO('yolov8n.pt') 
    #Initialize camera
    def start(self):
        self.running = True
        self._update_frame()

    #Terminate camera
    def stop(self):
        self.running = False
        self.cap.release()

    def _update_frame(self):
        if not self.running:
            return

        #Reading frame
        ret, frame = self.cap.read()

        if ret:
            #Collect features from current image
            features = self.extractor.process_frame(frame)
            
            if np.any(features): 
                scaled_features = self.sc.transform([features]) 
                prediction = self.classifier.predict(scaled_features)
                print("Prediction:", prediction)
            else:
                prediction = None
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
            
            #Use open CV to detect mobile phone
            results = self.model(frame)[0]
            for box in results.boxes:
                classID = int(box.cls[0])
                label = self.model.names[classID]
                if label.lower() in ['cell phone', 'mobile phone', 'telephone']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            #Visualize the landmarks on image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection_result = self.extractor.detector.detect(mp_image)
            
            prediction_dict = {0:"Focused", 1:"Focused", 2:"Distracted"}
            if detection_result.face_landmarks:
                annotated_image = draw_landmarks_on_image(frame, detection_result)
                #Display the current prediction
                if prediction is not None:
                    cv2.rectangle(annotated_image, (25, 20), (370, 65), (255,255,255), -1)
                    cv2.putText(annotated_image, 
                                f"Prediction: {prediction_dict[prediction[0]]}", 
                                (30, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, 
                                (0, 0, 0),
                                2, 
                                cv2.LINE_AA)
            else:
                annotated_image = frame
                cv2.rectangle(frame, (540, 20), (940, 65), (255,255,255), -1)
                cv2.putText(frame, "Not Present: Distracted!", (550,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            
            #Convert to Pillow image object
            img = Image.fromarray(annotated_image)
            
            #Convert to a format that Tkinter Label widget can display
            imgtk = ImageTk.PhotoImage(image=img)
            self.tk_label.imgtk = imgtk 

            #Update the label image
            self.tk_label.config(image=imgtk)

        # Schedule next update
        self.tk_label.after(17, self._update_frame)