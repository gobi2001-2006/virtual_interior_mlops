import os
import sys
import io
import json
import hashlib
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any, Optional
from collections import defaultdict
import random

from PIL import Image

# Canonical target project room classes
TARGET_CLASSES = [
    "Bathroom",
    "Bedroom",
    "DiningRoom",
    "HomeOffice",
    "Kitchen",
    "LivingRoom",
    "Other"
]

# Required interior categories in source directory
REQUIRED_SOURCE_CATEGORIES = [
    "bathroom",
    "bedroom",
    "dining",
    "kitchen",
    "living",
    "office"
]

# Explicit semantic mapping policy
SOURCE_CLASS_MAPPING = {
    "bathroom": "Bathroom",
    "bathrooms": "Bathroom",
    "bedroom": "Bedroom",
    "bedrooms": "Bedroom",
    "dining": "DiningRoom",
    "dining room": "DiningRoom",
    "dining_room": "DiningRoom",
    "diningroom": "DiningRoom",
    "kitchen": "Kitchen",
    "kitchens": "Kitchen",
    "living": "LivingRoom",
    "living room": "LivingRoom",
    "living_room": "LivingRoom",
    "livingroom": "LivingRoom",
    "office": "HomeOffice",
    "office room": "HomeOffice",
    "office_room": "HomeOffice",
    "officeroom": "HomeOffice",
    "home office": "HomeOffice",
    "home_office": "HomeOffice",
    "other": "Other",
}

# Explicitly excluded non-interior categories with rationale
EXCLUDED_CATEGORIES = {
    "gaming": "Specialized entertainment room lacking standard architectural interior furniture typology",
    "gaming room": "Specialized entertainment room lacking standard architectural interior furniture typology",
    "gaming_room": "Specialized entertainment room lacking standard architectural interior furniture typology",
    "laundry": "Utility and appliance space outside interior furnishing recommendation scope",
    "laundry room": "Utility and appliance space outside interior furnishing recommendation scope",
    "terrace": "Exterior/semi-outdoor architectural space outside interior furniture scope",
    "yard": "Outdoor landscaping and exterior grounds outside interior room scope",
    "backyard": "Outdoor landscaping and exterior grounds outside interior room scope",
}

def compute_file_hash(filepath: Path) -> str:
    """Computes SHA256 file hash for exact duplicate detection."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def compute_dhash_from_img(img: Image.Image, hash_size: int = 8) -> int:
    """Computes 64-bit difference hash (dHash) directly from an opened PIL Image."""
    try:
        gray = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = list(gray.getdata())
        diff = []
        for row in range(hash_size):
            row_start = row * (hash_size + 1)
            for col in range(hash_size):
                diff.append(pixels[row_start + col] > pixels[row_start + col + 1])
        decimal_value = 0
        for idx, val in enumerate(diff):
            if val:
                decimal_value += 2 ** idx
        return decimal_value
    except Exception:
        return 0

def compute_dhash(image_path: Path, hash_size: int = 8) -> int:
    """Computes difference hash (dHash) from image filepath."""
    try:
        with Image.open(image_path) as img:
            return compute_dhash_from_img(img, hash_size=hash_size)
    except Exception:
        return 0

def hamming_distance(h1: int, h2: int) -> int:
    """Calculates bitwise Hamming distance between two perceptual hashes."""
    return (h1 ^ h2).bit_count()

def resolve_dataset_source_path(source_dir: str) -> Path:
    """
    Resolves the raw dataset folder.
    If the directory contains a 'room-dataset' subdirectory, uses that subdirectory.
    """
    path = Path(source_dir).resolve()
    if path.exists():
        sub_room = path / "room-dataset"
        if sub_room.exists() and sub_room.is_dir():
            return sub_room
    return path

def validate_source_structure(source_path: Path, required_categories: List[str]):
    """
    Validates that the source directory exists and contains all required categories.
    Fails loudly with a ValueError if expected categories are missing.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_path}")
    
    subdirs = {d.name.lower(): d for d in source_path.iterdir() if d.is_dir()}
    missing = [c for c in required_categories if c.lower() not in subdirs]
    if missing:
        raise ValueError(
            f"Source path validation failed loudly: Required categories {missing} missing in {source_path}. "
            f"Found subdirectories: {list(subdirs.keys())}"
        )

