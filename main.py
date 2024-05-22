import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from watermark import Watermarker  # Import Watermarker class from watermark.py

# Function to select the base image
def select_base_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        watermark.select_img(file_path)  # Call select_img method from Watermarker class
        base_image_label.config(text=f"Selected: {os.path.basename(file_path)}")  # Update label text
        show_images_btn.config(state=tk.NORMAL)  # Enable show images button
        update_watermark_size(size_slider.get())  # Update watermark size

# Function to apply image watermark
def apply_image_watermark():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path and watermark.base_image:
        watermark.add_img_watermark(file_path)  # Call add_img_watermark method from Watermarker class
        watermark.show_images()  # Display images with watermark

# Function to save the watermarked image
def save_image():
    new_file_name = file_name_entry.get()
    if new_file_name:
        watermark.save_watermarked_image(new_file_name)  # Call save_watermarked_image method from Watermarker class
    else:
        messagebox.showerror("Error", "Please enter a file name to save the image")

# Function to update watermark size
def update_watermark_size(value):
    watermark.set_watermark_size(int(value))  # Call set_watermark_size method from Watermarker class
    if watermark.base_image:
        watermark.show_images()  # Display images with updated watermark size

# Function to update watermark opacity
def update_opacity(value):
    watermark.wtm_options['opacity'] = int(value) / 100  # Update opacity in watermark options
    if watermark.base_image and watermark.watermark_img:
        watermark._apply_watermark()  # Reapply watermark with updated opacity
        watermark.show_images()  # Display images with updated opacity

# Function to update watermark position
def update_watermark_position(event):
    position = position_combobox.get()
    watermark.set_watermark_position(position)  # Call set_watermark_position method from Watermarker class

# Create main window
window = tk.Tk()
window.title("Watermarker")
window.geometry("400x500")

watermark = Watermarker()  # Initialize Watermarker object

# GUI elements
select_image_btn = tk.Button(window, text="Select Base Image", command=select_base_image)
select_image_btn.pack(pady=10)

base_image_label = tk.Label(window, text="No image selected")
base_image_label.pack(pady=5)

apply_image_btn = tk.Button(window, text="Apply Image Watermark", command=apply_image_watermark)
apply_image_btn.pack(pady=5)

size_label = tk.Label(window, text="Watermark Size:")
size_label.pack(pady=5)

size_slider = tk.Scale(window, from_=10, to=100, orient='horizontal', command=update_watermark_size)
size_slider.set(30)  # Default size
size_slider.pack(pady=5)

opacity_label = tk.Label(window, text="Watermark Opacity:")
opacity_label.pack(pady=5)

opacity_slider = tk.Scale(window, from_=0, to=100, orient='horizontal', command=update_opacity)
opacity_slider.set(100)  # Default opacity
opacity_slider.pack(pady=5)

position_label = tk.Label(window, text="Watermark Position:")
position_label.pack(pady=5)

positions = ['Top Left', 'Top Right', 'Center', 'Bottom Left', 'Bottom Right']
position_combobox = ttk.Combobox(window, values=positions)
position_combobox.set('Bottom Right')
position_combobox.pack(pady=5)
position_combobox.bind("<<ComboboxSelected>>", update_watermark_position)

file_name_entry = tk.Entry(window, width=30)
file_name_entry.pack(pady=10)
file_name_entry.insert(0, "Enter file name to save")

save_image_btn = tk.Button(window, text="Save Image", command=save_image)
save_image_btn.pack(pady=5)

show_images_btn = tk.Button(window, text="Show Images", command=watermark.show_images, state=tk.DISABLED)
show_images_btn.pack(pady=5)

# Run the Tkinter event loop
window.mainloop()
