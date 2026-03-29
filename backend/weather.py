import requests

#Input parameter is a city string
def getWeather(city="Bath"):
    API_KEY = "bd5e378503939ddaee76f12ad7a97608"
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(url, params=parameters)
    data = response.json()

    temp = round(data["main"]["temp"])
    desc = data["weather"][0]["main"].lower()

    return "temperature: "+str(temp) + " degrees, " + " description: " + desc

#Test line (sarun remove if want)
print(getWeather("Bath"))