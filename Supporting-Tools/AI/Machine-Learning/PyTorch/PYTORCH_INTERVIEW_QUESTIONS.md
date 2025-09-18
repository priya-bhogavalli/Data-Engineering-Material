# PyTorch Interview Questions

## Basic Concepts

### 1. What is PyTorch and how does it differ from TensorFlow?
**Answer:** PyTorch is an open-source deep learning framework developed by Facebook. Key differences:

**PyTorch:**
- Dynamic computational graphs (define-by-run)
- Pythonic and intuitive API
- Eager execution by default
- Better for research and prototyping

**TensorFlow:**
- Static computational graphs (define-then-run) in 1.x
- More production-oriented ecosystem
- Better deployment tools
- Stronger mobile/edge support

```python
import torch
import torch.nn as nn
import torch.optim as optim

# PyTorch dynamic graph example
x = torch.randn(3, 4, requires_grad=True)
y = x ** 2
z = y.mean()

print(f"Input shape: {x.shape}")
print(f"Output: {z}")

# Backward pass
z.backward()
print(f"Gradients: {x.grad}")
```

### 2. What are tensors in PyTorch and how do you create them?
**Answer:** Tensors are multi-dimensional arrays similar to NumPy arrays but with GPU support and automatic differentiation.

```python
import torch
import numpy as np

# Creating tensors
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
random = torch.randn(2, 3)  # Normal distribution
uniform = torch.rand(2, 3)  # Uniform [0,1)

# From data
data = [[1, 2], [3, 4]]
tensor_from_data = torch.tensor(data)

# From NumPy
numpy_array = np.array([[1, 2], [3, 4]])
tensor_from_numpy = torch.from_numpy(numpy_array)

# Specify dtype and device
float_tensor = torch.tensor([1, 2, 3], dtype=torch.float32)
gpu_tensor = torch.tensor([1, 2, 3], device='cuda' if torch.cuda.is_available() else 'cpu')

# Tensor operations
a = torch.tensor([[1, 2], [3, 4]])
b = torch.tensor([[5, 6], [7, 8]])

# Element-wise operations
addition = a + b
multiplication = a * b
matrix_mult = torch.matmul(a, b)

print(f"Addition:\n{addition}")
print(f"Matrix multiplication:\n{matrix_mult}")
```

### 3. How does automatic differentiation work in PyTorch?
**Answer:** PyTorch uses automatic differentiation (autograd) to compute gradients automatically.

```python
import torch

# Enable gradient computation
x = torch.tensor([2.0], requires_grad=True)
y = torch.tensor([3.0], requires_grad=True)

# Forward pass
z = x**2 + y**3
loss = z.sum()

print(f"Forward pass result: {loss}")

# Backward pass
loss.backward()

print(f"dL/dx: {x.grad}")  # 2*x = 4
print(f"dL/dy: {y.grad}")  # 3*y^2 = 27

# Gradient accumulation
x.grad.zero_()  # Clear gradients
y.grad.zero_()

# Multiple backward passes
for i in range(3):
    z = x**2 + y**3
    z.backward()
    print(f"Iteration {i+1} - x.grad: {x.grad}, y.grad: {y.grad}")

# Computational graph
x = torch.tensor([1.0], requires_grad=True)
y = x + 2
z = y * y * 3
out = z.mean()

print(f"Computational graph: x -> y -> z -> out")
print(f"x.grad_fn: {x.grad_fn}")
print(f"y.grad_fn: {y.grad_fn}")
print(f"z.grad_fn: {z.grad_fn}")
```

### 4. How do you build neural networks using torch.nn?
**Answer:** PyTorch provides torch.nn module for building neural networks.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# Method 1: Sequential API
model_sequential = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10),
    nn.Softmax(dim=1)
)

# Method 2: Custom nn.Module
class CustomNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(CustomNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)

# Initialize model
model = CustomNet(784, 128, 10)

# Model parameters
print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")

# Forward pass
input_tensor = torch.randn(32, 784)  # Batch size 32
output = model(input_tensor)
print(f"Output shape: {output.shape}")

# Convolutional Neural Network
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

cnn_model = CNN()
```

## Intermediate Concepts

### 5. How do you implement custom datasets and data loaders in PyTorch?
**Answer:** PyTorch provides Dataset and DataLoader classes for efficient data handling.

```python
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from PIL import Image
import os

# Custom Dataset for tabular data
class TabularDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        # Get features and target
        features = self.data.iloc[idx, :-1].values.astype(np.float32)
        target = self.data.iloc[idx, -1]
        
        sample = {'features': torch.tensor(features), 'target': torch.tensor(target)}
        
        if self.transform:
            sample = self.transform(sample)
            
        return sample

