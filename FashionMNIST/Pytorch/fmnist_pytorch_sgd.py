import torch
import torch.optim as optim
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import model

# Define model
net = model.run_cnn()
#save_number = input("save file number: ")
save_number = ""
#a = input("gpu number: ")
a = "0"
a = "cuda:" + a
device = torch.device(a if torch.cuda.is_available() else "cpu")
if device != "cpu":
    gpuu = True
    net.to(device)
else:
    gpuu = False


# Load data for training & inference
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
    ])
trainset = datasets.FashionMNIST(root="./data", train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64)
testset = datasets.FashionMNIST(root="./data", train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False) #Yoshua Bengio Neurips


# More hyperparameters
epochs, alpha = 200, 0.1
classes = ("T-Shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot")

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=alpha, momentum=0.9, weight_decay=1e-04)
best_acc, last_improvement, threshhold = 0.0, 0, 0.99


# Training & Testing
for epoch in range(1, epochs+1):
    # Train 1 epoch
    net = net.train()
    for images, labels in trainloader:
        images, labels = (images.to(device), labels.to(device)) if gpuu else (images, labels)
        optimizer.zero_grad()
        outputs = net(images).to(device) if gpuu else net(images)
        loss = criterion(outputs, labels)        
        loss.backward()
        optimizer.step()

    # Test
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
    print("[%i]:"%(epoch), "Test Accuracy: %.4f"%(acc))

    # Early exit at 99% accuracy
    if acc >= threshhold:
        print(" -> Early-exiting: We reached our target accuracy of 90.0%")
        break
    
    if acc >= best_acc:
        # save weights:
        state = {
            "net":net.state_dict(),
            "acc": acc,
            "epoch": epoch,
            "optimizer": optimizer.state_dict(),
            "alpha": alpha
            }
        torch.save(state, str("./models/fmnist_sgd" + save_number + ".pt"))
        print(" -> New best accuracy! Saving model out to fmnist_sgd" + save_number + ".pt")
        best_acc, last_improvement = acc, epoch
    
    # Learning rate decay to dampen oscillations
    if epoch - last_improvement >= 10 and alpha > 1e-4:
        alpha /= 10
        for param_group in optimizer.param_groups:
            param_group["lr"] = alpha
        print(" -> Haven't improved in a while, dropping learning rate to %f!"%(alpha))
        last_improvement = epoch

    if epoch - last_improvement >= 20:
        print(" -> We're calling this converged.")
        break
