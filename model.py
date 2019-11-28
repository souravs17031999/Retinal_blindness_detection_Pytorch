# Importing all packages 
import numpy as np
import matplotlib.pyplot as plt
from torch.utils import data
import torch
from torch import nn
from torch import optim
import torchvision
import torch.nn.functional as F
from torchvision import datasets, transforms, models
import torchvision.models as models
from PIL import Image, ImageFile
import json
from torch.optim import lr_scheduler
import random
import os
import sys

print('Imported packages')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet152(pretrained=False)
num_ftrs = model.fc.in_features
out_ftrs = 5
model.fc = nn.Sequential(nn.Linear(num_ftrs, 512),nn.ReLU(),nn.Linear(512,out_ftrs),nn.LogSoftmax(dim=1))
criterion = nn.NLLLoss()
optimizer = torch.optim.Adam(filter(lambda p:p.requires_grad,model.parameters()) , lr = 0.00001)

scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
model.to(device);
# to unfreeze more layers


for name,child in model.named_children():
    if name in ['layer2','layer3','layer4','fc']:
        #print(name + 'is unfrozen')
        for param in child.parameters():
            param.requires_grad = True
    else:
        #print(name + 'is frozen')
        for param in child.parameters():
            param.requires_grad = False
optimizer = torch.optim.Adam(filter(lambda p:p.requires_grad,model.parameters()) , lr = 0.000001)
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

def load_model(path):
    checkpoint = torch.load(path,map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    return model
def inference(model, file, transform, classes):
    file = Image.open(file).convert('RGB')
    img = transform(file).unsqueeze(0)
    print('Transforming your image...')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    with torch.no_grad():
        print('Passing your image to the model....')
        out = model(img.to(device))
        ps = torch.exp(out)
        top_p, top_class = ps.topk(1, dim=1)
        value = top_class.item()
        print("Predicted Severity Value: ", value)
        print("class is: ", classes[value])
        print('Your image is printed:')
        return value, classes[value]
        # plt.imshow(np.array(file))
        # plt.show()


model = load_model('../Desktop/classifier.pt')
print("Model loaded Succesfully")
classes = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']
test_transforms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((224, 224)),
    torchvision.transforms.RandomHorizontalFlip(p=0.5),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])
def main(path):
    x, y = inference(model, path, test_transforms, classes)
    return x, y
# if __name__ == '__model__':
#     # test_dir = '../Desktop/eye'
#     # folders = os.listdir(test_dir)
#     # for num in range(len(folders)):
#     #     path = test_dir+"/"+folders[num]
#     #     print(path)
#     #     inference(model, path, test_transforms, classes)
#     l = sys.argv
#     if(len(l)>1):
#         for i in range(1, len(l)):
#             print(l[i])
#             path = l[i]
#             inference(model, path, test_transforms, classes)
#     else:
#         print('please provide the exact path of image !')
