import os
import csv
from PIL import Image
import re

DATA_DIR = "data"
OUTPUT_DIR = "dataset"
CSV_FILENAME = "symbol_data.csv"
IMAGE_SIZE = 256  # Size to scale up to

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_label(filename):
    match = re.match(r"([a-zA-Z]+)_\d+\.png", filename)
    return match.group(1) if match else "unknown"

def process_image(filepath):
    img = Image.open(filepath).convert("L")
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
    return list(img.getdata())

def main():
    images = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".png")]
    images.sort()  # optional: keep consistent order

    header = ["Label"] + [f"pixel_{row+1}x{col+1}" for row in range(IMAGE_SIZE) for col in range(IMAGE_SIZE)]
    rows = []

    for image_file in images:
        label = extract_label(image_file)
        filepath = os.path.join(DATA_DIR, image_file)
        pixels = process_image(filepath)
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
