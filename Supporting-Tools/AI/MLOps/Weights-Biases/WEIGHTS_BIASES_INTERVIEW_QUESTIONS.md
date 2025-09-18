# Weights & Biases (wandb) Interview Questions

## Basic Concepts

### 1. What is Weights & Biases and its key features?
**Answer:** Weights & Biases (wandb) is an MLOps platform for experiment tracking, model management, and collaboration. Key features:

- **Experiment Tracking**: Log metrics, hyperparameters, and artifacts
- **Visualizations**: Interactive charts and dashboards
- **Hyperparameter Optimization**: Automated hyperparameter sweeps
- **Model Registry**: Centralized model versioning
- **Collaboration**: Team sharing and reporting
- **Artifacts**: Dataset and model versioning

```python
import wandb
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize wandb
wandb.init(
    project="my-ml-project",
    name="experiment-1",
    config={
        "learning_rate": 0.01,
        "epochs": 100,
        "batch_size": 32,
        "architecture": "RandomForest"
    }
)

# Access config
config = wandb.config
print(f"Learning rate: {config.learning_rate}")

# Log metrics during training
for epoch in range(config.epochs):
    # Simulate training
    loss = np.random.exponential(0.1) * np.exp(-epoch/50)
    accuracy = 1 - np.exp(-epoch/50) + np.random.normal(0, 0.01)
    
    wandb.log({
        "epoch": epoch,
        "loss": loss,
        "accuracy": accuracy,
        "learning_rate": config.learning_rate
    })

# Finish run
wandb.finish()
```

### 2. How do you track experiments and log metrics with wandb?
**Answer:** Wandb provides comprehensive experiment tracking with automatic and manual logging.

```python
import wandb
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Advanced experiment setup
def setup_wandb_experiment():
    # Initialize with detailed configuration
    wandb.init(
        project="deep-learning-experiments",
        name="cnn-classifier-v1",
        tags=["cnn", "classification", "pytorch"],
        notes="Experimenting with CNN architecture for image classification",
        config={
            "model_architecture": "CNN",
            "learning_rate": 0.001,
            "batch_size": 64,
            "epochs": 50,
            "optimizer": "Adam",
            "loss_function": "CrossEntropyLoss",
            "dataset": "CIFAR-10",
            "data_augmentation": True,
            "dropout_rate": 0.5
        }
    )
    
    return wandb.config

# Log different types of metrics
def comprehensive_logging():
    config = setup_wandb_experiment()
    
    # Log scalar metrics
    wandb.log({
        "train_loss": 0.5,
        "val_loss": 0.6,
        "train_accuracy": 0.85,
        "val_accuracy": 0.82,
        "learning_rate": config.learning_rate
    })
    
    # Log histograms
    weights = torch.randn(1000)
    wandb.log({"weight_distribution": wandb.Histogram(weights.numpy())})
    
    # Log images
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    wandb.log({"training_curve": wandb.Image(fig)})
    plt.close()
    
    # Log custom charts
    data = [[x, np.sin(x)] for x in np.linspace(0, 10, 100)]
    table = wandb.Table(data=data, columns=["x", "sin(x)"])
    wandb.log({"sine_wave": wandb.plot.line(table, "x", "sin(x)", title="Sine Wave")})
    
    # Log system metrics
    wandb.log({
        "gpu_memory_usage": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
        "cpu_usage": 75.5,
        "memory_usage": 8.2
    })

# PyTorch integration
def train_with_wandb_pytorch():
    # Model definition
    class SimpleCNN(nn.Module):
        def __init__(self, num_classes=10):
            super(SimpleCNN, self).__init__()
            self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
            self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
            self.pool = nn.MaxPool2d(2, 2)
            self.fc1 = nn.Linear(64 * 8 * 8, 512)
            self.fc2 = nn.Linear(512, num_classes)
            self.dropout = nn.Dropout(0.5)
        
        def forward(self, x):
            x = self.pool(torch.relu(self.conv1(x)))
            x = self.pool(torch.relu(self.conv2(x)))
            x = x.view(-1, 64 * 8 * 8)
            x = torch.relu(self.fc1(x))
            x = self.dropout(x)
            x = self.fc2(x)
            return x
    
    # Initialize wandb
    config = setup_wandb_experiment()
    
    # Create model
    model = SimpleCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)
    
    # Watch model (logs gradients and parameters)
    wandb.watch(model, criterion, log="all", log_freq=10)
    
    # Training loop
    for epoch in range(config.epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        # Simulate training batches
        for batch_idx in range(100):  # Simulate 100 batches
            # Simulate batch data
            inputs = torch.randn(config.batch_size, 3, 32, 32)
            labels = torch.randint(0, 10, (config.batch_size,))
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Log batch metrics
            if batch_idx % 10 == 0:
                wandb.log({
                    "batch_loss": loss.item(),
                    "batch_accuracy": 100. * correct / total,
                    "epoch": epoch,
                    "batch": batch_idx
                })
        
        # Log epoch metrics
        epoch_loss = running_loss / 100
        epoch_accuracy = 100. * correct / total
        
        wandb.log({
            "epoch": epoch,
            "train_loss": epoch_loss,
            "train_accuracy": epoch_accuracy,
            "learning_rate": optimizer.param_groups[0]['lr']
        })
        
        print(f"Epoch {epoch}: Loss={epoch_loss:.4f}, Accuracy={epoch_accuracy:.2f}%")
    
    return model

# TensorFlow/Keras integration
def train_with_wandb_tensorflow():
    import tensorflow as tf
    from wandb.keras import WandbCallback
    
    # Initialize wandb
    wandb.init(
        project="tensorflow-experiments",
        config={
            "learning_rate": 0.001,
            "epochs": 20,
            "batch_size": 32,
            "architecture": "Sequential"
        }
    )
    
    # Create model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=wandb.config.learning_rate),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Generate dummy data
    x_train = np.random.random((1000, 784))
    y_train = np.random.randint(0, 10, (1000,))
    x_val = np.random.random((200, 784))
    y_val = np.random.randint(0, 10, (200,))
    
    # Train with wandb callback
    model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=wandb.config.epochs,
        batch_size=wandb.config.batch_size,
        callbacks=[WandbCallback()]
    )
    
    return model
```

