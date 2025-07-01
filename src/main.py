from tkinter import *
from tkinter import ttk
from webcam_feed import WebcamFeed

#Class inheriting from the Tk parent class
class App(Tk):
    def __init__(self):
        #Call the constructor of the parent class, the app class becomes an isntance of the parent class
        super().__init__()
        
        #Configure the window
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.title("Study Distraction App")
        self.geometry("%dx%d" % (self.w, self.h))
        self.background_image = PhotoImage(file = "lofi_background.png")

        
        #Create two frames, one for the study timer and the other for the webcam footage with live detection
        self.webcam_frame = Frame(self, bg='white')
        self.timer_frame = Frame(self, bg='white')

        # Place both frames in the same location. Both run at the same time just one is in the background. We do this instead of .pack so we can continue to run the webcam footage the whole time.
        
        self.webcam_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.timer_frame.place(x=0, y=0, relwidth=1, relheight=1)

        #Setting up the timer frame
        background_label = Label(self.timer_frame, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        title = Label(self.timer_frame, text="Study Timer", font=("Helvetica",36), bg="white", fg = "black")
        title.pack(pady=20)
        btn_to_webcam_frame = Button(self.timer_frame, text="Webcam Live Feed", command=self.show_webcam_frame)
        btn_to_webcam_frame.pack(pady = 20)
        self.remaining_time = 0

        self.countdown_timer()
        btn = Button(self.timer_frame, text='Set Time Countdown', bd='5',
                    command= self.submit)
        btn.pack(side='bottom', pady = self.h/8)

        # In frame2 add a label, button, and webcam feed label
        background_label = Label(self.webcam_frame, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        title2 = Label(self.webcam_frame, text="Webcam Live Feed", font=("Helvetica",36), bg="white", fg = "black")
        title2.pack(pady=20)
        btn_to_timer_frame = Button(self.webcam_frame, text="Study Timer", command=self.show_timer_frame)
        btn_to_timer_frame.pack(pady = 20)

        #Display the webcam footage
        self.video_label = Label(self.webcam_frame)
        self.video_label.place(relx=0.5, rely=0.5, anchor='center')

        # Initialize webcam feed with the label inside frame2
        self.webcam = WebcamFeed(self.video_label)
        
        self.webcam.start()
        

    def show_timer_frame(self):
        self.timer_frame.lift()

    def show_webcam_frame(self):
        self.webcam_frame.lift()
    
    def countdown_timer(self):
        self.hour=StringVar()
        self.minute=StringVar()
        self.second=StringVar()
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
        
        entry_width = int(self.w/4)
        entry_spacing = 10
        entry_height = int(self.h/4)
        
        font_size = int(entry_height/1.1)

        total_width = 3 * entry_width + 2 * entry_spacing
        widget_height = font_size + 20
        start_x = (self.w - total_width) // 2 
        start_y = (self.h - entry_height) // 2
        
        self.hourEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.hour, justify = 'center')
        self.hourEntry.place(x=start_x, y=start_y)

        self.minuteEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.minute, justify = 'center')
        self.minuteEntry.place(x=start_x + entry_width + entry_spacing, y=start_y)

        self.secondEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.second, justify = 'center')
        self.secondEntry.place(x=start_x + 2 * (entry_width + entry_spacing), y=start_y)
        
    def submit(self):
        try:
            self.remaining_time = int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
        except:
            print("Please input the right value")
            return
        
        self.countdown()

    def countdown(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)

            self.hour.set(f"{hours:02d}")
            self.minute.set(f"{mins:02d}")
            self.second.set(f"{secs:02d}")

            self.remaining_time -= 1

            # Call this method again after 1 second (1000 ms)
            self.after(1000, self.countdown)
        else:
            messagebox.showinfo("Time Countdown", "Time's up!")
if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.webcam.stop()