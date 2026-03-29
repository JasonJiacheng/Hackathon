from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
from colourSuggestion import getValidColours
import os
import ast
import re
import base64
import requests
 
 
# ── clients ──────────────────────────────────────────────────────────────────
 
def get_openrouter_client():
    return OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
 
 
# ── main ─────────────────────────────────────────────────────────────────────
 
def main(uploads):
    descriptions = []
    output, descriptions = recommend(uploads, descriptions, True)
    fileAddress = draw_model(descriptions, output, "modelClothes.png")
    return fileAddress
 
 
# ── outfit recommendation ────────────────────────────────────────────────────
 
def recommend(uploads, descriptions = [], is_smart= True):
    client = get_openrouter_client()
 
    detected_colours = []
    for upload in uploads:
        clothing_type = predict(upload)
        colour = detect_dominant_colour(upload)
        descriptions.append((clothing_type, colour))
        detected_colours.append(colour)
 
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
        "Suggest one complete complementary outfit that makes sense in real life. "
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
            return (ast.literal_eval(match.group()), descriptions)
        except Exception as e:
            print(f"Warning: could not parse outfit list: {e}")
    else:
        print("Warning: no list found in model response.")
 
    return ([], descriptions)
 
 
# ── image generation ─────────────────────────────────────────────────────────
 
def draw_model(descriptions, recommended_outfit, output_file = "ModelClothes.png"):
    """
    Generate a mannequin image via OpenRouter and save it as a PNG.
 
    OpenRouter image generation uses /v1/chat/completions with modalities=["image"],
    NOT the /v1/images/generations endpoint (which is why the original code 404'd).
    The image is returned as a base64 data URL inside choices[0].message.images.
    """
    all_items = descriptions + recommended_outfit
    outfit_text = ", ".join(f"{colour} {clothing}" for clothing, colour in all_items)
 
    prompt = (
        f"A photorealistic full-body 3D mannequin wearing a complete outfit: {outfit_text}. "
        "Plain white studio background, soft studio lighting, high quality, fashion photography style."
    )
 
    print(f"Generating image for outfit: {outfit_text}")
 
    # OpenRouter image generation: use chat/completions with modalities param.
    # flux.2-pro is an image-only model so modalities=["image"] (no "text").
    # Switch to "google/gemini-2.5-flash-image" if you prefer Gemini on OpenRouter.
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": "black-forest-labs/flux.2-pro",
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image"],
            "image_config": {"aspect_ratio": "3:4"},  # portrait — good for full-body
        },
        timeout=120,
    )
 
    response.raise_for_status()
    data = response.json()
 
    message = data["choices"][0]["message"]
    images = message.get("images")
 
    if not images:
        print("Error: no images returned in response.")
        print("Response was:", data)
        return
 
    # Images come back as base64 data URLs: "data:image/png;base64,<data>"
    data_url = images[0]["image_url"]["url"]
    base64_data = data_url.split(",", 1)[1]
 
    with open(output_file, "wb") as f:
        f.write(base64.b64decode(base64_data))
 
    print(f"Image saved to: {output_file}")
    return output_file
 
 
# ── location & weather helpers ────────────────────────────────────────────────
 
def get_area():
    resp = requests.get("https://ipinfo.io/json", timeout=5)
    resp.raise_for_status()
    city = resp.json().get("city")
    if not city:
        raise ValueError("Could not determine city from IP.")
    return city
 
 
def get_weather(city):
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
    uploads = [r"C:\Documents\Hackathon\imagesUploaded\blue_jumper.jpeg", r"C:\Documents\Hackathon\imagesUploaded\orange_shirt.jpg"]
    main(uploads)