### 3. How do you perform hyperparameter optimization with wandb sweeps?
**Answer:** Wandb sweeps automate hyperparameter optimization with various search strategies.

```python
import wandb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Define sweep configuration
sweep_config = {
    'method': 'bayes',  # 'grid', 'random', 'bayes'
    'metric': {
        'name': 'val_accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform_values',
            'min': 0.0001,
            'max': 0.1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'epochs': {
            'distribution': 'int_uniform',
            'min': 10,
            'max': 100
        },
        'optimizer': {
            'values': ['adam', 'sgd', 'rmsprop']
        },
        'dropout_rate': {
            'distribution': 'uniform',
            'min': 0.1,
            'max': 0.5
        },
        'hidden_layers': {
            'values': [1, 2, 3, 4]
        },
        'hidden_units': {
            'distribution': 'q_uniform',
            'min': 32,
            'max': 512,
            'q': 32
        }
    }
}

# Training function for sweep
def train_model():
    # Initialize wandb run
    wandb.init()
    
    # Get hyperparameters from sweep
    config = wandb.config
    
    # Create model with sweep parameters
    model = create_model_with_config(config)
    
    # Train model
    train_loss, val_loss, val_accuracy = train_model_with_config(model, config)
    
    # Log metrics
    wandb.log({
        'train_loss': train_loss,
        'val_loss': val_loss,
        'val_accuracy': val_accuracy,
        'final_score': val_accuracy
    })

def create_model_with_config(config):
    """Create model based on sweep configuration"""
    import torch.nn as nn
    
    layers = []
    input_size = 784  # Example input size
    
    # Add hidden layers
    for i in range(config.hidden_layers):
        layers.append(nn.Linear(input_size, config.hidden_units))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(config.dropout_rate))
        input_size = config.hidden_units
    
    # Output layer
    layers.append(nn.Linear(input_size, 10))  # 10 classes
    
    model = nn.Sequential(*layers)
    return model

def train_model_with_config(model, config):
    """Train model with given configuration"""
    import torch
    import torch.optim as optim
    import torch.nn as nn
    
    # Create optimizer based on config
    if config.optimizer == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)
    elif config.optimizer == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=config.learning_rate)
    elif config.optimizer == 'rmsprop':
        optimizer = optim.RMSprop(model.parameters(), lr=config.learning_rate)
    
    criterion = nn.CrossEntropyLoss()
    
    # Simulate training
    train_losses = []
    val_losses = []
    val_accuracies = []
    
    for epoch in range(config.epochs):
        # Simulate training step
        train_loss = np.random.exponential(0.1) * np.exp(-epoch/20)
        val_loss = train_loss + np.random.normal(0, 0.05)
        val_accuracy = min(0.95, 1 - np.exp(-epoch/15) + np.random.normal(0, 0.02))
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        
        # Log intermediate metrics
        wandb.log({
            'epoch': epoch,
            'train_loss': train_loss,
            'val_loss': val_loss,
            'val_accuracy': val_accuracy
        })
    
    return np.mean(train_losses), np.mean(val_losses), max(val_accuracies)

# Initialize and run sweep
def run_hyperparameter_sweep():
    # Create sweep
    sweep_id = wandb.sweep(sweep_config, project="hyperparameter-optimization")
    
    # Run sweep
    wandb.agent(sweep_id, train_model, count=50)  # Run 50 experiments
    
    return sweep_id

# Advanced sweep with early termination
def advanced_sweep_config():
    advanced_config = {
        'method': 'bayes',
        'metric': {
            'name': 'val_accuracy',
            'goal': 'maximize'
        },
        'parameters': {
            'learning_rate': {
                'distribution': 'log_uniform_values',
                'min': 0.0001,
                'max': 0.1
            },
            'batch_size': {
                'values': [16, 32, 64, 128]
            },
            'architecture': {
                'values': ['resnet', 'densenet', 'efficientnet']
            }
        },
        'early_terminate': {
            'type': 'hyperband',
            'min_iter': 5,
            'eta': 2,
            's': 3
        }
    }
    
    return advanced_config

# Multi-objective optimization
def multi_objective_sweep():
    multi_obj_config = {
        'method': 'bayes',
        'metric': {
            'name': 'combined_score',
            'goal': 'maximize'
        },
        'parameters': {
            'learning_rate': {
                'distribution': 'log_uniform_values',
                'min': 0.0001,
                'max': 0.1
            },
            'model_size': {
                'values': ['small', 'medium', 'large']
            }
        }
    }
    
    def multi_objective_train():
        wandb.init()
        config = wandb.config
        
        # Simulate training
        accuracy = np.random.uniform(0.8, 0.95)
        inference_time = np.random.uniform(10, 100)  # milliseconds
        model_size = {'small': 1, 'medium': 5, 'large': 20}[config.model_size]  # MB
        
        # Multi-objective score (accuracy vs efficiency)
        efficiency_score = 1 / (inference_time * model_size / 1000)
        combined_score = 0.7 * accuracy + 0.3 * efficiency_score
        
        wandb.log({
            'accuracy': accuracy,
            'inference_time': inference_time,
            'model_size': model_size,
            'efficiency_score': efficiency_score,
            'combined_score': combined_score
        })
    
    sweep_id = wandb.sweep(multi_obj_config, project="multi-objective-optimization")
    wandb.agent(sweep_id, multi_objective_train, count=30)
    
    return sweep_id
```

