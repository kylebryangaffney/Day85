import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class Watermarker:
    def __init__(self):
        self.base_image = None
        self.new_image = None
        self.watermark_size = 0.3
        
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
            size = (int(self.w * self.watermark_size), int(self.h * self.watermark_size))
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
    
    def update_watermark_size(self, scale):
        self.watermark_size = scale / 100



    def show_images(self):
        if self.base_image:
            plt.subplot(1, 2, 1)
            plt.title("Original Image")
            plt.imshow(self.base_image)
            plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.title("Watermarked Image")
            plt.imshow(self.new_image)
            plt.axis('off')
            plt.show()

            


def select_base_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        watermark.select_img(file_path)
        base_image_label.config(text=f"Selected: {os.path.basename(file_path)}")
        show_images_btn.config(state=tk.NORMAL)

def apply_text_watermark():
    user_text = text_entry.get()
    if user_text and watermark.new_image:
        watermark.add_text_watermark(user_text)
        watermark.show_images()

def apply_image_watermark():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path and watermark.new_image:
        watermark.add_img_watermark(file_path)
        watermark.show_images()

def save_image():
    new_file_name = file_name_entry.get()
    if new_file_name:
        watermark.save_watermarked_image(new_file_name)

def update_watermark_size(value):
    watermark.set_watermark_size(int(value))

# Create main window
window = tk.Tk()
window.title("Watermarker")
window.geometry("400x400")

watermark = Watermarker()

# GUI elements
select_image_btn = tk.Button(window, text="Select Base Image", command=select_base_image)
select_image_btn.pack(pady=10)

base_image_label = tk.Label(window, text="No image selected")
base_image_label.pack(pady=5)

text_entry = tk.Entry(window, width=30)
text_entry.pack(pady=10)
text_entry.insert(0, "Enter text watermark")

apply_text_btn = tk.Button(window, text="Apply Text Watermark", command=apply_text_watermark)
apply_text_btn.pack(pady=5)

apply_image_btn = tk.Button(window, text="Apply Image Watermark", command=apply_image_watermark)
apply_image_btn.pack(pady=5)

size_label = tk.Label(window, text="Watermark Size:")
size_label.pack(pady=5)

size_slider = tk.Scale(window, from_=10, to=100, orient='horizontal', command=update_watermark_size)
size_slider.set(30)  # Default size
size_slider.pack(pady=5)

file_name_entry = tk.Entry(window, width=30)
file_name_entry.pack(pady=10)
file_name_entry.insert(0, "Enter file name to save")

save_image_btn = tk.Button(window, text="Save Image", command=save_image)
save_image_btn.pack(pady=5)

show_images_btn = tk.Button(window, text="Show Images", command=watermark.show_images, state=tk.DISABLED)
show_images_btn.pack(pady=5)


# Run the Tkinter event loop
window.mainloop()