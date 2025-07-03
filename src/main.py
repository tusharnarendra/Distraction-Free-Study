from tkinter import *
from tkinter import ttk
from webcam_feed import WebcamFeed
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel

#Class inheriting from the Tk parent class
class App(CTk):
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
        canvas = Canvas(self.timer_frame)
        canvas.create_image(0, 0, image=self.background_image, anchor=NW)
        canvas.create_text(self.w // 2, self.h * 0.065, text='Distraction Free Study', fill='white', font=('Segoe UI', 80, 'bold'))
        canvas.create_text(self.w // 2, self.h * 0.225, text='Focus up! Distracted = stopwatch on pause, phone time = extra study time!', fill='white', font=('Segoe UI', 30, 'bold'))

        canvas.pack(fill="both", expand=True)

        # Create the button
        btn_to_webcam_frame = CTkButton(self.timer_frame, text="Webcam Live Feed", 
                                            width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                            hover_color="#FFF0F5", text_color="#211a47", 
                                            font = ('Segoe UI', 20, 'bold'), command=self.show_webcam_frame)
        btn_to_webcam_frame.place(relx = 0.5, rely=0.175, anchor = 'center')
        
        #Start, pause, resume, reset features for the timer
        self.paused = False
        self.remaining_time = 0
        
        self.countdown_timer()
        self.start_btn = CTkButton(self.timer_frame, text='Start', 
                                    width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                    hover_color="#FFF0F5", text_color="#211a47", 
                                    font = ('Segoe UI', 20, 'bold'), command= self.submit)
        self.start_btn.place(relx = 0.14, rely=0.75)
        
        self.pause_btn = CTkButton(self.timer_frame, text='Pause', 
                                    width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                    hover_color="#FFF0F5", text_color="#211a47", 
                                    font = ('Segoe UI', 20, 'bold'), command= self.pause_countdown)
        self.pause_btn.place(relx = 0.34, rely= 0.75)
        self.resume_btn = CTkButton(self.timer_frame, text='Resume', 
                                    width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                    hover_color="#FFF0F5", text_color="#211a47", 
                                    font = ('Segoe UI', 20, 'bold'), command= self.resume_countdown)
        self.resume_btn.place(relx = 0.54, rely = 0.75)
        self.reset_btn = CTkButton(self.timer_frame, text='Reset', 
                                    width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                    hover_color="#FFF0F5", text_color="#100b2e", 
                                    font = ('Segoe UI', 20, 'bold'), command= self.reset)
        self.reset_btn.place(relx = 0.74, rely=0.75)

        #Webcam frame setup
        canvas = Canvas(self.webcam_frame)
        canvas.create_image(0, 0, image=self.background_image, anchor=NW)
        canvas.create_text(self.w // 2, self.h * 0.065, text='Distraction Free Study', fill='white', font=('Segoe UI', 80, 'bold'))
        canvas.pack(fill="both", expand=True)
        
        btn_to_timer_frame = CTkButton(self.webcam_frame, text="Study Timer", 
                                        width = self.w/8, height = self.h/16, fg_color="#f7fcfc", 
                                        hover_color="#FFF0F5", text_color="#211a47", 
                                        font = ('Segoe UI', 20, 'bold'), command=self.show_timer_frame)
        btn_to_timer_frame.place(relx = 0.5, rely=0.175, anchor = 'center')

        #Display the webcam footage
        self.video_label = Label(self.webcam_frame)
        self.video_label.place(relx=0.5, rely=0.55, anchor='center')

        # Initialize webcam feed with the label inside frame2
        self.webcam = WebcamFeed(self.video_label)
        
        self.webcam.start()
        
        # Used in phone detection
        self.time_added = 0
        

    #Place the timer frame above the webcam frame
    def show_timer_frame(self):
        self.timer_frame.lift()

    #Place the webcam frame over the timer frame
    def show_webcam_frame(self):
        self.webcam_frame.lift()
    
    #Countdown feature
    def countdown_timer(self):
        #Create variables for hour, minute and seconds
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
        start_x = (self.w - total_width) // 2 
        
        #Create the text entry boxes for user to configure the duration of the countdown timer
        self.hourEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.hour, justify = 'center')
        self.hourEntry.place(x=start_x, rely=0.5, anchor = 'w')

        self.minuteEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.minute, justify = 'center')
        self.minuteEntry.place(x=start_x + entry_width + entry_spacing, rely=0.5, anchor = 'w')

        self.secondEntry = Entry(self.timer_frame, width=3, font=("Arial", font_size, ""),
                            textvariable=self.second, justify = 'center')
        self.secondEntry.place(x=start_x + 2 * (entry_width + entry_spacing), rely = 0.5, anchor = 'w')
        
    #Retrieving the input from the entry box
    def submit(self):
        try:
            self.remaining_time = int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
        except:
            print("Please input the right value")
            return
        
        self.countdown()

    #Time countdown logic
    def countdown(self):
        #Check if user has paused
        if self.paused:
            return
        #Check if the user has been distracted for 5 or more seconds
        if self.webcam.distracted:
            self.paused = True
            self.pause_btn.config(state='disabled')
            self.resume_btn.config(state='normal')
            self.after(1000, self.check_if_still_distracted)
            return
        #Check if the user has their phone out
        if self.webcam.phone_detected:
            self.paused = True
            self.pause_btn.config(state='disabled')
            self.resume_btn.config(state='normal')
            self.after(1000, self.check_if_phone_detected)
            return

        #Update the time
        if self.remaining_time >= 0:
            self.remaining_time += self.time_added
            self.time_added = 0             
            #Calculate the hours, mins,seconds format of the total remaining seconds
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)

            self.hour.set(f"{hours:02d}")
            self.minute.set(f"{mins:02d}")
            self.second.set(f"{secs:02d}")
            
            #Reduce the timer by 1
            self.remaining_time -= 1

            # Call this method again after 1 second (1000 ms)
            self.after(1000, self.countdown)
        else:
            messagebox.showinfo("Time Countdown", "Time's up!")


    def pause_countdown(self):
        self.paused = True
        self.resume_btn.config(state='normal') 
        self.pause_btn.config(state='disabled')
        
    def resume_countdown(self):
        self.paused = False
        self.pause_btn.config(state='normal')
        self.resume_btn.config(state='disabled')
        self.countdown()
    
    #Checking to see whether to resume the timer or not, and disabling either paused or resume based on if the timer is running or not
    def check_if_still_distracted(self):
        if not self.webcam.distracted:
            self.paused = False
            self.pause_btn.config(state='normal')
            self.resume_btn.config(state='disabled')
            self.countdown()
        else:
            self.after(1000, self.check_if_still_distracted)
    
    #Function to check if the user still has their phone out and adding 10 seconds to the total remaining time on the timer for every second the phone is detected
    def check_if_phone_detected(self):
        if not self.webcam.phone_detected:
            self.paused = False
            self.pause_btn.config(state='normal')
            self.resume_btn.config(state='disabled')
            self.countdown()
        else:
            self.time_added += 10
            self.after(1000, self.check_if_phone_detected)
    
    #Reset the countdown display
    def reset(self):
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.webcam.stop()