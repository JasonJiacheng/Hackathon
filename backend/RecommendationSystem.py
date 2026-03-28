import sys
sys.path.insert(0, r"C:\Users\sm4134\AppData\Roaming\Python\Python313\site-packages")
from openai import OpenAI
from clothing_detector import predict
from colourDetector import detect_dominant_colour
#Get the uploads from ifi's folder
#Put them in the uploads list
uploads = []
descriptions = [("Shorts", "Red"), ("Top", "Blue")]
for upload in uploads:
    type_of_clothes = predict(upload)
    colour_of_clothes = detect_dominant_colour(upload)
    descriptions.append(type_of_clothes, colour_of_clothes)
client = OpenAI()
response = client.responses.create(
    model = "gpt-5.4",
    input = "The user has got the following clothes: " + descriptions + ", I want you to create a list of type of clothes along with their colours that would go well with the clothes the user has already got."
    + " Utilise strong colour theory and have good sense of fashion, they must look good with your recommendations. Your reccomendations must be of the form <type of clothe>, <colour> where"
    + " the type of clothe is one of: dress, shirt, shoes, shorts, skirt, t-shirt, trousers, outwear and the colour is one of: red, yellow, blue, green, orange, purple, pink, black, white, grey."
    )
print(response.output[0].content[0].text)
