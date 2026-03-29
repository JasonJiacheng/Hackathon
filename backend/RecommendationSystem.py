from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
import os
import ast
import re
import io
import base64
from PIL import Image
import genai  
import requests
from colourSuggestion import getValidColours
def main(): #main is just for testing
    uploads = []
    descriptions = [("Trousers", "Blue"), ("T-shirt", "Red")]
    output = recommend(uploads, descriptions, True)
    print(output)
    draw_model(descriptions, output, "test.png")
    
def recommend(uploads, descriptions, is_smart): #is_smart is a toggle on/off switch bool
    client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

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

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    raw_text = response.output_text.strip()
    match = re.search(r"\[.*\]", raw_text, re.DOTALL)

    if match:
        try:
            outfit_list = ast.literal_eval(match.group())
        except Exception:
            outfit_list = []
    else:
        outfit_list = []

    return outfit_list       

def draw_model(descriptions, outputFromOpenAI, output_file):
    client = genai.Client()  # Gemini client
    prompt_text = (
        f"I have this description of an outfit: {descriptions} {outputFromOpenAI}. "
        "Draw a 3D model of this outfit on a mannequin/doll. "
        "Keep it plain and generic, strictly following the colour and type of clothing specified."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt_text
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data"):
            image_data = base64.b64decode(part.inline_data.data)
            image = Image.open(io.BytesIO(image_data))
            image.save(output_file)

def getArea():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    area = data.get("city")
    return area
    #returns string saying The user lives in area, and this will be added onto the prmpt of reccomendation system

def getWeather(city):
    API_KEY = "bd5e378503939ddaee76f12ad7a97608"
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=parameters)
    data = response.json()
    temp = round(data["main"]["temp"])
    desc = data["weather"][0]["main"].lower()
    return "temperature: "+ str(temp) + " degrees, " + " description: " + desc

main()

