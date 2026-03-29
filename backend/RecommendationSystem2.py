from openai import OpenAI
from google import genai
from google.genai import types
from clothing_detector import predict
from colourDetector import detect_dominant_colour
from colourSuggestion import getValidColours
import os
import ast
import re
import requests


# ── clients ──────────────────────────────────────────────────────────────────

def get_openrouter_client():
    """OpenRouter client (used for text / outfit recommendation only)."""
    return OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

def get_gemini_client():
    """Google GenAI client (used for image generation via Imagen)."""
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    uploads = []
    descriptions = [("Trousers", "Blue"), ("T-shirt", "Red")]

    output = recommend(uploads, descriptions, is_smart=True)
    print("Recommended outfit:", output)

    draw_model(descriptions, output, "test.png")


# ── outfit recommendation (OpenRouter) ───────────────────────────────────────

def recommend(uploads, descriptions, is_smart=False):
    """
    Recommend a full outfit that complements what the user owns.

    Args:
        uploads:      list of image file paths to auto-detect clothing from.
        descriptions: list of (clothing_type, colour) tuples already known.
        is_smart:     if True, tailor the suggestion to local weather.

    Returns:
        List of (clothing_type, colour) tuples.
    """
    client = get_openrouter_client()

    # Detect clothing from any uploaded images
    detected_colours = []
    for upload in uploads:
        clothing_type = predict(upload)
        colour = detect_dominant_colour(upload)
        descriptions.append((clothing_type, colour))
        detected_colours.append(colour)

    # Build allowed colour list (only if we auto-detected colours)
    valid_colours = set()
    for col in detected_colours:
        valid_colours.update(getValidColours(col))
    valid_colours = list(valid_colours)

    formatted = ", ".join(f"{t} ({c})" for t, c in descriptions)
    colour_constraint = (
        f"Use only these colours: {', '.join(valid_colours)}. " if valid_colours else ""
    )

    prompt = (
        f"The user already owns: {formatted}. "
        "Suggest one complete complementary outfit. "
        "Return ONLY a Python list of tuples: [(clothing_type, colour), ...]. "
        "Allowed types: dress, shirt, shoes, shorts, skirt, t-shirt, trousers, outerwear. "
        f"{colour_constraint}"
        "No explanation, no markdown, nothing outside the list."
    )

    if is_smart:
        try:
            area = get_area()
            weather = get_weather(area)
            prompt += f" Tailor the outfit for this location and weather — {area}: {weather}."
        except Exception as e:
            print(f"Warning: could not fetch weather/location: {e}")

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r"\[.*?\]", raw, re.DOTALL)
    if match:
        try:
            return ast.literal_eval(match.group())
        except Exception as e:
            print(f"Warning: could not parse outfit list: {e}")
    else:
        print("Warning: no list found in model response.")

    return []


# ── image generation (Google Gemini Imagen) ───────────────────────────────────

def draw_model(descriptions, recommended_outfit, output_file):
    """
    Generate a mannequin image wearing the outfit and save it as a PNG.

    Uses Google's Imagen 4 directly — OpenRouter does NOT support image
    generation, which is why the old code crashed with a 404.

    Requires: GEMINI_API_KEY env var (get one free at aistudio.google.com)
    Install:  pip install google-genai

    Args:
        descriptions:       list of (type, colour) the user already owns.
        recommended_outfit: list of (type, colour) from recommend().
        output_file:        path to save the resulting PNG.
    """
    client = get_gemini_client()

    all_items = descriptions + recommended_outfit
    outfit_text = ", ".join(f"{colour} {clothing}" for clothing, colour in all_items)

    prompt = (
        f"A photorealistic full-body 3D mannequin wearing a complete outfit: {outfit_text}. "
        "Plain white studio background, soft studio lighting, high quality, fashion photography style."
    )

    print(f"Generating image for outfit: {outfit_text}")

    result = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/png",
            aspect_ratio="3:4",           # portrait — good for full-body shots
            person_generation="ALLOW_ALL",
        ),
    )

    if not result.generated_images:
        print("Error: Imagen returned no images.")
        return

    # .image is a PIL Image object — just call .save() directly
    result.generated_images[0].image.save(output_file)
    print(f"Image saved to: {output_file}")


# ── location & weather helpers ────────────────────────────────────────────────

def get_area():
    """Return the user's city based on their public IP."""
    resp = requests.get("https://ipinfo.io/json", timeout=5)
    resp.raise_for_status()
    city = resp.json().get("city")
    if not city:
        raise ValueError("Could not determine city from IP.")
    return city


def get_weather(city):
    """Return a short weather string for the given city."""
    api_key = os.environ.get("OPENWEATHER_API_KEY", "bd5e378503939ddaee76f12ad7a97608")
    resp = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "metric"},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    temp = round(data["main"]["temp"])
    desc = data["weather"][0]["main"].lower()
    return f"{temp}C, {desc}"


if __name__ == "__main__":
    main()
