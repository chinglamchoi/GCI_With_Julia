import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import model


# Define model & load pretrained model from model.py for inference
net = model.run_cnn()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
if device != "cpu":
    gpuu = True
    net.to(device)
else:
    gpuu = False

checkpoint = torch.load("models/fmnist_sgd5.pt")
net.load_state_dict(checkpoint["net"])


# Loading test set for inference
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
    ])
testset = datasets.FashionMNIST(root="./data", train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False) #Yoshua Bengio Neurips

classes = ("T-Shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot")


# Inference 
net = net.eval()
total, correct = 0,0
for images,labels in testloader:
    images, labels = (images.to(device), labels.to(device)) if gpuu else (images, labels)
    outputs = net(images).to(device) if gpuu else net(images)
    _, predicted = torch.max(outputs.data, 1) ######
    total += labels.size(0)
    correct += (predicted == labels).float().sum().item()
    # Accuracy
acc = correct/total
print("Test Accuracy: %.4f"%(acc))