def inspect_and_prepare_dataset(
    source_dir: str = "ml/data/downloads/house-rooms/room-dataset",
    output_dir: str = "ml/data/processed/house_rooms",
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
    hamming_threshold: int = 3,
    required_classes: Optional[List[str]] = None,
    min_samples_per_class: int = 50,
    validate_expected_folders: bool = False,
    custom_mapping: Optional[Dict[str, str]] = None,
    excluded_categories: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Complete high-performance preprocessing pipeline:
    1. Validates source path and loudly asserts required category presence.
    2. Applies explicit semantic mapping and filters excluded categories.
    3. Single-pass memory hashing for SHA256 and perceptual dHash.
    4. Exact duplicate and perceptual near-duplicate cluster formation per class.
    5. Stratified train/val/test splitting with seed 42 (zero leakage across splits).
    6. High-speed file copying to processed split folders.
    7. JSON and Markdown report generation.
    """
    source_path = resolve_dataset_source_path(source_dir)
    output_path = Path(output_dir).resolve()
    
    print("=" * 80, flush=True)
    print("M L O p s   D a t a s e t   P r e p a r a t i o n   P i p e l i n e", flush=True)
    print(f"Source Directory: {source_path}", flush=True)
    print(f"Output Directory: {output_path}", flush=True)
    print(f"Random Seed:      {seed}", flush=True)
    print(f"Splits Target:    Train={1.0 - val_ratio - test_ratio:.2f}, Val={val_ratio:.2f}, Test={test_ratio:.2f}", flush=True)
    print("=" * 80, flush=True)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not source_path.exists():
        return _handle_missing_dataset(source_path, output_path, "Source directory does not exist.")
        
    # Validation of required categories
    if validate_expected_folders:
        validate_source_structure(source_path, REQUIRED_SOURCE_CATEGORIES)
        print(f"[Validation Passed] All required category folders verified in {source_path.name}:", flush=True)
        print(f"  {REQUIRED_SOURCE_CATEGORIES}", flush=True)
        
    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    discovered_files = [f for f in source_path.rglob("*") if f.is_file() and f.suffix.lower() in image_extensions]
    
    if len(discovered_files) == 0:
        return _handle_missing_dataset(source_path, output_path, "No image files found in download directory.")
        
    print(f"\n[1/5] Discovered {len(discovered_files)} raw image files across categories.", flush=True)
    
    # Active mapping and exclusion policies
    active_mapping = dict(SOURCE_CLASS_MAPPING)
    if custom_mapping:
        active_mapping.update(custom_mapping)
        
    active_exclusions = dict(EXCLUDED_CATEGORIES)
    if excluded_categories:
        active_exclusions.update(excluded_categories)
        
    valid_records: List[Dict[str, Any]] = []
    corrupted_count = 0
    excluded_count = 0
    excluded_by_category: Dict[str, int] = defaultdict(int)
    unmapped_skipped_count = 0
    unmapped_by_category: Dict[str, int] = defaultdict(int)
    
    print("Processing and verifying images...", flush=True)
    for idx, f in enumerate(discovered_files):
        parent_name = f.parent.name.strip().lower()
        
        # 1. Check policy exclusion
        if parent_name in active_exclusions:
            excluded_count += 1
            excluded_by_category[parent_name] += 1
            continue
            
        # 2. Check semantic class mapping
        target_class = active_mapping.get(parent_name)
        if not target_class:
            grandparent_name = f.parent.parent.name.strip().lower()
            if grandparent_name in active_exclusions:
                excluded_count += 1
                excluded_by_category[grandparent_name] += 1
                continue
            target_class = active_mapping.get(grandparent_name)
            
        if not target_class:
            unmapped_skipped_count += 1
            unmapped_by_category[parent_name] += 1
            continue
            
        # 3. High-speed single-pass memory verification and hashing
        try:
            content = f.read_bytes()
            sha256_hash = hashlib.sha256(content).hexdigest()
            
            with Image.open(io.BytesIO(content)) as img:
                img.verify()
                
            # Reopen in memory for dHash thumbnail
            with Image.open(io.BytesIO(content)) as img:
                dhash_val = compute_dhash_from_img(img)
                
            valid_records.append({
                "path": f,
                "target_class": target_class,
                "sha256": sha256_hash,
                "dhash": dhash_val,
                "source_parent": parent_name
            })
        except Exception:
            corrupted_count += 1
            
        if (idx + 1) % 2500 == 0:
            print(f"  ...processed {idx + 1}/{len(discovered_files)} files ({len(valid_records)} valid interior images)", flush=True)
            
    print(f"\n[Filtering & Integrity Summary]", flush=True)
    print(f"  - Valid interior images: {len(valid_records)}", flush=True)
    print(f"  - Corrupted files:       {corrupted_count}", flush=True)
    print(f"  - Policy excluded files: {excluded_count}", flush=True)
    for cat, count in sorted(excluded_by_category.items()):
        print(f"      * {cat}: {count} ({active_exclusions.get(cat, 'Excluded')})", flush=True)
    if unmapped_skipped_count > 0:
        print(f"  - Unmapped skipped:      {unmapped_skipped_count} ({dict(unmapped_by_category)})", flush=True)
        
    if len(valid_records) == 0:
        raise ValueError("Preprocessing error: No valid images found after filtering and integrity checks.")
        
    # [2/5] Exact & Perceptual Duplicate Clustering
    print("\n[2/5] Performing duplicate clustering within target classes...", flush=True)
    records_by_class: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for rec in valid_records:
        records_by_class[rec["target_class"]].append(rec)
        
    total_exact_duplicates = 0
    total_perceptual_duplicates = 0
    all_clusters: List[List[Dict[str, Any]]] = []
    
    for cls, class_records in records_by_class.items():
        # Exact SHA256 grouping
        exact_groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for rec in class_records:
            exact_groups[rec["sha256"]].append(rec)
            
        exact_dupes_in_class = sum(len(g) - 1 for g in exact_groups.values() if len(g) > 1)
        total_exact_duplicates += exact_dupes_in_class
        
        unique_class_items = [g[0] for g in exact_groups.values()]
        
        # Perceptual near-duplicate clustering (Hamming <= threshold)
        class_clusters: List[List[Dict[str, Any]]] = []
        visited_hashes: Set[str] = set()
        
        for i, item_a in enumerate(unique_class_items):
            if item_a["sha256"] in visited_hashes:
                continue
            current_cluster = list(exact_groups[item_a["sha256"]])
            visited_hashes.add(item_a["sha256"])
            h_a = item_a["dhash"]
            
            for j in range(i + 1, len(unique_class_items)):
                item_b = unique_class_items[j]
                if item_b["sha256"] in visited_hashes:
                    continue
                if (h_a ^ item_b["dhash"]).bit_count() <= hamming_threshold:
                    current_cluster.extend(exact_groups[item_b["sha256"]])
                    visited_hashes.add(item_b["sha256"])
                    
            class_clusters.append(current_cluster)
            
        perceptual_dupes_in_class = len(unique_class_items) - len(class_clusters)
        total_perceptual_duplicates += perceptual_dupes_in_class
        all_clusters.extend(class_clusters)
        print(f"  - {cls:<12}: {len(class_records)} images -> {len(class_clusters)} unique visual clusters ({exact_dupes_in_class} exact dupes, {perceptual_dupes_in_class} near dupes)", flush=True)
        
    print(f"\n  Total Exact Duplicates (SHA256):           {total_exact_duplicates}", flush=True)
    print(f"  Total Perceptual Near-Duplicates (dHash):    {total_perceptual_duplicates}", flush=True)
    print(f"  Total Unique Visual Clusters:               {len(all_clusters)}", flush=True)
    
    # [3/5] Stratified Cluster Splitting
    print("\n[3/5] Splitting clusters into Train, Val, and Test sets (Seed={seed})...", flush=True)
    random.seed(seed)
    
    clusters_by_class: Dict[str, List[List[Dict[str, Any]]]] = defaultdict(list)
    for cluster in all_clusters:
        primary_class = cluster[0]["target_class"]
        clusters_by_class[primary_class].append(cluster)
        
    # Enforce minimum sample counts
    target_req_classes = required_classes if required_classes is not None else [
        "Bathroom", "Bedroom", "DiningRoom", "HomeOffice", "Kitchen", "LivingRoom"
    ]
    if required_classes is not None or validate_expected_folders:
        for req_cls in target_req_classes:
            cls_clusters = clusters_by_class.get(req_cls, [])
            total_cls_images = sum(len(c) for c in cls_clusters)
            if total_cls_images == 0:
                raise ValueError(
                    f"Preprocessing halted: Required room class '{req_cls}' is missing from the dataset. "
                    f"Discovered classes: {list(clusters_by_class.keys())}"
                )
            if total_cls_images < min_samples_per_class:
                raise ValueError(
                    f"Preprocessing halted: Required room class '{req_cls}' has insufficient images "
                    f"({total_cls_images} < {min_samples_per_class} threshold)."
                )
                
    split_records: Dict[str, Dict[str, List[Path]]] = {
        "train": defaultdict(list),
        "val": defaultdict(list),
        "test": defaultdict(list)
    }
    class_counts_summary: Dict[str, Dict[str, int]] = {}
    
    for cls, cls_clusters in clusters_by_class.items():
        random.shuffle(cls_clusters)
        n = len(cls_clusters)
        n_test = max(1, int(n * test_ratio)) if n >= 5 else 0
        n_val = max(1, int(n * val_ratio)) if n >= 5 else 0
        n_train = n - n_val - n_test
        if n_train <= 0:
            n_train = n
            n_val = 0
            n_test = 0
            
        train_clusters = cls_clusters[:n_train]
        val_clusters = cls_clusters[n_train:n_train + n_val]
        test_clusters = cls_clusters[n_train + n_val:]
        
        for c in train_clusters:
            for item in c:
                split_records["train"][cls].append(item["path"])
        for c in val_clusters:
            for item in c:
                split_records["val"][cls].append(item["path"])
        for c in test_clusters:
            for item in c:
                split_records["test"][cls].append(item["path"])
                
        class_counts_summary[cls] = {
            "total_clusters": n,
            "total_images": sum(len(c) for c in cls_clusters),
            "train": len(split_records["train"][cls]),
            "val": len(split_records["val"][cls]),
            "test": len(split_records["test"][cls]),
        }
        
    # [4/5] Write Processed Dataset to Output Directory
    print("\n[4/5] Writing processed images to structured split directories...", flush=True)
    for split in ["train", "val", "test"]:
        for cls in TARGET_CLASSES:
            target_dir = output_path / split / cls
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
        for cls, paths in split_records[split].items():
            target_dir = output_path / split / cls
            for idx, p in enumerate(paths):
                dest_file = target_dir / f"{cls.lower()}_{idx:05d}{p.suffix.lower()}"
                try:
                    shutil.copy2(p, dest_file)
                except Exception as ex:
                    print(f"Warning: could not copy {p} -> {dest_file}: {ex}", flush=True)
                    
    total_train = sum(len(paths) for paths in split_records["train"].values())
    total_val = sum(len(paths) for paths in split_records["val"].values())
    total_test = sum(len(paths) for paths in split_records["test"].values())
    
    print(f"  - Train split:    {total_train} images", flush=True)
    print(f"  - Val split:      {total_val} images", flush=True)
    print(f"  - Test split:     {total_test} images", flush=True)
    print(f"  - Total deployed: {total_train + total_val + total_test} images", flush=True)
    
    # [5/5] Generate Reports
    report = {
        "status": "prepared",
        "dataset_name": "Kaggle House Rooms (annielu21/house-rooms)",
        "source_url": "https://www.kaggle.com/datasets/annielu21/house-rooms",
        "source_path": str(source_path),
        "license": "CC BY-SA 4.0 (Verify on Kaggle dataset page before commercial deployment)",
        "split_seed": seed,
        "splits": {
            "train_ratio": round(1.0 - val_ratio - test_ratio, 2),
            "val_ratio": val_ratio,
            "test_ratio": test_ratio
        },
        "statistics": {
            "discovered_files": len(discovered_files),
            "valid_images": len(valid_records),
            "corrupted_images": corrupted_count,
            "excluded_images": excluded_count,
            "unmapped_skipped_images": unmapped_skipped_count,
            "exact_duplicates": total_exact_duplicates,
            "perceptual_duplicates": total_perceptual_duplicates,
            "unique_image_clusters": len(all_clusters),
            "train_count": total_train,
            "val_count": total_val,
            "test_count": total_test
        },
        "class_mapping_policy": {
            "bathroom": "Bathroom",
            "bedroom": "Bedroom",
            "dining": "DiningRoom",
            "kitchen": "Kitchen",
            "living": "LivingRoom",
            "office": "HomeOffice"
        },
        "excluded_policy": {
            "gaming": "Specialized entertainment room lacking standard architectural interior furniture typology",
            "laundry": "Utility and appliance space outside interior furnishing recommendation scope",
            "terrace": "Exterior/semi-outdoor architectural space outside interior furniture scope",
            "yard": "Outdoor landscaping and exterior grounds outside interior room scope"
        },
        "excluded_by_category": dict(excluded_by_category),
        "per_class_summary": class_counts_summary
    }
    
    report_json_path = output_path / "dataset_report.json"
    report_md_path = output_path / "dataset_report.md"
    
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    _write_markdown_report(report, report_md_path)
    
    print(f"\n[Done] Dataset successfully processed and verified.", flush=True)
    print(f"Report JSON: {report_json_path}", flush=True)
    print(f"Report MD:   {report_md_path}", flush=True)
    print("=" * 80, flush=True)
    return report

def _handle_missing_dataset(source_path: Path, output_path: Path, reason: str) -> Dict[str, Any]:
    print("\n" + "!" * 80, flush=True)
    print("DATASET ABSENT OR EMPTY NOTICE", flush=True)
    print("!" * 80, flush=True)
    print(f"Reason: {reason}", flush=True)
    print(f"Expected source directory: {source_path}", flush=True)
    print("\nTo download the Kaggle House Rooms dataset:", flush=True)
    print("1. Ensure your Kaggle API key is placed at: ~/.kaggle/kaggle.json", flush=True)
    print("2. Run the Kaggle CLI command:", flush=True)
    print("   kaggle datasets download -d annielu21/house-rooms -p ml/data/downloads/house-rooms/ --unzip", flush=True)
    print("3. Alternatively, download manually from:", flush=True)
    print("   https://www.kaggle.com/datasets/annielu21/house-rooms", flush=True)
    print("   and extract all class folders into: ml/data/downloads/house-rooms/room-dataset/", flush=True)
    print("\nPer requirements, synthetic samples are NOT substituted for the Kaggle dataset.", flush=True)
    print("!" * 80 + "\n", flush=True)
    
    report = {
        "status": "absent",
        "dataset_name": "Kaggle House Rooms (annielu21/house-rooms)",
        "source_url": "https://www.kaggle.com/datasets/annielu21/house-rooms",
        "license": "CC BY-SA 4.0 (verification required upon download)",
        "reason": reason,
        "expected_path": str(source_path),
        "download_instructions": {
            "kaggle_cli": "kaggle datasets download -d annielu21/house-rooms -p ml/data/downloads/house-rooms/ --unzip",
            "kaggle_credentials_path": "~/.kaggle/kaggle.json",
            "manual_url": "https://www.kaggle.com/datasets/annielu21/house-rooms"
        },
        "target_classes": TARGET_CLASSES,
        "class_mapping_policy": SOURCE_CLASS_MAPPING,
        "excluded_policy": EXCLUDED_CATEGORIES,
    }
    
    with open(output_path / "dataset_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    _write_markdown_report(report, output_path / "dataset_report.md")
    return report

def _write_markdown_report(report: Dict[str, Any], path: Path):
    lines = [
        "# Kaggle House Rooms Dataset Preparation Report",
        "",
        f"- **Dataset Source:** [{report['dataset_name']}]({report['source_url']})",
        f"- **Status:** `{report['status'].upper()}`",
        f"- **Source Path:** `{report.get('source_path', report.get('expected_path'))}`",
        f"- **License:** {report.get('license', 'Needs verification')}",
        "",
        "## Semantic Class Mapping Policy",
        "",
        "| Source Folder | Target Project Class | Policy |",
        "|---|---|---|",
        "| `bathroom` | `Bathroom` | Retained |",
        "| `bedroom` | `Bedroom` | Retained |",
        "| `dining` | `DiningRoom` | Retained |",
        "| `kitchen` | `Kitchen` | Retained |",
        "| `living` | `LivingRoom` | Retained |",
        "| `office` | `HomeOffice` | Retained |",
        "",
        "### Explicit Exclusions & Rationale",
        "",
        "| Excluded Category | Rationale | Discovered Excluded Count |",
        "|---|---|---|",
    ]
    
    ex_counts = report.get("excluded_by_category", {})
    for cat, reason in report.get("excluded_policy", {}).items():
        count = ex_counts.get(cat, 0)
        lines.append(f"| `{cat}` | {reason} | {count} |")
        
    lines.append("")
    if report["status"] == "absent":
        lines.extend([
            "## Dataset Absence Notice",
            "",
            f"The dataset is currently absent from `{report['expected_path']}`.",
            "",
            "### Download Command:",
            "```bash",
            f"{report['download_instructions']['kaggle_cli']}",
            "```",
            "",
            "> [!IMPORTANT]",
            "> Per strict MLOps evaluation policy, synthetic demo placeholders are **not** substituted for the verified Kaggle House Rooms dataset.",
        ])
    else:
        stats = report["statistics"]
        lines.extend([
            "## Ingestion & Deduplication Statistics",
            "",
            f"- **Total Discovered Source Files:** {stats['discovered_files']}",
            f"- **Valid Interior Images Processed:** {stats['valid_images']}",
            f"- **Corrupted / Unreadable Images:** {stats['corrupted_images']}",
            f"- **Excluded Category Images:** {stats['excluded_images']}",
            f"- **Unmapped Skipped Images:** {stats.get('unmapped_skipped_images', 0)}",
            f"- **Exact Duplicates (SHA256):** {stats['exact_duplicates']}",
            f"- **Perceptual Near-Duplicates (dHash):** {stats['perceptual_duplicates']}",
            f"- **Unique Visual Clusters:** {stats['unique_image_clusters']}",
            f"- **Train Split Count:** {stats['train_count']}",
            f"- **Validation Split Count:** {stats['val_count']}",
            f"- **Test Split Count:** {stats['test_count']}",
            f"- **Split Seed:** {report['split_seed']}",
            "",
            "## Per-Class Split Counts",
            "",
            "| Class | Total Images | Unique Clusters | Train | Val | Test |",
            "|---|---|---|---|---|---|",
        ])
        for cls, counts in sorted(report.get("per_class_summary", {}).items()):
            tot_img = counts.get("total_images", counts["train"] + counts["val"] + counts["test"])
            lines.append(
                f"| **{cls}** | {tot_img} | {counts['total_clusters']} | {counts['train']} | {counts['val']} | {counts['test']} |"
            )
            
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare, clean, deduplicate, and split Kaggle House Rooms dataset")
    parser.add_argument(
        "--source-dir",
        default="ml/data/downloads/house-rooms/room-dataset",
        help="Source directory containing raw room folders"
    )
    parser.add_argument(
        "--output-dir",
        default="ml/data/processed/house_rooms",
        help="Output directory for processed train/val/test splits"
    )
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation ratio")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test ratio")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--min-samples", type=int, default=50, help="Minimum images required per class")
    parser.add_argument(
        "--require-classes",
        default="Bathroom,Bedroom,DiningRoom,Kitchen,LivingRoom,HomeOffice",
        help="Comma-separated list of required classes"
    )
    parser.add_argument(
        "--exclude-categories",
        default="gaming,laundry,terrace,yard",
        help="Comma-separated list of raw categories to exclude"
    )
    args = parser.parse_args()
    
    req_classes = [c.strip() for c in args.require_classes.split(",") if c.strip()]
    ex_cats = {c.strip(): f"User configured exclusion for {c.strip()}" for c in args.exclude_categories.split(",") if c.strip()}
    
    inspect_and_prepare_dataset(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
        required_classes=req_classes,
        min_samples_per_class=args.min_samples,
        validate_expected_folders=True,
        excluded_categories=ex_cats
    )
