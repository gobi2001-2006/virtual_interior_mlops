from typing import Dict, Any, List
import numpy as np
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from backend.app.core.config import settings

def evaluate_model_on_loader(
    model: torch.nn.Module,
    data_loader: torch.utils.data.DataLoader,
    class_names: List[str] = settings.ROOM_CLASSES,
    device: str = "cpu"
) -> Dict[str, Any]:
    """
    Evaluates a PyTorch model on a DataLoader and computes comprehensive metrics.
    """
    model.eval()
    model.to(device)
    
    all_preds = []
    all_targets = []
    
    with torch.no_grad():
        for images, targets in data_loader:
            images = images.to(device)
            outputs = model(images)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(targets.numpy())
            
    if not all_targets:
        return {
            "accuracy": 0.0,
            "macro_f1": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "sample_count": 0,
            "per_class_metrics": {},
            "confusion_matrix": []
        }
        
    y_true = np.array(all_targets)
    y_pred = np.array(all_preds)
    
    accuracy = float(accuracy_score(y_true, y_pred))
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    
    # Per-class metrics
    p_class, r_class, f1_class, support_class = precision_recall_fscore_support(
        y_true, y_pred, labels=list(range(len(class_names))), zero_division=0
    )
    
    per_class = {}
    for idx, name in enumerate(class_names):
        per_class[name] = {
            "precision": round(float(p_class[idx]), 4),
            "recall": round(float(r_class[idx]), 4),
            "f1_score": round(float(f1_class[idx]), 4),
            "support": int(support_class[idx])
        }
        
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(class_names))))
    
    return {
        "accuracy": round(accuracy, 4),
        "macro_f1": round(float(f1), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "sample_count": len(y_true),
        "per_class_metrics": per_class,
        "confusion_matrix": cm.tolist()
    }
