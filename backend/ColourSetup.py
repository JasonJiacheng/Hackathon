#Colour theory was based on https://www.colormatters.com/color-and-design/basic-color-theory
#Sets up colours that will be accessible in the app
#The dictionary contains hex for each colour, to be implemented by front end
coloursOwned = []
primaryColoursOwned = []
secondaryColoursOwned = []
tertiaryColoursOwned = []
colourPalette = {
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "blue": "#0000FF",
    "green": "#00FF00",
    "orange": "#FFA500",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "brown": "#A52A2A",
    "black": "#000000",
    "white": "#FFFFFF",
    "grey": "#808080"
}
def categoriseColours(coloursOwned):
    for colour in coloursOwned:
        if(isPrimary(colour)):
            primaryColoursOwned.append(colour)
        elif(isSecondary(colour)):
            secondaryColoursOwned.append(colour)
        else:
            tertiaryColoursOwned.append(colour)

def isPrimary(colour):
    if(colour == "red" or colour == "yellow" or colour == "blue"):
        return True
    else:
        return False
    
def isSecondary(colour):
    if(colour == "green" or colour == "orange" or colour == "purple"):
        return True
    else:
        return False
    
def getColoursNotOwned(coloursOwned):
    coloursNotOwned = []
    for dictColour in colourPalette:
        isOwned = False
        for colour in coloursOwned:
            if colour == dictColour:
                isOwned = True
        if not isOwned:
            coloursNotOwned.append(dictColour)
    return coloursNotOwned 
