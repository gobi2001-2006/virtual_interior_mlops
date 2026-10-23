import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.ml.train import train_classifier
from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.services.model_registry_service import ModelRegistryService

def main():
    parser = argparse.ArgumentParser(description="Train MobileNetV3-Small Room Classifier")
    parser.add_argument("--data-dir", default="./ml/data/raw", help="Path to raw dataset")
    parser.add_argument("--output-dir", default="./ml/artifacts", help="Path to output artifacts")
    parser.add_argument("--version", default="v001", help="Version tag for model checkpoint")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    args = parser.parse_args()

    print(f"=== Starting Training Run for Model '{args.version}' ===")
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Epochs: {args.epochs}, Batch Size: {args.batch_size}, LR: {args.lr}")

    try:
        metadata = train_classifier(
            data_dir=args.data_dir,
            output_dir=args.output_dir,
            version_tag=args.version,
            epochs=args.epochs,
            batch_size=args.batch_size,
            lr=args.lr
        )
        print("\n=== Training Completed Successfully ===")
        test_metrics = metadata.get("test_metrics", {})
        print(f"Test Accuracy: {test_metrics.get('accuracy', 0.0):.4f}")
        print(f"Test Macro F1: {test_metrics.get('macro_f1', 0.0):.4f}")
        
        # Register in DB
        with SessionLocal() as db:
            ModelRegistryService.register_model_version(
                db=db,
                version_tag=args.version,
                weights_path=str(Path(args.output_dir) / f"model_{args.version}.pth"),
                metadata_path=str(Path(args.output_dir) / f"model_{args.version}.json"),
                accuracy=test_metrics.get('accuracy', 0.0),
                macro_f1=test_metrics.get('macro_f1', 0.0)
            )
            print(f"Registered version '{args.version}' in database model registry.")

    except ValueError as e:
        print(f"\n[Training Halted]: {e}", file=sys.stderr)
        print("Please prepare the dataset using ml/scripts/prepare_dataset.py before training.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[Training Error]: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
