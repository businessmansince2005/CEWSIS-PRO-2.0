import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from pathlib import Path
import json
from typing import Tuple, Dict, List
import matplotlib.pyplot as plt

class ModulationDataset(torch.utils.data.Dataset):
    """Custom dataset for modulation classification."""
    def __init__(self, spectrograms, labels):
        self.spectrograms = torch.FloatTensor(spectrograms)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.spectrograms[idx], self.labels[idx]

def prepare_data_loaders(train_specs, train_labels, val_specs, val_labels, batch_size=32):
    """
    Create DataLoaders for training and validation.
    """
    train_dataset = ModulationDataset(train_specs, train_labels)
    val_dataset = ModulationDataset(val_specs, val_labels)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    return train_loader, val_loader

def train_epoch(model, train_loader, optimizer, criterion, device='cpu'):
    """Train for one epoch."""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    
    for specs, labels in train_loader:
        specs, labels = specs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(specs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = total_loss / len(train_loader)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def eval_epoch(model, val_loader, criterion, device='cpu'):
    """Evaluate for one epoch."""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for specs, labels in val_loader:
            specs, labels = specs.to(device), labels.to(device)
            outputs = model(specs)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    epoch_loss = total_loss / len(val_loader)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def train_model(model, train_loader, val_loader, num_epochs=50, lr=1e-3, device='cpu', checkpoint_dir='./checkpoints'):
    """
    Full training pipeline with checkpoint saving.
    """
    Path(checkpoint_dir).mkdir(exist_ok=True)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=5, verbose=True)
    
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    best_val_acc = 0.0
    patience_counter = 0
    patience_limit = 10
    
    for epoch in range(num_epochs):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = eval_epoch(model, val_loader, criterion, device)
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        print(f"Epoch {epoch+1}/{num_epochs} | Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            checkpoint_path = Path(checkpoint_dir) / f'best_model_acc_{val_acc:.4f}.pth'
            torch.save(model.state_dict(), checkpoint_path)
            print(f"  -> Saved best model: {checkpoint_path}")
        else:
            patience_counter += 1
        
        scheduler.step(val_acc)
        
        # Early stopping
        if patience_counter >= patience_limit:
            print(f"Early stopping at epoch {epoch+1}")
            break
    
    # Save final model
    final_path = Path(checkpoint_dir) / 'final_model.pth'
    torch.save(model.state_dict(), final_path)
    print(f"Saved final model: {final_path}")
    
    return history

def plot_training_history(history: Dict, save_path: str = None):
    """Plot training and validation metrics."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss
    axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
    axes[0].plot(history['val_loss'], label='Val Loss', marker='s')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training & Validation Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy
    axes[1].plot(history['train_acc'], label='Train Acc', marker='o')
    axes[1].plot(history['val_acc'], label='Val Acc', marker='s')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Training & Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"Saved plot: {save_path}")
    plt.show()

def save_training_config(config: Dict, path: str):
    """Save training configuration as JSON."""
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Saved config: {path}")