### 4. How do you manage artifacts and model versioning with wandb?
**Answer:** Wandb Artifacts provide versioned storage for datasets, models, and other files.

```python
import wandb
import joblib
import pandas as pd
import torch

# Dataset artifact management
def create_dataset_artifact():
    # Initialize run
    wandb.init(project="artifact-management", job_type="data-preparation")
    
    # Create dataset
    data = pd.DataFrame({
        'feature1': np.random.randn(1000),
        'feature2': np.random.randn(1000),
        'target': np.random.randint(0, 2, 1000)
    })
    
    # Save dataset
    data.to_csv('processed_dataset.csv', index=False)
    
    # Create artifact
    dataset_artifact = wandb.Artifact(
        name="processed_dataset",
        type="dataset",
        description="Processed training dataset with feature engineering",
        metadata={
            "source": "raw_data_v1.csv",
            "preprocessing_steps": ["normalization", "feature_selection"],
            "rows": len(data),
            "columns": len(data.columns),
            "target_distribution": data['target'].value_counts().to_dict()
        }
    )
    
    # Add file to artifact
    dataset_artifact.add_file('processed_dataset.csv')
    
    # Log artifact
    wandb.log_artifact(dataset_artifact)
    
    wandb.finish()
    
    return dataset_artifact

# Model artifact management
def create_model_artifact(model, model_name="trained_model"):
    # Initialize run
    wandb.init(project="model-registry", job_type="training")
    
    # Save model
    if isinstance(model, torch.nn.Module):
        torch.save(model.state_dict(), f'{model_name}.pth')
        model_file = f'{model_name}.pth'
    else:
        joblib.dump(model, f'{model_name}.pkl')
        model_file = f'{model_name}.pkl'
    
    # Create model artifact
    model_artifact = wandb.Artifact(
        name=model_name,
        type="model",
        description="Trained classification model",
        metadata={
            "framework": "pytorch" if isinstance(model, torch.nn.Module) else "sklearn",
            "model_type": type(model).__name__,
            "training_accuracy": 0.95,
            "validation_accuracy": 0.92,
            "hyperparameters": {
                "learning_rate": 0.001,
                "epochs": 50,
                "batch_size": 32
            }
        }
    )
    
    # Add model file
    model_artifact.add_file(model_file)
    
    # Add additional files
    model_artifact.add_file('model_config.json')  # Model configuration
    model_artifact.add_file('training_log.txt')   # Training logs
    
    # Log artifact
    wandb.log_artifact(model_artifact)
    
    wandb.finish()
    
    return model_artifact

# Use artifacts in training
def train_with_artifacts():
    # Initialize run
    run = wandb.init(project="training-with-artifacts", job_type="training")
    
    # Download dataset artifact
    dataset_artifact = run.use_artifact('processed_dataset:latest')
    dataset_dir = dataset_artifact.download()
    
    # Load dataset
    data = pd.read_csv(f'{dataset_dir}/processed_dataset.csv')
    
    # Train model (simplified)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    wandb.log({'accuracy': accuracy})
    
    # Create and log model artifact
    create_model_artifact(model, "random_forest_v1")
    
    wandb.finish()
    
    return model

# Model versioning and lineage
def model_versioning_workflow():
    """Complete model versioning workflow"""
    
    # Version 1: Initial model
    wandb.init(project="model-versioning", job_type="training", name="model_v1")
    
    # Simulate training
    model_v1_accuracy = 0.85
    wandb.log({'accuracy': model_v1_accuracy})
    
    # Create model artifact v1
    model_v1 = wandb.Artifact(
        name="classifier_model",
        type="model",
        description="Initial model version",
        metadata={"version": "1.0", "accuracy": model_v1_accuracy}
    )
    model_v1.add_file('model_v1.pkl')
    wandb.log_artifact(model_v1)
    wandb.finish()
    
    # Version 2: Improved model
    wandb.init(project="model-versioning", job_type="training", name="model_v2")
    
    # Use previous model as baseline
    baseline_artifact = wandb.use_artifact('classifier_model:v0')
    
    # Simulate improved training
    model_v2_accuracy = 0.92
    wandb.log({'accuracy': model_v2_accuracy, 'improvement': model_v2_accuracy - model_v1_accuracy})
    
    # Create model artifact v2
    model_v2 = wandb.Artifact(
        name="classifier_model",
        type="model",
        description="Improved model with better accuracy",
        metadata={"version": "2.0", "accuracy": model_v2_accuracy, "baseline_version": "1.0"}
    )
    model_v2.add_file('model_v2.pkl')
    wandb.log_artifact(model_v2)
    wandb.finish()

# Artifact lineage and dependencies
def create_artifact_lineage():
    """Create artifacts with clear lineage"""
    
    # Raw data artifact
    wandb.init(project="data-lineage", job_type="data-collection")
    raw_data_artifact = wandb.Artifact("raw_data", type="dataset")
    raw_data_artifact.add_file('raw_data.csv')
    wandb.log_artifact(raw_data_artifact)
    wandb.finish()
    
    # Processed data artifact (depends on raw data)
    wandb.init(project="data-lineage", job_type="data-preprocessing")
    raw_data = wandb.use_artifact('raw_data:latest')
    
    processed_data_artifact = wandb.Artifact(
        "processed_data", 
        type="dataset",
        description="Cleaned and preprocessed data"
    )
    processed_data_artifact.add_file('processed_data.csv')
    wandb.log_artifact(processed_data_artifact)
    wandb.finish()
    
    # Model artifact (depends on processed data)
    wandb.init(project="data-lineage", job_type="model-training")
    processed_data = wandb.use_artifact('processed_data:latest')
    
    model_artifact = wandb.Artifact(
        "trained_model",
        type="model",
        description="Model trained on processed data"
    )
    model_artifact.add_file('model.pkl')
    wandb.log_artifact(model_artifact)
    wandb.finish()

# Artifact comparison and analysis
def compare_model_artifacts():
    """Compare different model versions"""
    
    wandb.init(project="model-comparison", job_type="analysis")
    
    # Load multiple model versions
    model_v1 = wandb.use_artifact('classifier_model:v0')
    model_v2 = wandb.use_artifact('classifier_model:v1')
    
    # Compare metadata
    v1_metadata = model_v1.metadata
    v2_metadata = model_v2.metadata
    
    comparison_results = {
        'v1_accuracy': v1_metadata.get('accuracy', 0),
        'v2_accuracy': v2_metadata.get('accuracy', 0),
        'improvement': v2_metadata.get('accuracy', 0) - v1_metadata.get('accuracy', 0),
        'v1_size': model_v1.size,
        'v2_size': model_v2.size
    }
    
    # Log comparison
    wandb.log(comparison_results)
    
    # Create comparison table
    comparison_table = wandb.Table(
        columns=["Version", "Accuracy", "Size (MB)", "Description"],
        data=[
            ["v1", v1_metadata.get('accuracy'), model_v1.size/1024/1024, model_v1.description],
            ["v2", v2_metadata.get('accuracy'), model_v2.size/1024/1024, model_v2.description]
        ]
    )
    
    wandb.log({"model_comparison": comparison_table})
    
    wandb.finish()
    
    return comparison_results
```

This comprehensive Weights & Biases interview questions set covers fundamental concepts through advanced artifact management and model versioning, providing practical examples for experiment tracking, hyperparameter optimization, and MLOps workflows.