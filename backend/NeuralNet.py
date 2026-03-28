#We define the neural network:
import sys
sys.path.insert(0, r"C:\Users\sm4134\AppData\Roaming\Python\Python313\site-packages")
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
from PIL import Image

class ClothingCNN(nn.Module):
    #224×224 pixels with 3 color channels (RGB) expected
    def __init__(self, num_classes):
        super(ClothingCNN, self).__init__()
        #Now set up the convolutional layers 
        #Convolution adds each element of an image to its local neighbors, weighted by a kernel, or a small matrix, 
        #That helps us extract certain features (like edge detection, sharpness, blurriness, etc.) from the input image.
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)  #3 input channels, 16 output channels, 3x3 kernel
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2) #reduces image size by half (2x2 window)
        self.fc1 = nn.Linear(64 * 28 * 28, 128) # the flattened feature map size after all convolutions and pooling 
        self.fc2 = nn.Linear(128, num_classes) #128 inputs -> num_classes outputs 
        self.dropout = nn.Dropout(0.3) #Randomly drops 30% of neurons to prevent overfitting (model performs well on training data, but not unseen)

    def forward(self, x): #x here is the input image 
        x = self.pool(F.relu(self.conv1(x)))  #We apply the convolution, then the activation, and then pooling. 224 x 224 -> 112x112
        x = self.pool(F.relu(self.conv2(x)))  #112x112 -> 56x56
        x = self.pool(F.relu(self.conv3(x)))  #56x56 -> 28x28
        x = x.view(x.size(0), -1) #Converts 3d feature vectors into a 1D vector for fully connected layers (flattens), but keeps batch dimension
        x = self.dropout(F.relu(self.fc1(x))) #hidden layer with dropout 
        x = self.fc2(x) #output layer (raw scores for each clothing category)
        return x
    
def evaluate(model, val_loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return accuracy

transform = transforms.Compose([transforms.Resize((224, 224)),transforms.ToTensor()])
#Creates a pipeline of image transformations that will be applied to every image before being fed into the neural network 
#Transforms.compose combines multiple transformations into a single pipeline 
#toTensor converts the PIL image to a pytorch tensor 
#Load all data
full_dataset = datasets.ImageFolder(r"C:\\Users\\sm4134\\Downloads\\Dataset\\Train", transform=transform)
#Split into train (80%) and validation (20%) data
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_data, val_data = random_split(full_dataset, [train_size, val_size]) #Performs the split
#Create data loaders
train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
val_loader = DataLoader(val_data, batch_size=16)
#We now want to train the CNN model 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #If GPU compatible, will run on GPU which is much faster
model = ClothingCNN(num_classes=len(full_dataset.classes)).to(device) #Creates an instance of the CNN
criterion = nn.CrossEntropyLoss() #defines the loss function for multi-class classification, measures how far 
#The model's predictions are from actual labels, we want a LOWER loss for BETTER predictions
optimizer = optim.Adam(model.parameters(), lr=0.001) #Applies Adam's optimisation algorithm that updates model weights
best_accuracy = 0
best_epoch = 0 
for epoch in range(5): #An epoch is a full run through the dataset 
    model.train()
    running_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}")
    accuracy = evaluate(model, val_loader, device)
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_epoch = epoch + 1
        torch.save(model.state_dict(), 'clothing_model_best.pth')
        print(f"New best model has been saved: Epoch {best_epoch} with accuracy: {best_accuracy:.2f}%")
print(f"\nTraining complete! Best model was from Epoch {best_epoch} with {best_accuracy:.2f}% accuracy")

model.load_state_dict(torch.load('clothing_model_best.pth'))
print(f"Loaded best model from Epoch {best_epoch}")


#Predicts the class of an image
def predict(image_path):
    model.eval() #Sets model to evaluation mode
    image = Image.open(image_path).convert("RGB") #Ensures only 3 colour channels
    image = transform(image).unsqueeze(0).to(device) #Unsqueeze adds a batch dimension (from 3×224×224 to 1×3×224×224)
    with torch.no_grad(): #Disables derivative calculation to save memory and computation since we're only predicting 
        outputs = model(image) #Sets up to get predictions for the single image 
        _, predicted = torch.max(outputs, 1) #_ ignores the max value, predicted stores the class indices 
        #Such that for a single image, predicted will be a tensor with one value 
    return full_dataset.classes[predicted.item()]

#Testing with unseen images
if __name__ == "__main__":
    test_images = [
        "C:\\Users\\sm4134\\Downloads\\t1.jfif",
        "C:\\Users\\sm4134\\Downloads\\t2.jfif",
        "C:\\Users\\sm4134\\Downloads\\trouser1.jfif"
    ]
    for img_path in test_images:
        try:
            prediction = predict(img_path)
            print(f"{img_path}: {prediction}")
        except FileNotFoundError:
            print(f"File not found: {img_path}")