# Custom Dataset for images
class ImageDataset(Dataset):
    def __init__(self, root_dir, annotations_file, transform=None):
        self.root_dir = root_dir
        self.annotations = pd.read_csv(annotations_file)
        self.transform = transform
        
    def __len__(self):
        return len(self.annotations)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[idx, 0])
        image = Image.open(img_path)
        label = self.annotations.iloc[idx, 1]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

# Data transformations
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])

# Create dataset and dataloader
# dataset = ImageDataset('path/to/images', 'annotations.csv', transform=transform)
# dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

# Custom collate function
def custom_collate_fn(batch):
    """Custom function to handle variable-length sequences"""
    features = [item['features'] for item in batch]
    targets = [item['target'] for item in batch]
    
    # Pad sequences to same length
    features_padded = torch.nn.utils.rnn.pad_sequence(features, batch_first=True)
    targets_tensor = torch.stack(targets)
    
    return {'features': features_padded, 'targets': targets_tensor}

# DataLoader with custom collate
# dataloader = DataLoader(dataset, batch_size=32, collate_fn=custom_collate_fn)

# Efficient data loading example
class EfficientDataset(Dataset):
    def __init__(self, data_path, preload=False):
        self.data_path = data_path
        self.file_list = os.listdir(data_path)
        self.preload = preload
        
        if preload:
            # Preload all data into memory
            self.data = []
            for file_name in self.file_list:
                data = torch.load(os.path.join(data_path, file_name))
                self.data.append(data)
    
    def __len__(self):
        return len(self.file_list)
    
    def __getitem__(self, idx):
        if self.preload:
            return self.data[idx]
        else:
            # Load data on-the-fly
            file_path = os.path.join(self.data_path, self.file_list[idx])
            return torch.load(file_path)

# Usage with DataLoader
def create_data_loaders(train_dataset, val_dataset, batch_size=32):
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True,  # Faster GPU transfer
        drop_last=True    # Drop incomplete batches
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    return train_loader, val_loader
```

### 6. How do you implement training loops and optimization in PyTorch?
**Answer:** PyTorch provides flexible training loop implementation with various optimizers and schedulers.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, ReduceLROnPlateau
import time

def train_model(model, train_loader, val_loader, num_epochs=10):
    """Complete training loop with validation"""
    
    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = StepLR(optimizer, step_size=7, gamma=0.1)
    
    # Training history
    train_losses = []
    val_losses = []
    train_accuracies = []
    val_accuracies = []
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(num_epochs):
        start_time = time.time()
        
        # Training phase
        model.train()
        running_loss = 0.0
        correct_predictions = 0
        total_samples = 0
        
        for batch_idx, (data, targets) in enumerate(train_loader):
            data, targets = data.to(device), targets.to(device)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(data)
            loss = criterion(outputs, targets)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping (optional)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            # Update weights
            optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += targets.size(0)
            correct_predictions += (predicted == targets).sum().item()
            
            # Print progress
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}, '
                      f'Loss: {loss.item():.4f}')
        
        # Calculate training metrics
        train_loss = running_loss / len(train_loader)
        train_accuracy = 100 * correct_predictions / total_samples
        
        # Validation phase
        val_loss, val_accuracy = evaluate_model(model, val_loader, criterion, device)
        
        # Update learning rate
        scheduler.step()
        
        # Store metrics
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        train_accuracies.append(train_accuracy)
        val_accuracies.append(val_accuracy)
        
        # Print epoch results
        epoch_time = time.time() - start_time
        print(f'Epoch {epoch+1}/{num_epochs} - {epoch_time:.2f}s')
        print(f'Train Loss: {train_loss:.4f}, Train Acc: {train_accuracy:.2f}%')
        print(f'Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}%')
        print('-' * 60)
    
    return {
        'train_losses': train_losses,
        'val_losses': val_losses,
        'train_accuracies': train_accuracies,
        'val_accuracies': val_accuracies
    }

def evaluate_model(model, data_loader, criterion, device):
    """Evaluate model on validation/test set"""
    model.eval()
    total_loss = 0.0
    correct_predictions = 0
    total_samples = 0
    
    with torch.no_grad():
        for data, targets in data_loader:
            data, targets = data.to(device), targets.to(device)
            
            outputs = model(data)
            loss = criterion(outputs, targets)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += targets.size(0)
            correct_predictions += (predicted == targets).sum().item()
    
    avg_loss = total_loss / len(data_loader)
    accuracy = 100 * correct_predictions / total_samples
    
    return avg_loss, accuracy

# Advanced training with mixed precision
from torch.cuda.amp import GradScaler, autocast

def train_with_mixed_precision(model, train_loader, num_epochs=10):
    """Training with automatic mixed precision for faster training"""
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scaler = GradScaler()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(num_epochs):
        model.train()
        
        for batch_idx, (data, targets) in enumerate(train_loader):
            data, targets = data.to(device), targets.to(device)
            
            optimizer.zero_grad()
            
            # Forward pass with autocast
            with autocast():
                outputs = model(data)
                loss = criterion(outputs, targets)
            
            # Backward pass with gradient scaling
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch+1}, Batch {batch_idx}, Loss: {loss.item():.4f}')

# Custom optimizer example
class CustomSGD(optim.Optimizer):
    def __init__(self, params, lr=0.01, momentum=0.9):
        defaults = dict(lr=lr, momentum=momentum)
        super(CustomSGD, self).__init__(params, defaults)
    
    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()
        
        for group in self.param_groups:
            momentum = group['momentum']
            
            for p in group['params']:
                if p.grad is None:
                    continue
                
                d_p = p.grad.data
                
                if momentum != 0:
                    param_state = self.state[p]
                    if len(param_state) == 0:
                        param_state['momentum_buffer'] = torch.zeros_like(p.data)
                    
                    buf = param_state['momentum_buffer']
                    buf.mul_(momentum).add_(d_p)
                    d_p = buf
                
                p.data.add_(d_p, alpha=-group['lr'])
        
        return loss
```

