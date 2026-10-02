"""
Evaluation metrics for classification and anomaly detection.

This module provides comprehensive metrics for evaluating model performance,
including classification metrics, confusion matrices, and per-class statistics.

Author: Cognitive EW System Team
Date: 2024
"""
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    precision_recall_curve, roc_curve
)
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt


def compute_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, 
                                   average: str = 'macro') -> Dict[str, float]:
    """
    Compute comprehensive classification metrics.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Averaging strategy ('macro', 'micro', 'weighted')
    
    Returns:
        Dictionary with accuracy, precision, recall, and F1-score
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
        "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
        "f1": f1_score(y_true, y_pred, average=average, zero_division=0)
    }


def compute_per_class_metrics(y_true: np.ndarray, y_pred: np.ndarray, 
                              class_names: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
    """
    Compute per-class classification metrics.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        class_names: Optional list of class names for labeling
    
    Returns:
        Dictionary mapping class names/indices to their metrics
    """
    unique_classes = np.unique(np.concatenate([y_true, y_pred]))
    per_class_metrics = {}
    
    for cls in unique_classes:
        # Binary classification for this class
        y_true_binary = (y_true == cls).astype(int)
        y_pred_binary = (y_pred == cls).astype(int)
        
        precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
        recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
        f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
        
        # Support (number of true instances)
        support = np.sum(y_true == cls)
        
        class_name = class_names[cls] if class_names and cls < len(class_names) else f"Class_{cls}"
        per_class_metrics[class_name] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": int(support)
        }
    
    return per_class_metrics


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray,
                          class_names: Optional[List[str]] = None,
                          save_path: Optional[str] = None,
                          normalize: bool = True) -> np.ndarray:
    """
    Plot and optionally save confusion matrix.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        class_names: Optional list of class names
        save_path: Optional path to save the plot
        normalize: Whether to normalize the confusion matrix
    
    Returns:
        Confusion matrix as numpy array
    """
    cm = confusion_matrix(y_true, y_pred)
    
    if normalize:
        cm = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-8)
        fmt = '.2f'
        title = 'Normalized Confusion Matrix'
    else:
        fmt = 'd'
        title = 'Confusion Matrix'
    
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    # Set labels
    if class_names:
        tick_marks = np.arange(len(class_names))
        ax.set_xticks(tick_marks)
        ax.set_yticks(tick_marks)
        ax.set_xticklabels(class_names, rotation=45, ha='right')
        ax.set_yticklabels(class_names)
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")
    
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')
    ax.set_title(title)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print(f"Saved confusion matrix to {save_path}")
    
    plt.show()
    return cm


def print_classification_report(y_true: np.ndarray, y_pred: np.ndarray,
                                class_names: Optional[List[str]] = None) -> str:
    """
    Print detailed classification report.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        class_names: Optional list of class names
    
    Returns:
        Classification report as string
    """
    report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    print(report)
    return report


def compute_anomaly_detection_metrics(y_true: np.ndarray, anomaly_scores: np.ndarray,
                                     threshold: Optional[float] = None) -> Dict[str, float]:
    """
    Compute metrics for anomaly detection.
    
    Args:
        y_true: Binary labels (0=normal, 1=anomaly)
        anomaly_scores: Anomaly scores (higher = more anomalous)
        threshold: Optional threshold for binary classification.
                  If None, uses optimal threshold based on F1-score.
    
    Returns:
        Dictionary with precision, recall, F1, and optimal threshold
    """
    if threshold is None:
        # Find optimal threshold using precision-recall curve
        precision, recall, thresholds = precision_recall_curve(y_true, anomaly_scores)
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
        optimal_idx = np.argmax(f1_scores)
        threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else np.median(anomaly_scores)
    
    y_pred = (anomaly_scores >= threshold).astype(int)
    
    metrics = compute_classification_metrics(y_true, y_pred)
    metrics['threshold'] = threshold
    
    # Compute AUC-ROC if possible
    try:
        metrics['roc_auc'] = roc_auc_score(y_true, anomaly_scores)
    except ValueError:
        metrics['roc_auc'] = 0.0
    
    return metrics

