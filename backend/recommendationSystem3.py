from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
import os
import ast
import re
import base64
import requests
from colourSuggestion import getValidColours
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def main():
    uploads = []
    descriptions = [("Trousers", "Blue"), ("T-shirt", "Red")]
    output = recommend(uploads, descriptions, True)
    print(output)
    draw_model(descriptions, output, "test.png")

def recommend(uploads, descriptions, is_smart):
    detected_colours = []
    for upload in uploads:
        type_of_clothes = predict(upload)
        colour_of_clothes = detect_dominant_colour(upload)
        descriptions.append((type_of_clothes, colour_of_clothes))
        detected_colours.append(colour_of_clothes)

    valid_colours = set()
    for col in detected_colours:
        valid_colours.update(getValidColours(col))
    valid_colours = list(valid_colours)
    formatted_descriptions = ", ".join([f"{t} ({c})" for t, c in descriptions])
    prompt = (
        f"The user has the following clothes: {formatted_descriptions}. "
        "Suggest one full outfit that complements the user's clothes. "
        "Return only a Python list of tuples in the form (type of clothing, colour). "
        "Use only these types: dress, shirt, shoes, shorts, skirt, t-shirt, trousers, outerwear "
        f"and only these colours: {', '.join(valid_colours)}. "
        "Do not include any text outside the list, no explanations, no quotes, nothing else. "
    )
    if is_smart:
        prompt += "Focus your outfit to match these conditions: " + getArea() + " " + getWeather(getArea())

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[{"role": "user", "content": prompt}]
    )
    raw_text = response.choices[0].message.content.strip()

    match = re.search(r"\[.*\]", raw_text, re.DOTALL)
    if match:
        try:
            outfit_list = ast.literal_eval(match.group())
        except Exception:
            outfit_list = []
    else:
        outfit_list = []
    return outfit_list

def draw_model(descriptions, outputFromAI, output_file):
    prompt = (
        f"A 3D mannequin wearing this outfit: {descriptions} {outputFromAI}. "
        "Clean white background, realistic clothing, full body visible."
    )

    # Use Pollinations AI — completely free, no key needed
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

    response = requests.get(url, timeout=60)
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Image saved to {output_file}")

def getArea():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    return data.get("city")

def getWeather(city):
    API_KEY = "bd5e378503939ddaee76f12ad7a97608"
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=parameters)
    data = response.json()
    temp = round(data["main"]["temp"])
    desc = data["weather"][0]["main"].lower()
    return "temperature: " + str(temp) + " degrees, description: " + desc

main()