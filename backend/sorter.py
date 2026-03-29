import os
import shutil
import pandas as pd

# ---------------------------------------------------------------------------
# Config — update these two paths
# ---------------------------------------------------------------------------
CSV_PATH    = r"backend\images.csv"       # the CSV file
IMAGES_DIR  = r"backend\images_compressed"           # the flat folder of images
OUTPUT_DIR  = r"backend\sorted"    # where sorted folders will be created

# ---------------------------------------------------------------------------
# Map Kaggle labels -> your 8 category folder names
# Labels not in this map are skipped (e.g. "Not sure", "Others", "Skip")
# ---------------------------------------------------------------------------
LABEL_MAP = {
    "T-Shirt":     "t-shirt",
    "Shirt":       "shirt",
    "Long Sleeve": "shirt",
    "Polo":        "shirt",
    "Outwear":     "outwear",
    "Blazer":      "outwear",
    "Hoodie":      "outwear",
    "Dress":       "dress",
    "Blouse":      "dress",
    "Body":        "dress",
    "Pants":       "trousers",
    "Shorts":      "shorts",
    "Skirt":       "skirt",
    "Shoes":       "shoes",
}

# ---------------------------------------------------------------------------
# Read CSV and organise images
# ---------------------------------------------------------------------------
df = pd.read_csv(CSV_PATH)

# Create output folders
for folder in set(LABEL_MAP.values()):
    os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)

skipped = 0
copied  = 0

for _, row in df.iterrows():
    label    = str(row["label"]).strip()
    image_id = str(row["image"]).strip()

    if label not in LABEL_MAP:
        skipped += 1
        continue

    # Find the image file (try .jpg and .png)
    src = None
    for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
        candidate = os.path.join(IMAGES_DIR, image_id + ext)
        if os.path.exists(candidate):
            src = candidate
            break

    if src is None:
        print(f"Image not found: {image_id}")
        skipped += 1
        continue

    dest_folder = os.path.join(OUTPUT_DIR, LABEL_MAP[label])
    dest        = os.path.join(dest_folder, os.path.basename(src))
    shutil.copy2(src, dest)
    copied += 1

print(f"\nDone! {copied} images copied, {skipped} skipped.")
print(f"Output folder: {OUTPUT_DIR}")

# Print count per category
print("\nImages per category:")
for folder in sorted(set(LABEL_MAP.values())):
    count = len(os.listdir(os.path.join(OUTPUT_DIR, folder)))
    print(f"  {folder}: {count}")