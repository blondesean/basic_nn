import tkinter as tk
from tkinter import Label
from PIL import Image, ImageDraw, ImageOps
import torch
import torch.nn.functional as F
from torchvision import transforms
from symbol_classifier import SymbolClassifier

# Load model
model = SymbolClassifier()
model.load_state_dict(torch.load("symbol_model.pt"))
model.eval()

#Symbol labels
labels = [
    'Fire Level 1', 'Fire Level 2', 'Fire Level 3',
    'Air Level 1', 'Air Level 2', 'Air Level 3',
    'Water Level 1', 'Water Level 2', 'Water Level 3',
    'Earth Level 1', 'Earth Level 2', 'Earth Level 3',
    'Dark Level 1', 'Dark Level 2', 'Dark Level 3',
    'Light Level 1', 'Light Level 2', 'Light Level 3']

# Image and drawing setup
canvas_size = 280  # larger canvas for easier drawing
image = Image.new("L", (canvas_size, canvas_size), color=255)
draw = ImageDraw.Draw(image)

# Tkinter setup
root = tk.Tk()
root.title("Draw a Symbol")

canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()
#UI Labels
result_label = Label(root, text="", justify="left", anchor="w", font=("Courier", 10))
result_label.pack(pady=10)

# Mouse drawing functions
def start_draw(event):
    canvas.old_coords = event.x, event.y

def draw_motion(event):
    x, y = event.x, event.y
    x1, y1 = canvas.old_coords
    canvas.create_line(x, y, x1, y1, width=8, fill="black", capstyle=tk.ROUND, smooth=True)
    draw.line([x, y, x1, y1], fill=0, width=8)
    canvas.old_coords = x, y

def reset_coords(event):
    canvas.old_coords = None

# Preprocess and predict
def predict():
    img = image.copy()
    img = ImageOps.invert(img)
    img = img.resize((28, 28), Image.LANCZOS)
    tensor = transforms.ToTensor()(img).view(1, -1)

    print("Input tensor shape:", tensor.shape)
    print("Input tensor min/max:", tensor.min().item(), tensor.max().item())
    print("Input tensor sample values:", tensor[0, :10])

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)
        top_probs, top_indices = probs[0].topk(18)

        print("\n🔮 Prediction Confidence:")
        for i in range(18):
            label = labels[top_indices[i].item()]
            prob = top_probs[i].item()
            print(f"{label}: {prob:.4f}")

    probs = F.softmax(logits, dim=1).squeeze()

    top_class = torch.argmax(probs).item()
    top_probs, top_indices = torch.sort(probs, descending=True)

    result_text.delete("1.0", tk.END)
    for cls, prob in zip(top_indices, top_probs):
        result_text.insert(tk.END, f"{labels[cls.item()]}: {prob:.4f}\n")


# Clear drawing
def clear():
    canvas.delete("all")
    draw.rectangle([0, 0, canvas_size, canvas_size], fill=255)
    result_text.delete("1.0", tk.END)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

predict_btn = tk.Button(btn_frame, text="Predict", command=predict)
predict_btn.pack(side=tk.LEFT)

clear_btn = tk.Button(btn_frame, text="Clear", command=clear)
clear_btn.pack(side=tk.LEFT)

result_text = tk.Text(root, height=20, width=30)
result_text.pack()

# Bindings
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<B1-Motion>", draw_motion)
canvas.bind("<ButtonRelease-1>", reset_coords)

root.mainloop()
