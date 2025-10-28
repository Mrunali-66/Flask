# Image Watermark App using Tkinter and Pillow
# Author: Jiya

from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark App")
        self.root.geometry("700x500")
        self.root.config(bg="#F5F5F5")

        self.image_path = None
        self.watermark_text = StringVar()

        # Title Label
        Label(root, text="Watermark Generator", font=("Helvetica", 20, "bold"), bg="#F5F5F5", fg="#333").pack(pady=20)

        # Upload Button
        Button(root, text="Upload Image", command=self.upload_image, font=("Arial", 12), bg="#0078D7", fg="white", padx=10, pady=5).pack(pady=10)

        # Text Entry
        Label(root, text="Enter Watermark Text:", font=("Arial", 12), bg="#F5F5F5").pack(pady=5)
        Entry(root, textvariable=self.watermark_text, font=("Arial", 12), width=40).pack(pady=5)

        # Apply Button
        Button(root, text="Add Watermark", command=self.add_watermark, font=("Arial", 12), bg="#28A745", fg="white", padx=10, pady=5).pack(pady=10)

        # Canvas to display image
        self.canvas = Canvas(root, width=500, height=300, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

    def upload_image(self):
        """Function to upload an image file"""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((500, 300))
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(250, 150, image=self.tk_image)
            messagebox.showinfo("Success", "Image uploaded successfully!")

    def add_watermark(self):
        """Function to add watermark text to the image"""
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        text = self.watermark_text.get()
        if not text:
            messagebox.showerror("Error", "Please enter a watermark text.")
            return

        img = Image.open(self.image_path).convert("RGBA")
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        font = ImageFont.load_default()

        # Calculate text size using textbbox()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = (img.width - text_width - 20, img.height - text_height - 20)

        # Add semi-transparent watermark
        draw.text(position, text, fill=(255, 255, 255, 128), font=font)

        # Merge the text layer with the image
        watermarked = Image.alpha_composite(img, txt_layer)

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")])
        if save_path:
            watermarked.convert("RGB").save(save_path)
            messagebox.showinfo("Saved", f"Watermarked image saved as {save_path}")

            # Update canvas with the new image preview
            preview_img = watermarked.copy()
            preview_img.thumbnail((500, 300))
            self.tk_image = ImageTk.PhotoImage(preview_img)
            self.canvas.create_image(250, 150, image=self.tk_image)

# Run the app
if __name__ == "__main__":
    root = Tk()
    WatermarkApp(root)
    root.mainloop()
