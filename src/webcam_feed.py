import cv2
from PIL import Image, ImageTk

class WebcamFeed:
    def __init__(self, tk_label, width=960, height=540, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.tk_label = tk_label
        self.width = width
        self.height = height
        self.running = False

    #Initliaze camera
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
        # Mirror the camera
        frame = cv2.flip(frame, 1)
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))

            #Convert to Pillow image object
            img = Image.fromarray(frame)

            #Convert to a format that Tkinter Label widget can display
            imgtk = ImageTk.PhotoImage(image=img)
            self.tk_label.imgtk = imgtk 

            #Update the label image
            self.tk_label.config(image=imgtk)

        # Schedule next update
        self.tk_label.after(15, self._update_frame)