### 7. How do you implement transfer learning in PyTorch?
**Answer:** Transfer learning leverages pre-trained models for new tasks with minimal training.

```python
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms

# Load pre-trained model
def create_transfer_model(num_classes, model_name='resnet18', freeze_features=True):
    """Create transfer learning model"""
    
    if model_name == 'resnet18':
        model = models.resnet18(pretrained=True)
        num_features = model.fc.in_features
        
        # Freeze feature extraction layers
        if freeze_features:
            for param in model.parameters():
                param.requires_grad = False
        
        # Replace classifier
        model.fc = nn.Linear(num_features, num_classes)
        
    elif model_name == 'vgg16':
        model = models.vgg16(pretrained=True)
        
        if freeze_features:
            for param in model.features.parameters():
                param.requires_grad = False
        
        # Modify classifier
        model.classifier[6] = nn.Linear(model.classifier[6].in_features, num_classes)
    
    return model

# Fine-tuning approach
def fine_tune_model(model, unfreeze_layers=2):
    """Fine-tune pre-trained model by unfreezing top layers"""
    
    # First, freeze all layers
    for param in model.parameters():
        param.requires_grad = False
    
    # Unfreeze top layers
    if hasattr(model, 'fc'):  # ResNet
        model.fc.requires_grad_(True)
        
        # Unfreeze last few layers
        layers = list(model.children())
        for layer in layers[-unfreeze_layers:]:
            for param in layer.parameters():
                param.requires_grad = True
    
    elif hasattr(model, 'classifier'):  # VGG
        for param in model.classifier.parameters():
            param.requires_grad = True

# Multi-stage training
def multi_stage_training(model, train_loader, val_loader, num_classes):
    """Multi-stage transfer learning training"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # Stage 1: Train only classifier
    print("Stage 1: Training classifier only")
    for param in model.parameters():
        param.requires_grad = False
    
    # Enable gradients for classifier
    if hasattr(model, 'fc'):
        for param in model.fc.parameters():
            param.requires_grad = True
    
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()), 
        lr=0.001
    )
    
    # Train for few epochs
    train_epochs(model, train_loader, val_loader, optimizer, epochs=5)
    
    # Stage 2: Fine-tune entire model
    print("Stage 2: Fine-tuning entire model")
    for param in model.parameters():
        param.requires_grad = True
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)  # Lower LR
    
    # Train for more epochs
    train_epochs(model, train_loader, val_loader, optimizer, epochs=10)

def train_epochs(model, train_loader, val_loader, optimizer, epochs):
    """Helper function for training epochs"""
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        
        for data, targets in train_loader:
            data, targets = data.to(next(model.parameters()).device), targets.to(next(model.parameters()).device)
            
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}')

# Feature extraction approach
class FeatureExtractor(nn.Module):
    def __init__(self, pretrained_model, layer_name):
        super(FeatureExtractor, self).__init__()
        self.pretrained_model = pretrained_model
        self.layer_name = layer_name
        self.features = None
        
        # Register hook
        self._register_hook()
    
    def _register_hook(self):
        def hook_fn(module, input, output):
            self.features = output
        
        # Find the layer and register hook
        for name, layer in self.pretrained_model.named_modules():
            if name == self.layer_name:
                layer.register_forward_hook(hook_fn)
                break
    
    def forward(self, x):
        _ = self.pretrained_model(x)
        return self.features

# Custom transfer learning with multiple backbones
class EnsembleTransferModel(nn.Module):
    def __init__(self, num_classes):
        super(EnsembleTransferModel, self).__init__()
        
        # Multiple pre-trained backbones
        self.resnet = models.resnet18(pretrained=True)
        self.vgg = models.vgg16(pretrained=True)
        
        # Remove final layers
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-1])
        self.vgg = nn.Sequential(*list(self.vgg.features.children()))
        
        # Freeze pre-trained layers
        for param in self.resnet.parameters():
            param.requires_grad = False
        for param in self.vgg.parameters():
            param.requires_grad = False
        
        # Adaptive pooling for consistent output size
        self.adaptive_pool = nn.AdaptiveAvgPool2d((7, 7))
        
        # Classifier
        combined_features = 512 + 512  # ResNet + VGG features
        self.classifier = nn.Sequential(
            nn.Linear(combined_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        # Extract features from both models
        resnet_features = self.resnet(x)
        resnet_features = resnet_features.view(resnet_features.size(0), -1)
        
        vgg_features = self.vgg(x)
        vgg_features = self.adaptive_pool(vgg_features)
        vgg_features = vgg_features.view(vgg_features.size(0), -1)
        
        # Concatenate features
        combined = torch.cat([resnet_features, vgg_features], dim=1)
        
        # Classify
        output = self.classifier(combined)
        return output

# Usage example
if __name__ == "__main__":
    # Create transfer learning model
    num_classes = 10
    model = create_transfer_model(num_classes, model_name='resnet18')
    
    # Print model architecture
    print(model)
    
    # Count trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    
    print(f"Trainable parameters: {trainable_params}")
    print(f"Total parameters: {total_params}")
    print(f"Percentage trainable: {100 * trainable_params / total_params:.2f}%")
```

