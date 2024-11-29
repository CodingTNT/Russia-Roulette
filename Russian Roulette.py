import tkinter as tk
from PIL import Image, ImageTk
import pygame

class NeedleSpinner:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True) 
        self.master.bind("<Escape>", self.exit_fullscreen) 

        
        pygame.mixer.init()

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        self.canvas = tk.Canvas(master, width=screen_width, height=screen_height, bg='white')
        self.canvas.pack()

        
        self.background_img = Image.open("Background.png")
        self.background_img = self.background_img.resize((screen_width, screen_height)) 
        self.background_tk = ImageTk.PhotoImage(self.background_img)

        self.revolver_img = Image.open("Revolver.png")
        self.revolver_img = self.revolver_img.resize((480, 480))  
        self.revolver_tk = ImageTk.PhotoImage(self.revolver_img)

        self.needle_img = Image.open("Needle.png")
        self.needle_img = self.needle_img.resize((160, 160)) 
        self.needle_tk = ImageTk.PhotoImage(self.needle_img)

        
        self.axis_img = Image.open("Axis.png")
        self.axis_img = self.axis_img.resize((50, 50))  
        self.axis_tk = ImageTk.PhotoImage(self.axis_img)

        self.bg_image = self.canvas.create_image(screen_width / 2, screen_height / 2, image=self.background_tk)

        self.canvas.create_image(screen_width / 2, screen_height / 2, image=self.revolver_tk)

        self.needle = self.canvas.create_image(screen_width / 2, screen_height / 2, image=self.needle_tk)

        self.axis = self.canvas.create_image(screen_width / 2, screen_height / 2, image=self.axis_tk)

        self.angle = 0
        self.spin_speed = 0 
        self.max_speed = 40 
        self.acceleration = 0.5  
        self.is_running = False  

        self.start_button = tk.Button(
            master, 
            text="Start", 
            font=("Arial", 24), 
            bg="lightgray", 
            fg="black", 
            command=self.toggle_spin
        )
        self.start_button.place(relx=0.5, rely=0.9, anchor="center") 

        self.you_img = Image.open("You.png")
        self.you_img = self.you_img.resize((1200, 200)) 
        self.you_tk = ImageTk.PhotoImage(self.you_img)
        self.you_image = None  

        self.gun_img = Image.open("Gun.png")
        self.gun_img = self.gun_img.resize((300, 500))  
        self.gun_tk = ImageTk.PhotoImage(self.gun_img)
        self.gun_image = None
        self.gun_position_y = screen_height  

        self.spark_img = Image.open("Spark.png")
        self.spark_img = self.spark_img.resize((300, 300)) 
        self.spark_tk = ImageTk.PhotoImage(self.spark_img)
        self.spark_image = None 

        self.roulette_sound = pygame.mixer.Sound("roulette.aiff")

    def toggle_spin(self):

        if not self.is_running: 
            self.is_running = True
            self.start_button.config(text="Stop", bg="red", fg="white")  
            self.accelerate_needle() 
            self.roulette_sound.play(loops=-1, fade_ms=3000)  
        else: 
            self.is_running = False
            self.start_button.config(text="Start", bg="lightgray", fg="black")  
            self.start_button.place_forget()  
            self.decelerate_needle() 

    def accelerate_needle(self):

        if self.is_running and self.spin_speed < self.max_speed:
            self.spin_speed += self.acceleration  
            self.update_needle()
            self.master.after(10, self.accelerate_needle)  
        elif self.is_running: 
            self.update_needle()
            self.master.after(10, self.update_needle)

    def decelerate_needle(self):

        if not self.is_running and self.spin_speed > 0:
            self.spin_speed -= self.acceleration 
            self.update_needle()
            self.master.after(10, self.decelerate_needle)  
        elif not self.is_running and self.spin_speed <= 0:  
            self.spin_speed = 0
            self.roulette_sound.stop() 
            self.master.after(500, self.show_you_image) 
            self.master.after(1500, self.show_gun_image)  

    def update_needle(self):

        self.angle = (self.angle + self.spin_speed) % 360

        rotated_needle = self.needle_img.rotate(self.angle, resample=Image.BICUBIC)
        self.needle_tk = ImageTk.PhotoImage(rotated_needle)
        self.canvas.itemconfig(self.needle, image=self.needle_tk) 

        if self.is_running and self.spin_speed == self.max_speed:
            self.master.after(10, self.update_needle)

    def show_you_image(self):
       
        if self.you_image is None:
            self.you_image = self.canvas.create_image(
                self.master.winfo_screenwidth() / 2, 
                self.master.winfo_screenheight() / 2, 
                image=self.you_tk
            )
            self.canvas.itemconfig(self.you_image, state="hidden") 

        self.canvas.itemconfig(self.you_image, state="normal") 
        self.fade_in(self.you_image)

    def show_gun_image(self):

        if self.gun_image is None:
            self.gun_image = self.canvas.create_image(
                self.master.winfo_screenwidth() / 2, 
                self.gun_position_y, 
                image=self.gun_tk
            )

        
        if self.gun_position_y > self.master.winfo_screenheight() / 2:
            self.gun_position_y -= 20  
            self.canvas.coords(self.gun_image, self.master.winfo_screenwidth() / 2, self.gun_position_y)
            self.master.after(30, self.show_gun_image) 
        else:
           
            pygame.mixer.music.load("shot.wav")  
            pygame.mixer.music.play()  
            self.show_spark_image() 

    def show_spark_image(self):
        
        if self.spark_image is None:
            self.spark_image = self.canvas.create_image(
                self.master.winfo_screenwidth() / 2, 
                self.master.winfo_screenheight() / 3, 
                image=self.spark_tk
            )
            self.canvas.itemconfig(self.spark_image, state="hidden")  

        self.canvas.itemconfig(self.spark_image, state="normal") 
        self.fade_in(self.spark_image)

    def fade_in(self, item, alpha=0):
        
        if alpha < 255:
            alpha += 5
            self.master.after(30, self.fade_in, item, alpha) 
            self.canvas.itemconfig(item, fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}")
    
    def exit_fullscreen(self, event=None):
        
        self.master.attributes('-fullscreen', False)
        self.master.quit()

    def clear_screen(self):
        
        self.canvas.delete("all")
        self.canvas.config(bg="black") 


root = tk.Tk()
game = NeedleSpinner(root)
root.mainloop()
