import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")
        
        # Variables
        self.data_var = tk.StringVar()
        self.fg_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.style_var = tk.StringVar(value="square")
        self.size_var = tk.IntVar(value=10)
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="QR Code Content", padx=10, pady=10)
        input_frame.pack(pady=10, fill="x", padx=10)
        
        tk.Label(input_frame, text="Enter text/URL:").pack(anchor="w")
        tk.Entry(input_frame, textvariable=self.data_var, width=50).pack(fill="x")
        
        # Settings Frame
        settings_frame = tk.LabelFrame(self.root, text="QR Code Settings", padx=10, pady=10)
        settings_frame.pack(pady=10, fill="x", padx=10)
        
        # Color Settings
        color_frame = tk.Frame(settings_frame)
        color_frame.pack(fill="x", pady=5)
        
        tk.Label(color_frame, text="Foreground:").grid(row=0, column=0)
        tk.Button(color_frame, text="Choose", command=self.choose_fg_color).grid(row=0, column=1)
        
        tk.Label(color_frame, text="Background:").grid(row=1, column=0)
        tk.Button(color_frame, text="Choose", command=self.choose_bg_color).grid(row=1, column=1)
        
        # Style Settings
        style_frame = tk.Frame(settings_frame)
        style_frame.pack(fill="x", pady=5)
        
        tk.Label(style_frame, text="Module Style:").grid(row=0, column=0)
        tk.OptionMenu(style_frame, self.style_var, "square", "rounded", "circle").grid(row=0, column=1)
        
        tk.Label(style_frame, text="Size:").grid(row=1, column=0)
        tk.Scale(style_frame, from_=1, to=20, orient="horizontal", variable=self.size_var).grid(row=1, column=1)
        
        # Generate Button
        tk.Button(self.root, text="Generate QR Code", command=self.generate_qr, 
                 bg="#4CAF50", fg="white").pack(pady=10)
        
        # QR Code Display
        self.qr_label = tk.Label(self.root)
        self.qr_label.pack(pady=10)
        
        # Save Button
        tk.Button(self.root, text="Save QR Code", command=self.save_qr, 
                 bg="#2196F3", fg="white").pack(pady=5)
    
    def choose_fg_color(self):
        color = tk.colorchooser.askcolor(title="Choose foreground color")
        if color[1]:
            self.fg_color = color[1]
    
    def choose_bg_color(self):
        color = tk.colorchooser.askcolor(title="Choose background color")
        if color[1]:
            self.bg_color = color[1]
    
    def generate_qr(self):
        data = self.data_var.get()
        if not data:
            messagebox.showerror("Error", "Please enter some text or URL")
            return
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.size_var.get(),
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Apply different styles based on selection
            if self.style_var.get() == "rounded":
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                    color_mask=RadialGradiantColorMask(
                        back_color=self.bg_color,
                        center_color=self.fg_color,
                        edge_color=self.fg_color
                    )
                )
            else:
                img = qr.make_image(
                    fill_color=self.fg_color,
                    back_color=self.bg_color
                )
            
            # Resize for display
            img = img.resize((300, 300), Image.LANCZOS)
            self.qr_img = img
            self.tk_img = ImageTk.PhotoImage(img)
            self.qr_label.config(image=self.tk_img)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def save_qr(self):
        if not hasattr(self, 'qr_img'):
            messagebox.showerror("Error", "Please generate a QR code first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save QR Code"
        )
        
        if file_path:
            try:
                self.qr_img.save(file_path)
                messagebox.showinfo("Success", f"QR code saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
