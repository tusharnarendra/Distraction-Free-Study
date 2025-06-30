from tkinter import *
from tkinter import ttk
from webcam_feed import WebcamFeed

# Initializing the window
window = Tk()
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.title("Study Distraction App")
window.geometry("%dx%d" % (w, h))
window.configure(background='white')

# Title label
title = Label(window, text="Study Timer", font=("Helvetica",36), bg="white", fg = "black")
title.pack(side="top", pady=30)

# Webcam display label
video_label = Label(window)
video_label.pack()

#Display webcam footage
webcam = WebcamFeed(video_label)
webcam.start()

# Main loop
window.mainloop()

#Stop the webcam once app is closed
webcam.stop()