### 8. How do you implement custom loss functions and metrics in PyTorch?
**Answer:** PyTorch allows creation of custom loss functions and metrics for specialized requirements.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# Custom Loss Functions
class FocalLoss(nn.Module):
    """Focal Loss for addressing class imbalance"""
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class DiceLoss(nn.Module):
    """Dice Loss for segmentation tasks"""
    def __init__(self, smooth=1e-6):
        super(DiceLoss, self).__init__()
        self.smooth = smooth
    
    def forward(self, inputs, targets):
        # Flatten tensors
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        
        # Calculate intersection and union
        intersection = (inputs * targets).sum()
        dice_score = (2. * intersection + self.smooth) / (inputs.sum() + targets.sum() + self.smooth)
        
        return 1 - dice_score

class ContrastiveLoss(nn.Module):
    """Contrastive Loss for siamese networks"""
    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
    
    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim=True)
        
        loss_contrastive = torch.mean(
            (1 - label) * torch.pow(euclidean_distance, 2) +
            label * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2)
        )
        
        return loss_contrastive

class TripletLoss(nn.Module):
    """Triplet Loss for metric learning"""
    def __init__(self, margin=1.0):
        super(TripletLoss, self).__init__()
        self.margin = margin
    
    def forward(self, anchor, positive, negative):
        distance_positive = F.pairwise_distance(anchor, positive, 2)
        distance_negative = F.pairwise_distance(anchor, negative, 2)
        
        losses = torch.relu(distance_positive - distance_negative + self.margin)
        return losses.mean()

