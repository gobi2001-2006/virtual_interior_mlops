import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.db.session import SessionLocal
from backend.app.models.mlops import ModelVersion, ModelEvaluation

def compare_models(v1: str, v2: str):
    with SessionLocal() as db:
        m1 = db.query(ModelVersion).filter(ModelVersion.version_tag == v1).first()
        m2 = db.query(ModelVersion).filter(ModelVersion.version_tag == v2).first()
        
        if not m1 or not m2:
            print(f"Error: One or both models ({v1}, {v2}) could not be found in database.")
            sys.exit(1)
            
        print("\n================ MODEL VERSION COMPARISON ================")
        print(f"{'Metric':<20} | {v1:<15} | {v2:<15}")
        print("-" * 56)
        print(f"{'Architecture':<20} | {m1.architecture:<15} | {m2.architecture:<15}")
        print(f"{'Accuracy':<20} | {str(m1.accuracy):<15} | {str(m2.accuracy):<15}")
        print(f"{'Macro F1':<20} | {str(m1.macro_f1):<15} | {str(m2.macro_f1):<15}")
        print(f"{'Is Active':<20} | {str(m1.is_active):<15} | {str(m2.is_active):<15}")
        print(f"{'Is Promoted':<20} | {str(m1.is_promoted):<15} | {str(m2.is_promoted):<15}")
        print("==========================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two model version metrics")
    parser.add_argument("v1", help="First model version tag")
    parser.add_argument("v2", help="Second model version tag")
    args = parser.parse_args()
    compare_models(args.v1, args.v2)
