import cv2
import numpy as np
from sklearn.cluster import KMeans
import csv

colourNames = {
    "#ff0000": "Red",
    "#ffff00": "Yellow",
    "#0000ff": "Blue",
    "#00ff00": "Green",
    "#ffa500": "Orange",
    "#800080": "Purple",
    "#ffc0cb": "Pink",
    "#a52a2a": "Brown",
    "#000000": "Black",
    "#ffffff": "White",
    "#808080": "Grey"
}

COLOUR_NAME_TO_HEX = {
    "red":    "#ff0000",
    "yellow": "#ffff00",
    "blue":   "#0000ff",
    "green":  "#00ff00",
    "orange": "#ffa500",
    "purple": "#800080",
    "pink":   "#ffc0cb",
    "brown":  "#a52a2a",
    "black":  "#000000",
    "white":  "#ffffff",
    "grey":   "#808080",
    "navy":   "#0000ff",
    "olive":  "#808080",
}



def _rgb_to_hsv_pixel(rgb: tuple) -> tuple:
    arr = np.uint8([[rgb]])
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


def classify_by_hue(rgb: tuple) -> str:
    h, s, v = _rgb_to_hsv_pixel(rgb)
    if s < 50:
        if v < 70:  return "black"
        if v > 200: return "white"
        return "grey"
    if h < 10 or h >= 165:
        return "brown" if v < 130 else "red"
    if h < 22:
        if v > 180 and s > 150:
            return "orange"
        return "brown"
    if h < 33:
        return "brown" if v < 130 else "orange"
    if h < 45:
        if s < 120 and v < 160:
            return "olive"
        return "yellow"
    if h < 65:
        return "yellow" if h < 50 else "green"
    if h < 95:
        return "olive" if s < 80 or v < 100 else "green"
    if h < 105:
        return "green"
    if h < 130:
        return "navy" if v < 110 else "blue"
    if h < 150:
        return "purple" if s > 100 else "blue"
    if h < 165:
        if v < 120:
            return "purple"
        return "pink" if s < 180 else "purple"
    return "grey"


def _extract_patches(img_rgb: np.ndarray, patch_size: int) -> np.ndarray:
    h, w, _ = img_rgb.shape
    half = patch_size // 2
    centres = [
        (h // 2,     w // 2),
        (h // 3,     w // 2),
        (2 * h // 3, w // 2),
        (h // 2,     w // 3),
        (h // 2,     2 * w // 3),
    ]
    patches = []
    for cy, cx in centres:
        y0, y1 = max(0, cy - half), min(h, cy + half)
        x0, x1 = max(0, cx - half), min(w, cx + half)
        patches.append(img_rgb[y0:y1, x0:x1].reshape(-1, 3))
    return np.vstack(patches)


def _get_saturation_mask(pixels_rgb: np.ndarray, threshold: int = 50) -> np.ndarray:
    img = pixels_rgb.reshape(1, -1, 3).astype(np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).reshape(-1, 3)
    return hsv[:, 1] > threshold

def detect_dominant_colour(
    img_path: str,
    patch_size: int = 200,
    k: int = 4,
    saturation_threshold: int = 50,
) -> str:
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not open image: {img_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = _extract_patches(img_rgb, patch_size)

    not_white = ~np.all(pixels > 230, axis=1)
    pixels = pixels[not_white]

    if len(pixels) == 0:
        return "unknown"

    chroma_mask = _get_saturation_mask(pixels, saturation_threshold)
    chroma_ratio = chroma_mask.sum() / len(pixels)
    print(f"Chromatic pixel ratio: {chroma_ratio:.2%}")

    working = pixels[chroma_mask] if chroma_ratio > 0.15 else pixels

    n_clusters = min(k, len(working))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(working)

    counts = np.bincount(kmeans.labels_)
    dominant_rgb = tuple(int(c) for c in kmeans.cluster_centers_[np.argmax(counts)])

    print(f"Dominant RGB: {dominant_rgb}  HSV: {_rgb_to_hsv_pixel(dominant_rgb)}")
    return classify_by_hue(dominant_rgb)

def isValidHex(colour):
    try:
        return colour.startswith("#") and len(colour) == 7 and bool(int(colour[1:], 16) >= 0)
    except ValueError:
        return False

def hexToRgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgbDistance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(hexToRgb(c1), hexToRgb(c2)))

def closestColourName(hex):
    return min(colourNames, key=lambda ref: rgbDistance(hex, ref))

def loadDataset(csvFile):
    with open(csvFile, newline='', encoding='utf-8') as f:
        return [{
            "colour1Hex":   r["Color_1_Hex"].strip().lower(),
            "colour1Name":  r["Color_1_Name"].strip(),
            "colour2Hex":   r["Color_2_Hex"].strip().lower(),
            "colour2Name":  r["Color_2_Name"].strip(),
            "style":       r["Style_Category"].strip(),
            "description": r["Description"].strip(),
        } for r in csv.DictReader(f)]

def pairScore(inputColour, pair):
    d1, d2 = rgbDistance(inputColour, pair["colour1Hex"]), rgbDistance(inputColour, pair["colour2Hex"])
    return (min(d1, d2), max(d1, d2))

def suggestOutfits(inputColour, csvFile, topN=3):
    return sorted(loadDataset(csvFile), key=lambda p: pairScore(inputColour, p))[:topN]


if __name__ == "__main__":
    img_path = input("Enter image path: ").strip()

    detected_name = detect_dominant_colour(img_path)

    detected_hex = COLOUR_NAME_TO_HEX.get(detected_name, "#808080")

    print(f"\nDetected clothing colour: {detected_name.capitalize()} ({detected_hex})")
    print("\nTop 3 suggested colour pairings:\n")

    for i, pair in enumerate(suggestOutfits(detected_hex, "backend\clothing_colour_combinations.csv"), start=1):
        print(f"  Outfit {i}: {pair['colour1Name']} ({pair['colour1Hex']}) + {pair['colour2Name']} ({pair['colour2Hex']})")
        print(f"  Style: {pair['style']} — {pair['description']}\n")