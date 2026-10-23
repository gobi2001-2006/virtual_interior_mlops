import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.db.session import SessionLocal
from backend.app.services.model_registry_service import ModelRegistryService

def main():
    parser = argparse.ArgumentParser(description="Promote evaluated model version to active production")
    parser.add_argument("version", help="Model version tag to promote (e.g. v001)")
    args = parser.parse_args()

    print(f"Requesting promotion for candidate version '{args.version}'...")
    try:
        with SessionLocal() as db:
            promoted = ModelRegistryService.promote_model(db, args.version)
            print(f"SUCCESS: Model '{promoted.version_tag}' is now active in production!")
    except Exception as e:
        print(f"FAILED TO PROMOTE: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
