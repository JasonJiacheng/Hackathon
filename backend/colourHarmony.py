import csv  
  
colorNames = {
    "#ff0000": "Red",
    "#ffff00": "Yellow",
    "#0000ff": "Blue",
    "#00ff00": "Green",
    "#ffa500": "Orange",
    "#800080": "Purple",
    "#ffc0cb": "Pink",
    "#a52a2a": "Brown",
    "#000000": "Black",
    "#ffffff": "White",
    "#808080": "Grey"
}

def isValidHex(color):
    try:
        return color.startswith("#") and len(color) == 7 and bool(int(color[1:], 16) >= 0)
    except ValueError:
        return False

def hexToRgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgbDistance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(hexToRgb(c1), hexToRgb(c2)))

def closestColorName(hex):
    return min(colorNames, key=lambda ref: rgbDistance(hex, ref))

def loadDataset(csvFile):
    with open(csvFile, newline='', encoding='utf-8') as f:
        return [{
            "color1Hex":   r["Color_1_Hex"].strip().lower(),
            "color1Name":  r["Color_1_Name"].strip(),
            "color2Hex":   r["Color_2_Hex"].strip().lower(),
            "color2Name":  r["Color_2_Name"].strip(),
            "style":       r["Style_Category"].strip(),
            "description": r["Description"].strip(),
        } for r in csv.DictReader(f)]

def pairScore(inputColor, pair):
    d1, d2 = rgbDistance(inputColor, pair["color1Hex"]), rgbDistance(inputColor, pair["color2Hex"])
    return (min(d1, d2), max(d1, d2))

def suggestOutfits(inputColor, csvFile, topN=3):
    return sorted(loadDataset(csvFile), key=lambda p: pairScore(inputColor, p))[:topN]

if __name__ == "__main__":
    userInput = input("Enter a hex color (e.g. #58c05e): ").strip().lower()

    if not isValidHex(userInput):
        print("Invalid hex color. Please use format like #58c05e")
        exit()

    print(f"\nYour Input Color: {colorNames.get(userInput, closestColorName(userInput))} ({userInput})")
    print(f"\nTop 3 suggested colour pairings:\n")

    for i, pair in enumerate(suggestOutfits(userInput, "clothing_colour_combinations.csv"), start=1):
        print(f"  Outfit {i}: {pair['color1Name']} ({pair['color1Hex']}) + {pair['color2Name']} ({pair['color2Hex']})")
        print(f"  Style: {pair['style']} — {pair['description']}\n")
