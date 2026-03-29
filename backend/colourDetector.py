import cv2
import numpy as np
from sklearn.cluster import KMeans

def _rgb_to_hsv_pixel(rgb: tuple) -> tuple:
    arr = np.uint8([[rgb]])
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)[0][0]
    return int(hsv[0]), int(hsv[1]), int(hsv[2])


def classify_by_hue(rgb: tuple) -> str:
    """
    Classify a colour by HSV hue ranges rather than distance to references.
    Hue is brightness-independent, so navy and dark brown stay distinguishable.
    """
    h, s, v = _rgb_to_hsv_pixel(rgb)
    if s < 50:
        if v < 70:  return "black"
        if v > 200: return "white"
        return "grey"


    if h < 10 or h >= 165:
        # Red hues — dark + saturated = brown, bright = red
        return "brown" if v < 130 else "red"

    if h < 22:
        # Orange-brown — almost always brown for clothing
        if v > 180 and s > 150:
            return "orange"
        return "brown"

    if h < 33:
        # Orange zone
        if v < 130:
            return "brown"
        return "orange"

    if h < 45:
        # Yellow-orange
        if s < 120 and v < 160:
            return "olive"
        return "yellow"

    if h < 65:
        # Yellow-green
        return "yellow" if h < 50 else "green"

    if h < 95:
        # Green
        if s < 80 or v < 100:
            return "olive"
        return "green"

    if h < 105:
        # Cyan — rare in clothing, often teal/green
        return "green"

    if h < 130:
        # Blue range
        # Dark blue (low V) = navy, brighter = blue
        if v < 110:
            return "navy"
        return "blue"

    if h < 150:
        # Blue-purple
        return "purple" if s > 100 else "blue"

    if h < 165:
        # Purple-pink
        if v < 120:
            return "purple"
        return "pink" if s < 180 else "purple"

    return "grey"  # fallback


# ---------------------------------------------------------------------------
# Pixel extraction — multiple patches to handle off-centre garments
# ---------------------------------------------------------------------------

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
    """Return boolean mask of pixels whose HSV saturation exceeds threshold."""
    img = pixels_rgb.reshape(1, -1, 3).astype(np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).reshape(-1, 3)
    return hsv[:, 1] > threshold


# ---------------------------------------------------------------------------
# Main detection
# ---------------------------------------------------------------------------

# returns the main color found in an image (possibly return the images that are closest to it)
def detect_dominant_colour(
    img_path: str,
    patch_size: int = 200,
    k: int = 4,
    saturation_threshold: int = 50,
) -> str:
    """
    Detect the dominant clothing colour in an image.

    Strategy
    --------
    1. Sample pixels from multiple image patches.
    2. Remove near-white pixels (background / blown highlights).
       Do NOT remove dark pixels — dark navy and dark brown are still valid.
    3. Split pixels into chromatic (S > threshold) and achromatic (S <= threshold).
    4. If enough chromatic pixels exist, cluster ONLY those with KMeans.
       This stops dark-but-saturated blues/browns from averaging into grey.
    5. Classify the dominant cluster centre by hue ranges, not colour distance.
    """
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not open image: {img_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Gather pixels from multiple patches
    pixels = _extract_patches(img_rgb, patch_size)

    # Remove near-white (background/flash) — but keep dark pixels
    not_white = ~np.all(pixels > 230, axis=1)
    pixels = pixels[not_white]

    if len(pixels) == 0:
        return "unknown"

    # --- Chromatic / achromatic split ---
    chroma_mask = _get_saturation_mask(pixels, saturation_threshold)
    chroma_ratio = chroma_mask.sum() / len(pixels)
    print(f"Chromatic pixel ratio: {chroma_ratio:.2%}")

    if chroma_ratio > 0.15:
        working = pixels[chroma_mask]
    else:
        working = pixels

    n_clusters = min(k, len(working))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(working)

    counts = np.bincount(kmeans.labels_)
    dominant_rgb = tuple(int(c) for c in kmeans.cluster_centers_[np.argmax(counts)])

    print(f"Dominant RGB: {dominant_rgb}  HSV: {_rgb_to_hsv_pixel(dominant_rgb)}")
    return classify_by_hue(dominant_rgb)


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    colour = detect_dominant_colour(r"backend\brown_jumper.jpeg")
    print("Detected colour:", colour)
    colour = detect_dominant_colour(r"backend\orange_shirt.jpg")
    print("Detected colour:", colour)
    colour = detect_dominant_colour(r"backend\green_jumper.jpeg")
    print("Detected colour:", colour)
    colour = detect_dominant_colour(r"backend\blue_jumper.jpeg")
    print("Detected colour:", colour)
    colour = detect_dominant_colour(r"backend\grey_jeans.jpeg")
    print("Detected colour:", colour)