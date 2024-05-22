# Import all the libraries
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# Generate a timestamp for the filename
current_datetime = datetime.now()
current_date = current_datetime.date()
current_time = current_datetime.strftime("%H-%M-%S")  # Use hyphens to avoid issues in filenames
time_stamp = f"{current_date}_{current_time}"
print(time_stamp)

class Watermarker:
    def __init__(self):
        self.base_image = None
        self.new_image = None
        
    def select_img(self, base_image_path):
        self.base_image = Image.open(base_image_path)
        self.new_image = self.base_image.copy()
        self.w, self.h = self.base_image.size


    def add_text_watermark(self, user_text):
        if self.base_image:
            x, y = int(self.w//4), int(self.h//6)
            draw = ImageDraw.Draw(self.new_image)
            font_size = min(self.w, self.h) // 10
            img_font = ImageFont.truetype("arial.ttf", font_size)
            draw.text((x, y), user_text, fill=(255, 255, 255), font=img_font, anchor='mm')

    def add_img_watermark(self, watermark_img=None):
        if self.base_image:
            size = (self.w // 3, self.h // 3)
            x, y = int(self.w//10), int(self.h//8)

            if watermark_img:
                watermark = Image.open(watermark_img)
                watermark.thumbnail(size)
                self.new_image.paste(watermark, (x, y))
            else:
                # Use a shrunken version of the base image as the watermark
                cropped_img = self.base_image.copy()
                cropped_img.thumbnail(size)
                self.new_image.paste(cropped_img, (x, y))

    def save_watermarked_image(self, new_file_name):
        if self.base_image:
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            current_time = current_datetime.strftime("%H-%M-%S")
            time_stamp = f"{current_date}_{current_time}"
            output_filename = f"{time_stamp}-{new_file_name}.jpg"
            self.new_image.save(output_filename)
            print(f"Watermarked image saved as {output_filename}")

    def show_images(self, isBase):
        if self.base_image:
            if isBase:
                plt.subplot(1, 2, 1)
                plt.title("Original Image")
                plt.imshow(self.base_image)
                plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.title("Watermarked Image")
            plt.imshow(self.new_image)
            plt.axis('off')
            plt.show()

            

wtrmkr = Watermarker("dexter_falshing.jpg")
wtrmkr.add_img_watermark("henry_every_flag.webp")
wtrmkr.show_images(True)


from tkinter import *

#Creating a new window and configurations
window = Tk()
window.title("Widget Examples")
window.minsize(width=500, height=500)

#Labels
label = Label(text="This is old text")
label.config(text="This is new text")
label.pack()

#Buttons
def action():
    print("Do something")

#calls action() when pressed
button = Button(text="Click Me", command=action)
button.pack()

#Entries
entry = Entry(width=30)
#Add some text to begin with
entry.insert(END, string="Some text to begin with.")
#Gets text in entry
print(entry.get())
entry.pack()

#Text
text = Text(height=5, width=30)
#Puts cursor in textbox.
text.focus()
#Adds some text to begin with.
text.insert(END, "Example of multi-line text entry.")
#Get's current value in textbox at line 1, character 0
print(text.get("1.0", END))
text.pack()

#Spinbox
def spinbox_used():
    #gets the current value in spinbox.
    print(spinbox.get())
spinbox = Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.pack()

#Scale
#Called with current scale value.
def scale_used(value):
    print(value)
scale = Scale(from_=0, to=100, command=scale_used)
scale.pack()

#Checkbutton
def checkbutton_used():
    #Prints 1 if On button checked, otherwise 0.
    print(checked_state.get())
#variable to hold on to checked state, 0 is off, 1 is on.
checked_state = IntVar()
checkbutton = Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checked_state.get()
checkbutton.pack()

#Radiobutton
def radio_used():
    print(radio_state.get())
#Variable to hold on to which radio button value is checked.
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Option1", value=1, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Option2", value=2, variable=radio_state, command=radio_used)
radiobutton1.pack()
radiobutton2.pack()


#Listbox
def listbox_used(event):
    # Gets current selection from listbox
    print(listbox.get(listbox.curselection()))

listbox = Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()
window.mainloop()

