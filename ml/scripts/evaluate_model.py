import os
import sys
import argparse
from pathlib import Path
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.core.config import settings
from backend.app.ml.model import build_model
from backend.app.ml.dataset import create_data_loaders
from backend.app.ml.evaluate import evaluate_model_on_loader

def main():
    parser = argparse.ArgumentParser(description="Evaluate Room Classifier Checkpoint")
    parser.add_argument("--version", default="v001", help="Model version tag to evaluate")
    parser.add_argument("--data-dir", default="./ml/data/raw", help="Path to evaluation dataset")
    parser.add_argument("--artifacts-dir", default="./ml/artifacts", help="Path to artifacts folder")
    args = parser.parse_args()

    weights_file = Path(args.artifacts_dir) / f"model_{args.version}.pth"
    if not weights_file.exists():
        print(f"Error: Weights file '{weights_file}' not found. Please train model '{args.version}' first.")
        sys.exit(1)

    print(f"Loading weights from {weights_file}...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    num_classes = len(settings.ROOM_CLASSES)
    model = build_model(num_classes=num_classes, pretrained=False)
    model.load_state_dict(torch.load(weights_file, map_location=device))
    
    _, _, test_loader, counts, _ = create_data_loaders(
        data_dir=args.data_dir,
        class_names=settings.ROOM_CLASSES,
        batch_size=16
    )
    
    if test_loader is None or sum(counts.values()) == 0:
        print(f"Error: No images found in '{args.data_dir}' to evaluate on.")
        sys.exit(1)
        
    print(f"Evaluating model on test split ({device})...")
    metrics = evaluate_model_on_loader(model, test_loader, settings.ROOM_CLASSES, device=device)
    
    print("\n================ EVALUATION RESULTS ================")
    print(f"Model Version : {args.version}")
    print(f"Sample Count  : {metrics['sample_count']}")
    print(f"Accuracy      : {metrics['accuracy']:.4f}")
    print(f"Macro F1      : {metrics['macro_f1']:.4f}")
    print(f"Precision     : {metrics['precision']:.4f}")
    print(f"Recall        : {metrics['recall']:.4f}")
    print("----------------------------------------------------")
    print("Per-Class Breakdown:")
    for cls, vals in metrics["per_class_metrics"].items():
        print(f"  {cls:12} -> F1: {vals['f1_score']:.4f} | Prec: {vals['precision']:.4f} | Rec: {vals['recall']:.4f} | Support: {vals['support']}")
    print("====================================================")

if __name__ == "__main__":
    main()
