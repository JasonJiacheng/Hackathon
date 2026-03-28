import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import sys

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL_PATH  = r"backend\clothing_model_best.pth"
IMAGE_PATH  = r"backend\grey_jeans.jpeg"  # ← change this
CLASS_NAMES = ['dress', 'outwear', 'shirt', 'shoes', 'shorts', 'skirt', 't-shirt', 'trousers']

# ---------------------------------------------------------------------------
# Model — must match the architecture used during training
# ---------------------------------------------------------------------------
class ClothingCNN(nn.Module):
    def __init__(self, num_classes):
        super(ClothingCNN, self).__init__()
        self.conv1   = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2   = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3   = nn.Conv2d(32, 64, 3, padding=1)
        self.pool    = nn.MaxPool2d(2, 2)
        self.fc1     = nn.Linear(64 * 8 * 8, 128)
        self.fc2     = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 128 → 64
        x = self.pool(F.relu(self.conv2(x)))  # 64 → 32
        x = self.pool(F.relu(self.conv3(x)))  # 32 → 16
        x = self.pool(x)                      # 16 → 8
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        return self.fc2(x)

# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model  = ClothingCNN(num_classes=len(CLASS_NAMES)).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

# ---------------------------------------------------------------------------
# Predict
# ---------------------------------------------------------------------------
def predict(image_path: str) -> tuple[str, float]:
    image  = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        probs         = torch.softmax(model(tensor), dim=1)[0]
        predicted_idx = probs.argmax().item()
        confidence    = probs[predicted_idx].item() * 100
    return CLASS_NAMES[predicted_idx], confidence

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        label, confidence = predict(IMAGE_PATH)
        print(f"Clothing type : {label}")
        print(f"Confidence    : {confidence:.1f}%")
    except FileNotFoundError:
        print(f"Error: file not found — {IMAGE_PATH}")