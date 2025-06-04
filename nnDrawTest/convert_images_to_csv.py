import os
import csv
from PIL import Image
import re

DATA_DIR = "data"
OUTPUT_DIR = "dataset"
CSV_FILENAME = "symbol_data.csv"
IMAGE_SIZE = 28  # Size to scale up to

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_label(filename):
    match = re.match(r"([^_]+)_", filename)
    return match.group(1) if match else "unknown"

def process_image(filepath):
    img = Image.open(filepath)
    if img.mode in ("RGBA", "LA"):  # Has transparency
        bg = Image.new("RGB", img.size, (255, 255, 255))  # white background
        bg.paste(img, mask=img.split()[-1])  # Paste with alpha channel as mask
        img = bg
    img = img.convert("L")  # Convert to grayscale
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
    return list(img.getdata())

def main():
    all_images = []
    for folder in ["data", "augmented"]:
        folder_path = os.path.join(folder)
        if not os.path.isdir(folder_path):
            print(f"⚠️ Folder not found: {folder_path}")
            continue
        images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".png")]
        all_images.extend(images)

    all_images.sort()  # Optional: keep a consistent order

    header = ["Label"] + [f"p_{row+1}x{col+1}" for row in range(IMAGE_SIZE) for col in range(IMAGE_SIZE)]
    rows = []

    for image_path in all_images:
        filename = os.path.basename(image_path)
        label = extract_label(filename)
        pixels = process_image(image_path)
        row = [label] + pixels
        rows.append(row)

    output_path = os.path.join(OUTPUT_DIR, CSV_FILENAME)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"✅ Saved CSV to {output_path} with {len(rows)} rows.")

if __name__ == "__main__":
    main()