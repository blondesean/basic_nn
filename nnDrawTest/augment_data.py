import os
import random
from PIL import Image
import numpy as np
import os
print("Current script:", __file__)
print("Working directory:", os.getcwd())


def augment_image(image_path, output_dir, num_variants=10):
    image = Image.open(image_path).convert("L")
    w, h = image.size

    basename = os.path.splitext(os.path.basename(image_path))[0]

    for i in range(num_variants):
        # Random small scale and translation values
        scale_x = random.uniform(0.8, 1.2)
        scale_y = random.uniform(0.8, 1.2)
        shear_x = random.uniform(-0.25, 0.25)  # subtle shear
        shear_y = random.uniform(-0.25, 0.25)
        translate_x = random.uniform(-7, 7)
        translate_y = random.uniform(-7, 7)

        matrix = (
            scale_x, shear_x, translate_x,
            shear_y, scale_y, translate_y
        )

        # Apply transformation
        transformed = image.transform((w, h), Image.AFFINE, matrix, resample=Image.BILINEAR)

        # Save new image
        new_name = f"{basename}_aug{i}.png"
        transformed.save(os.path.join(output_dir, new_name))

# Example usage:
input_folder = "./data"
output_folder = "./augmented"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        augment_image(os.path.join(input_folder, filename), output_folder, num_variants=25)
