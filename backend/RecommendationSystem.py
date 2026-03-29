from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
import os
import ast
import re
import io
import base64
from PIL import Image
import genai  # make sure you have the Gemini SDK installed

def recommend(uploads, descriptions, valid_colours):
    # predicts type of clothing and color and gives a prompt to AI model to generate a 3D visual representation
    client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    for upload in uploads:
        type_of_clothes = predict(upload)
        colour_of_clothes = detect_dominant_colour(upload)
        descriptions.append((type_of_clothes, colour_of_clothes))

    formatted_descriptions = ", ".join([f"{t} ({c})" for t, c in descriptions])

    prompt = (
        f"The user has the following clothes: {formatted_descriptions}. "
        "Suggest one full outfit that complements the user's clothes. "
        "Return only a Python list of tuples in the form (type of clothing, colour). "
        "Use only these types: dress, shirt, shoes, shorts, skirt, t-shirt, trousers, outerwear "
        f"and only these colours: {', '.join(valid_colours)}. "
        "Do not include any text outside the list, no explanations, no quotes, nothing else."
    )

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