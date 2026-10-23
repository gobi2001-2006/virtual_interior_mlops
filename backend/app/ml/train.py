import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List, Tuple
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.ml.model import build_model
from backend.app.ml.dataset import create_data_loaders
from backend.app.ml.evaluate import evaluate_model_on_loader

def train_classifier(
    data_dir: str,
    output_dir: str = settings.MODEL_ARTIFACT_DIR,
    version_tag: str = "v001",
    extra_samples: Optional[List[Tuple[str, int]]] = None,
    epochs: int = 5,
    batch_size: int = 16,
    lr: float = 0.001,
    progress_callback: Optional[Callable[[int, int, float, float], None]] = None
) -> Dict[str, Any]:
    """
    Executes training loop for MobileNetV3-Small on data in data_dir + extra feedback samples.
    Saves best model weights, metadata, class mappings, and training history.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Starting model training for version {version_tag} on {device}")
    
    train_loader, val_loader, test_loader, counts, is_synthetic_demo = create_data_loaders(
        data_dir=data_dir,
        class_names=settings.ROOM_CLASSES,
        extra_samples=extra_samples,
        batch_size=batch_size
    )
    
    total_samples = sum(counts.values())
    if total_samples == 0:
        raise ValueError(
            f"No training data found in {data_dir}. Please place images in class subdirectories: "
            f"{', '.join(settings.ROOM_CLASSES)}"
        )
        
    os.makedirs(output_dir, exist_ok=True)
    
    num_classes = len(settings.ROOM_CLASSES)
    model = build_model(num_classes=num_classes, pretrained=True)
    model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_val_f1 = -1.0
    best_weights_path = os.path.join(output_dir, f"model_{version_tag}.pth")
    history = []
    
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, targets in train_loader:
            images, targets = images.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            correct += (preds == targets).sum().item()
            total += targets.size(0)
            
        scheduler.step()
        
        train_loss = running_loss / max(1, total)
        train_acc = correct / max(1, total)
        
        # Validation
        val_metrics = evaluate_model_on_loader(model, val_loader, settings.ROOM_CLASSES, device=device)
        val_acc = val_metrics["accuracy"]
        val_f1 = val_metrics["macro_f1"]
        
        epoch_record = {
            "epoch": epoch,
            "train_loss": round(train_loss, 4),
            "train_acc": round(train_acc, 4),
            "val_acc": val_acc,
            "val_macro_f1": val_f1
        }
        history.append(epoch_record)
        logger.info(
            f"Epoch {epoch}/{epochs} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
            f"Val Acc: {val_acc:.4f}, Val F1: {val_f1:.4f}"
        )
        
        if progress_callback:
            progress_callback(epoch, epochs, train_loss, val_acc)
            
        # Save best checkpoint
        if val_f1 >= best_val_f1 or epoch == 1:
            best_val_f1 = val_f1
            torch.save(model.state_dict(), best_weights_path)
            
    training_duration = round(time.time() - start_time, 2)
    
    # Final evaluation on held-out test loader
    model.load_state_dict(torch.load(best_weights_path, map_location=device))
    test_metrics = evaluate_model_on_loader(model, test_loader, settings.ROOM_CLASSES, device=device)
    
    provenance = (
        "Preliminary synthetic/sample placeholder dataset. Metrics are indicative of pipeline execution only."
        if is_synthetic_demo
        else "Curated interior room dataset."
    )
    
    # Save metadata JSON
    metadata = {
        "version_tag": version_tag,
        "architecture": "MobileNetV3-Small",
        "num_classes": num_classes,
        "classes": settings.ROOM_CLASSES,
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": lr,
        "training_samples_per_class": counts,
        "total_samples": total_samples,
        "is_synthetic_demo": is_synthetic_demo,
        "provenance_notes": provenance,
        "training_duration_seconds": training_duration,
        "test_metrics": test_metrics,
        "training_history": history,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    metadata_path = os.path.join(output_dir, f"model_{version_tag}.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
        
    class_mapping_path = os.path.join(output_dir, "class_mapping.json")
    with open(class_mapping_path, "w") as f:
        json.dump({cls: idx for idx, cls in enumerate(settings.ROOM_CLASSES)}, f, indent=2)
        
    logger.info(f"Training completed successfully. Artifacts saved at {output_dir}")
    return metadata
