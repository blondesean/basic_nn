import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageOps
import os

CANVAS_SIZE = 280
IMAGE_SIZE = 28
DATA_DIR = "data"

class SymbolApp:
    def __init__(self, master, labels, samples_per_label):
        self.master = master
        self.labels = labels
        self.samples_per_label = samples_per_label

        self.current_label_index = 0
        self.current_sample_num = 1

        self.label = self.labels[self.current_label_index]

        self.canvas = tk.Canvas(master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='white')
        self.canvas.pack()

        self.info_label = tk.Label(master, text=self.status_text())
        self.info_label.pack()

        self.button_clear = tk.Button(master, text="Clear", command=self.clear_canvas)
        self.button_clear.pack()

        self.canvas.bind("<Button-1>", self.on_pen_down)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_pen_lift)

        self.image = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), "white")
        self.draw_obj = ImageDraw.Draw(self.image)

        self.prev_x, self.prev_y = None, None

        os.makedirs(DATA_DIR, exist_ok=True)

    def status_text(self):
        return f"Draw symbol for label '{self.label}' - Sample {self.current_sample_num} of {self.samples_per_label}. Draw and release mouse to save."
    
    def on_pen_down(self, event):
        self.prev_x, self.prev_y = event.x, event.y


    def draw(self, event):
        x, y = event.x, event.y
        r = 8

        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.create_line(self.prev_x, self.prev_y, x, y, width=r*2, fill='black', capstyle=tk.ROUND, smooth=True)
            self.draw_obj.line([self.prev_x, self.prev_y, x, y], fill='black', width=r*2)
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='black')
            self.draw_obj.ellipse([x - r, y - r, x + r, y + r], fill='black')

        self.prev_x, self.prev_y = x, y

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), "white")
        self.draw_obj = ImageDraw.Draw(self.image)
        self.prev_x, self.prev_y = None, None

    def on_pen_lift(self, event):
        # Save image automatically on mouse release
        filename = f"{self.label}_{self.current_sample_num:03d}.png"
        filepath = os.path.join(DATA_DIR, filename)

        small_img = self.image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
        small_img = ImageOps.invert(small_img)
        small_img.save(filepath)
        print(f"Saved {filename} in {DATA_DIR}")

        # Advance to next sample/label
        if self.current_sample_num < self.samples_per_label:
            self.current_sample_num += 1
        else:
            self.current_sample_num = 1
            self.current_label_index += 1
            if self.current_label_index >= len(self.labels):
                messagebox.showinfo("Done", "All samples saved. You can close the app.")
                self.master.quit()
                return
            self.label = self.labels[self.current_label_index]

        self.info_label.config(text=self.status_text())
        self.clear_canvas()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Symbol Collector")

    labels = ['Fire Level 1', 'Fire Level 2', 'Fire Level 3'
              ,'Air Level 1', 'Air Level 2', 'Air Level 3'
              ,'Water Level 1', 'Water Level 2', 'Water Level 3'
              ,'Earth Level 1', 'Earth Level 2', 'Earth Level 3'
              ,'Dark Level 1', 'Dark Level 2', 'Dark Level 3'
              ,'Light Level 1', 'Light Level 2', 'Fire Level 3']    # example labels
    samples_per_label = 25      # example samples per label

    app = SymbolApp(root, labels, samples_per_label)
    root.mainloop()
