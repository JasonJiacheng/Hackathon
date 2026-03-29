from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
from colourSuggestion import getValidColours
import os
import ast
import re
import base64
import requests


def main():
    uploads = []
    descriptions = [("Trousers", "Blue"), ("T-shirt", "Red")]
    output = recommend(uploads, descriptions, is_smart=True)
    print("Recommended outfit:", output)
    draw_model(descriptions, output, "test.png")


def get_client():
    """Create and return an OpenRouter-compatible OpenAI client."""
    return OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


def recommend(uploads, descriptions, is_smart=False):
    """
    Given a list of image uploads and/or manual descriptions, recommend a full outfit.

    Args:
        uploads: list of image file paths to analyse automatically.
        descriptions: list of (clothing_type, colour) tuples already known.
        is_smart: if True, tailor the outfit suggestion to local weather.

    Returns:
        List of (clothing_type, colour) tuples representing the recommended outfit.
    """
    client = get_client()

    # Detect clothing from uploaded images and append to descriptions
    detected_colours = []
    for upload in uploads:
        clothing_type = predict(upload)
        colour = detect_dominant_colour(upload)
        descriptions.append((clothing_type, colour))
        detected_colours.append(colour)

    # Build the allowed colour list from detected colours (if any uploads were given)
    valid_colours = set()
    for col in detected_colours:
        valid_colours.update(getValidColours(col))
    valid_colours = list(valid_colours)

    formatted_descriptions = ", ".join([f"{t} ({c})" for t, c in descriptions])

    colour_constraint = (
        f"Use only these colours: {', '.join(valid_colours)}. "
        if valid_colours
        else ""
    )

    prompt = (
        f"The user already owns the following clothes: {formatted_descriptions}. "
        "Suggest one complete outfit that complements what they own. "
        "Return ONLY a Python list of tuples in the form [(type, colour), ...]. "
        "Allowed clothing types: dress, shirt, shoes, shorts, skirt, t-shirt, trousers, outerwear. "
        f"{colour_constraint}"
        "Do not include any explanation, markdown, or text outside the list."
    )

    if is_smart:
        try:
            area = get_area()
            weather = get_weather(area)
            prompt += f" Tailor the outfit for this location and weather — {area}: {weather}."
        except Exception as e:
            print(f"Warning: could not fetch weather/location data: {e}")

    response = client.chat.completions.create(
        model="openai/gpt-4o",  # OpenRouter model string
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw_text = response.choices[0].message.content.strip()

    # Extract the Python list from the response
    match = re.search(r"\[.*?\]", raw_text, re.DOTALL)
    if match:
        try:
            outfit_list = ast.literal_eval(match.group())
        except Exception as e:
            print(f"Warning: could not parse outfit list: {e}")
            outfit_list = []
    else:
        print("Warning: no list found in model response.")
        outfit_list = []

    return outfit_list


def draw_model(descriptions, recommended_outfit, output_file):
    """
    Generate an image of a mannequin wearing the given outfit and save it to disk.

    Args:
        descriptions: list of (type, colour) tuples the user already owns.
        recommended_outfit: list of (type, colour) tuples from recommend().
        output_file: path where the resulting PNG will be saved.
    """
    client = get_client()

    all_items = descriptions + recommended_outfit
    outfit_text = ", ".join([f"{colour} {clothing}" for clothing, colour in all_items])

    prompt = (
        f"A photorealistic 3D mannequin wearing a full outfit: {outfit_text}. "
        "Plain white background, full body shot, studio lighting, high quality."
    )

    result = client.images.generate(
        model="openai/gpt-image-1",  # OpenRouter image model
        prompt=prompt,
        response_format="b64_json",
        n=1,
    )

    image_base64 = result.data[0].b64_json
    if not image_base64:
        print("Error: no image data returned from the API.")
        return

    with open(output_file, "wb") as f:
        f.write(base64.b64decode(image_base64))

    print(f"Image saved to {output_file}")


def get_area():
    """Return the user's city based on their IP address."""
    response = requests.get("https://ipinfo.io/json", timeout=5)
    response.raise_for_status()
    data = response.json()
    city = data.get("city")
    if not city:
        raise ValueError("Could not determine city from IP.")
    return city


def get_weather(city):
    """
    Return a short weather description string for the given city.

    Args:
        city: city name string.

    Returns:
        e.g. "temperature: 18 degrees, description: cloudy"
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY", "bd5e378503939ddaee76f12ad7a97608")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    temp = round(data["main"]["temp"])
    description = data["weather"][0]["main"].lower()
    return f"temperature: {temp} degrees, description: {description}"


if __name__ == "__main__":
    main()
