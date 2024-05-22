import os
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageEnhance
import matplotlib.pyplot as plt
from datetime import datetime

# Constant for padding factor
WTM_PADDING_FACTOR = 1/30

class Watermarker:
    def __init__(self):
        # Initialize variables to hold image data and watermark options
        self.base_image = None
        self.new_image = None
        self.watermark_scale = 0.3  # Default scale for watermark size
        self.watermark_img = None
        self.width = 0
        self.height = 0
        # Default watermark options
        self.wtm_options = {
            'resize_factor': self.watermark_scale,
            'position': 'Bottom Right',
            'opacity': 1.0
        }

    # Method to select base image
    def select_img(self, base_image_path):
        try:
            self.base_image = Image.open(base_image_path)  # Open the image file
            self.new_image = self.base_image.copy()  # Create a copy for modifications
            self.width, self.height = self.base_image.size  # Get image dimensions
        except Exception as e:
            # Show error message if image cannot be opened
            messagebox.showerror("Error", f"Error opening image: {e}")
            self.base_image = None

    # Method to add image watermark
    def add_img_watermark(self, watermark_img_path=None):
        if self.base_image:
            if watermark_img_path:
                try:
                    self.watermark_img = Image.open(watermark_img_path).convert("RGBA")  # Open and convert to RGBA
                except Exception as e:
                    # Show error message if watermark image cannot be added
                    messagebox.showerror("Error", f"Error adding watermark: {e}")
            
            if self.watermark_img:
                self._apply_watermark()  # Apply the watermark to the image

    # Method to apply the watermark to the image
    def _apply_watermark(self):
        # Resize watermark according to options
        new_wtm = self.watermark_img.copy()
        new_wtm_width = int(self.wtm_options['resize_factor'] * self.width)
        coef = new_wtm_width / new_wtm.width
        new_wtm_height = int(new_wtm.height * coef)
        new_wtm = new_wtm.resize((new_wtm_width, new_wtm_height), Image.LANCZOS)

        # Determine position of the watermark
        wtm_position = self._get_watermark_position(new_wtm)

        # Adjust opacity of the watermark
        self._adjust_opacity(new_wtm)

        # Paste watermark onto the image
        new_image_rgba = self.base_image.convert("RGBA")
        new_image_rgba.paste(new_wtm, wtm_position, new_wtm)
        self.new_image = new_image_rgba.convert("RGB")

    # Method to determine the position of the watermark
    def _get_watermark_position(self, resized_wtm):
        position = self.wtm_options['position']
        padding = int(self.width * WTM_PADDING_FACTOR)
        if position == "Top Left":
            x_coord = padding
            y_coord = padding
        elif position == "Center":
            x_coord = int(self.width / 2 - resized_wtm.width / 2)
            y_coord = int(self.height / 2 - resized_wtm.height / 2)
        elif position == 'Bottom Right':
            x_coord = int(self.width - padding - resized_wtm.width)
            y_coord = int(self.height - padding - resized_wtm.height)
        elif position == 'Top Right':
            x_coord = int(self.width - padding - resized_wtm.width)
            y_coord = padding
        else:  # Bottom Left
            x_coord = padding
            y_coord = int(self.height - padding - resized_wtm.height)
        return x_coord, y_coord

    # Method to adjust opacity of the watermark
    def _adjust_opacity(self, new_wtm):
        opacity_level = int(self.wtm_options['opacity'] * 255)
        alpha = new_wtm.getchannel('A')
        new_alpha = alpha.point(lambda i: opacity_level if i > 0 else 0)
        new_wtm.putalpha(new_alpha)

    # Method to set the size of the watermark
    def set_watermark_size(self, scale):
        self.watermark_scale = scale / 100  # Scale the watermark
        self.wtm_options['resize_factor'] = self.watermark_scale  # Update options
        if self.watermark_img:
            self.new_image = self.base_image.copy()
            self._apply_watermark()  # Apply the watermark
            self.show_images()  # Show the images with the watermark

    # Method to set the position of the watermark
    def set_watermark_position(self, position):
        self.wtm_options['position'] = position  # Update position in options
        if self.watermark_img:
            self.new_image = self.base_image.copy()
            self._apply_watermark()  # Apply the watermark
            self.show_images()  # Show the images with the watermark

    # Method to display original and watermarked images
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

    # Method to save the watermarked image
    def save_watermarked_image(self, new_file_name):
        if self.base_image:
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            current_time = current_datetime.strftime("%H-%M-%S")
            time_stamp = f"{current_date}_{current_time}"
            output_filename = f"{time_stamp}-{new_file_name}.jpg"  # Construct filename
            try:
                self.new_image.save(output_filename)  # Save the watermarked image
                messagebox.showinfo("Success", f"Watermarked image saved as {output_filename}")
            except Exception as e:
                # Show error message if image cannot be saved
                messagebox.showerror("Error", f"Error saving image: {e}")
