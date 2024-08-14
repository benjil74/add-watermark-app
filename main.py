import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


def add_watermark(image, watermark_text):
    image = image.convert("RGBA")
    txt = Image.new('RGBA', image.size, (0, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", 40)
    d = ImageDraw.Draw(txt)
    width, height = image.size
    bbox = d.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = width - text_width - 30
    y = height - text_height - 30
    d.text((x, y), watermark_text, fill=(55, 155, 155, 200), font=font)
    watermarked = Image.alpha_composite(image, txt)

    return watermarked


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        watermarked_img = add_watermark(img, "Sample Watermark")
        tk_img = ImageTk.PhotoImage(watermarked_img)
        panel = tk.Label(root, image=tk_img)
        panel.image = tk_img
        panel.pack()


def add_logo_watermark(image, logo_path, position=None):
    image = image.convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo_width, logo_height = logo.size
    base_width = image.width // 4
    wpercent = (base_width / float(logo_width))
    hsize = int((float(logo_height) * float(wpercent)))
    logo = logo.resize((base_width, hsize), Image.Resampling.LANCZOS)

    if position is None:
        position = (image.width - logo.width - 10, image.height - logo.height - 10)

    watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
    watermark.paste(logo, position, mask=logo)
    watermarked = Image.alpha_composite(image, watermark)

    return watermarked


def open_image_logo():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        logo_path = filedialog.askopenfilename(title="Select a logo file")

        if logo_path:
            watermarked_img = add_logo_watermark(img, logo_path)
            tk_img = ImageTk.PhotoImage(watermarked_img)

            panel = tk.Label(root, image=tk_img)
            panel.image = tk_img
            panel.pack()


def save_image():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                 ("All files", "*.*")])
    print(f"Image saved to {save_path}")


root = tk.Tk()
root.title("Watermark Image")
root.config(padx=30, pady=30, background="blue")

btn = tk.Button(root, highlightthickness=0, width=30, text="Open Image to add text", command=open_image)
btn.config()
btn.pack()

btn = tk.Button(root, text="Open Image to add logo", width=30, command=open_image_logo)
btn.pack()

btn_save = tk.Button(root, text="Save Image", width=30, command=save_image)
btn_save.pack()

root.mainloop()
