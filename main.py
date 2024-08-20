import math
import urllib.request
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import extcolors



class ImageColorAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Color Analyzer")


        self.label_url = tk.Label(self.root, text="Resim URL'si:", font=("Arial", 12))
        self.label_url.pack(pady=10)
        self.entry_url = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.entry_url.pack(pady=5)

        self.btn_file = tk.Button(self.root, text="Resim Dosyası Seç", font=("Arial", 12),
                                  command=self.open_file_dialog)
        self.btn_file.pack(pady=10)

        self.btn_analyze = tk.Button(self.root, text="Analiz Et", font=("Arial", 12), command=self.analyze_image)
        self.btn_analyze.pack(pady=10)

        self.canvas_palette = tk.Canvas(self.root, width=800, height=600)
        self.canvas_palette.pack()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.entry_url.delete(0, tk.END)
            self.entry_url.insert(0, file_path)

    def analyze_image(self):
        image_path = self.entry_url.get()

        try:
            img = self.fetch_image(image_path)
            colors = self.extract_colors(img)
            color_palette = self.render_color_palette(colors)
            self.display_color_palette(color_palette, colors)
        except Exception as e:
            messagebox.showerror("Hata", f"Resim analiz edilirken bir hata oluştu: {e}")

    def fetch_image(self, image_path):
        if image_path.startswith('http'):
            urllib.request.urlretrieve(image_path, "temp_image.png")
            img = Image.open("temp_image.png")
        else:
            img = Image.open(image_path)
        return img

    def extract_colors(self, img):
        tolerance = 32
        limit = 24
        colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
        return colors

    def render_color_palette(self, colors):
        size = 100
        columns = 6
        width = int(min(len(colors), columns) * size)
        height = int((math.floor(len(colors) / columns) + 1) * size)
        result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        canvas = ImageDraw.Draw(result)

        for idx, color in enumerate(colors):
            x = int((idx % columns) * size)
            y = int(math.floor(idx / columns) * size)
            canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])

        return result

    def display_color_palette(self, color_palette, colors):
        img_tk = ImageTk.PhotoImage(color_palette)
        self.canvas_palette.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas_palette.image = img_tk
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=10)

        for idx, (rgb, _) in enumerate(colors):
            color_hex = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
            color_label = tk.Label(color_frame, text=f"RGB: {rgb}", fg=color_hex, font=("Arial", 10))
            color_label.grid(row=idx // 3, column=idx % 3, padx=5, pady=5, sticky="w")


def main():
    root = tk.Tk()
    app = ImageColorAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