# Custom Metrics
class Accuracy:
    """Accuracy metric"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.correct = 0
        self.total = 0
    
    def update(self, outputs, targets):
        _, predicted = torch.max(outputs.data, 1)
        self.total += targets.size(0)
        self.correct += (predicted == targets).sum().item()
    
    def compute(self):
        return 100 * self.correct / self.total if self.total > 0 else 0

class F1Score:
    """F1 Score metric"""
    def __init__(self, num_classes, average='macro'):
        self.num_classes = num_classes
        self.average = average
        self.reset()
    
    def reset(self):
        self.tp = torch.zeros(self.num_classes)
        self.fp = torch.zeros(self.num_classes)
        self.fn = torch.zeros(self.num_classes)
    
    def update(self, outputs, targets):
        _, predicted = torch.max(outputs, 1)
        
        for c in range(self.num_classes):
            tp = ((predicted == c) & (targets == c)).sum().item()
            fp = ((predicted == c) & (targets != c)).sum().item()
            fn = ((predicted != c) & (targets == c)).sum().item()
            
            self.tp[c] += tp
            self.fp[c] += fp
            self.fn[c] += fn
    
    def compute(self):
        precision = self.tp / (self.tp + self.fp + 1e-8)
        recall = self.tp / (self.tp + self.fn + 1e-8)
        f1 = 2 * (precision * recall) / (precision + recall + 1e-8)
        
        if self.average == 'macro':
            return f1.mean().item()
        elif self.average == 'weighted':
            weights = self.tp + self.fn
            return (f1 * weights).sum() / weights.sum()
        else:
            return f1

class IoU:
    """Intersection over Union for segmentation"""
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.reset()
    
    def reset(self):
        self.intersection = torch.zeros(self.num_classes)
        self.union = torch.zeros(self.num_classes)
    
    def update(self, outputs, targets):
        _, predicted = torch.max(outputs, 1)
        
        for c in range(self.num_classes):
            pred_c = (predicted == c)
            target_c = (targets == c)
            
            intersection = (pred_c & target_c).sum().item()
            union = (pred_c | target_c).sum().item()
            
            self.intersection[c] += intersection
            self.union[c] += union
    
    def compute(self):
        iou = self.intersection / (self.union + 1e-8)
        return iou.mean().item()

# Metric Manager
class MetricManager:
    """Manage multiple metrics during training"""
    def __init__(self):
        self.metrics = {}
    
    def add_metric(self, name, metric):
        self.metrics[name] = metric
    
    def reset_all(self):
        for metric in self.metrics.values():
            metric.reset()
    
    def update_all(self, outputs, targets):
        for metric in self.metrics.values():
            metric.update(outputs, targets)
    
    def compute_all(self):
        results = {}
        for name, metric in self.metrics.items():
            results[name] = metric.compute()
        return results

# Advanced Loss Combinations
class CombinedLoss(nn.Module):
    """Combine multiple loss functions"""
    def __init__(self, losses, weights):
        super(CombinedLoss, self).__init__()
        self.losses = nn.ModuleList(losses)
        self.weights = weights
    
    def forward(self, outputs, targets):
        total_loss = 0
        individual_losses = {}
        
        for i, (loss_fn, weight) in enumerate(zip(self.losses, self.weights)):
            loss_value = loss_fn(outputs, targets)
            total_loss += weight * loss_value
            individual_losses[f'loss_{i}'] = loss_value.item()
        
        return total_loss, individual_losses

# Usage Example
def training_with_custom_metrics():
    """Example training loop with custom metrics"""
    
    # Initialize model, loss, and metrics
    model = nn.Sequential(
        nn.Linear(784, 128),
        nn.ReLU(),
        nn.Linear(128, 10)
    )
    
    # Custom loss
    criterion = FocalLoss(alpha=1, gamma=2)
    
    # Initialize metrics
    metric_manager = MetricManager()
    metric_manager.add_metric('accuracy', Accuracy())
    metric_manager.add_metric('f1', F1Score(num_classes=10))
    
    optimizer = torch.optim.Adam(model.parameters())
    
    # Training loop
    for epoch in range(10):
        model.train()
        metric_manager.reset_all()
        
        # Simulate training batches
        for batch in range(100):  # Simulate 100 batches
            # Generate dummy data
            inputs = torch.randn(32, 784)
            targets = torch.randint(0, 10, (32,))
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            # Update metrics
            metric_manager.update_all(outputs, targets)
        
        # Compute and print metrics
        metrics = metric_manager.compute_all()
        print(f"Epoch {epoch+1}:")
        for name, value in metrics.items():
            print(f"  {name}: {value:.4f}")

if __name__ == "__main__":
    # Test custom losses
    inputs = torch.randn(10, 5)
    targets = torch.randint(0, 5, (10,))
    
    focal_loss = FocalLoss()
    loss_value = focal_loss(inputs, targets)
    print(f"Focal Loss: {loss_value.item():.4f}")
    
    # Test metrics
    accuracy = Accuracy()
    accuracy.update(inputs, targets)
    print(f"Accuracy: {accuracy.compute():.2f}%")
```

This comprehensive PyTorch interview questions set covers fundamental concepts through advanced implementations, providing practical examples for neural networks, custom components, and production-ready training pipelines.