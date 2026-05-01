"""
Generates training visualization graphs and logs them to MLflow.
These are the graphs ML engineers post on LinkedIn and GitHub.
"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import mlflow
import os

def plot_confusion_matrix(y_true, y_pred, labels, run_id):
    """The most important ML graph — shows where the model is confused."""
    fig, ax = plt.subplots(figsize=(10, 8))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, cmap='Blues', colorbar=True)
    ax.set_title('CIPHER Classifier — Confusion Matrix', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=11)
    ax.set_ylabel('True Label', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    path = '/tmp/confusion_matrix.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    mlflow.log_artifact(path, "plots")
    print(f"Confusion matrix saved")
    return path

def plot_category_distribution(df):
    """Shows training data balance — important for understanding bias."""
    fig, ax = plt.subplots(figsize=(10, 5))
    counts = df['label'].value_counts()
    colors = ['#6366f1','#06b6d4','#10b981','#f59e0b','#ef4444','#8b5cf6','#64748b']
    bars = ax.bar(counts.index, counts.values, color=colors[:len(counts)])
    ax.set_title('CIPHER Training Data — Category Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Failure Category', fontsize=11)
    ax.set_ylabel('Number of Examples', fontsize=11)
    plt.xticks(rotation=30, ha='right')
    for bar, count in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    path = '/tmp/category_distribution.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    mlflow.log_artifact(path, "plots")
    print(f"Category distribution saved")
    return path

def plot_f1_history(current_f1, previous_f1, version):
    """Shows model improvement over time."""
    fig, ax = plt.subplots(figsize=(8, 5))
    versions = list(range(1, version + 1))
    # Simulate history (in production this comes from MLflow run history)
    f1_scores = [previous_f1] * (version - 1) + [current_f1]
    if len(f1_scores) == 0:
        f1_scores = [current_f1]
    if len(f1_scores) == 1:
        versions = [1]

    ax.plot(versions, f1_scores, 'o-', color='#6366f1',
            linewidth=2.5, markersize=8, markerfacecolor='white',
            markeredgewidth=2.5)
    ax.fill_between(versions, f1_scores, alpha=0.1, color='#6366f1')
    ax.axhline(y=0.9, color='#10b981', linestyle='--',
               linewidth=1.5, alpha=0.7, label='Target F1 = 0.90')
    ax.set_title('CIPHER Model — F1 Score Over Versions', fontsize=14, fontweight='bold')
    ax.set_xlabel('Model Version', fontsize=11)
    ax.set_ylabel('Weighted F1 Score', fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(versions)
    ax.legend()
    ax.grid(True, alpha=0.3)
    for v, f in zip(versions, f1_scores):
        ax.annotate(f'{f:.3f}', (v, f),
                    textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    path = '/tmp/f1_history.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    mlflow.log_artifact(path, "plots")
    print(f"F1 history chart saved")
    return path

def plot_per_class_f1(report_dict, labels):
    """Shows which failure categories the model handles best."""
    fig, ax = plt.subplots(figsize=(10, 5))
    f1_scores = []
    valid_labels = []
    for label in labels:
        if label in report_dict:
            f1_scores.append(report_dict[label].get('f1-score', 0))
            valid_labels.append(label)

    colors = ['#10b981' if f >= 0.7 else '#f59e0b' if f >= 0.4 else '#ef4444'
              for f in f1_scores]
    bars = ax.barh(valid_labels, f1_scores, color=colors, height=0.6)
    ax.axvline(x=0.7, color='#10b981', linestyle='--',
               linewidth=1.5, alpha=0.7, label='Good threshold (0.7)')
    ax.set_title('CIPHER — F1 Score Per Failure Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('F1 Score', fontsize=11)
    ax.set_xlim(0, 1.1)
    ax.legend()
    for bar, score in zip(bars, f1_scores):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{score:.3f}', va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    path = '/tmp/per_class_f1.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    mlflow.log_artifact(path, "plots")
    print(f"Per-class F1 chart saved")
    return path
