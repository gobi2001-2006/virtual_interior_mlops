import os
import random
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from backend.app.core.config import settings
from backend.app.ml.transforms import get_train_transforms, get_eval_transforms

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

DEFAULT_HOUSE_ROOM_CLASSES: List[str] = [
    "Bathroom",
    "Bedroom",
    "DiningRoom",
    "HomeOffice",
    "Kitchen",
    "LivingRoom",
]

EXPECTED_ROOM_CLASSES: List[str] = DEFAULT_HOUSE_ROOM_CLASSES

class RoomImageDataset(Dataset):
    def __init__(self, samples: List[Tuple[str, int]], transform=None):
        self.samples = samples  # List of (file_path, class_idx)
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        image_path, label = self.samples[idx]
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception:
            # Fallback to neutral gray image if corrupted
            image = Image.new("RGB", (224, 224), color=(128, 128, 128))
            
        if self.transform:
            image = self.transform(image)
        return image, label

def scan_split_directory(
    split_dir: Path,
    class_names: List[str],
    expected_classes: Optional[List[str]] = None,
    split_name: str = "split",
) -> Tuple[List[Tuple[str, int]], Dict[str, int]]:
    """
    Scans a split directory (train, val, or test) for class subdirectories.
    Recursively discovers all images matching SUPPORTED_IMAGE_EXTENSIONS.
    Validates that all expected_classes exist and are non-empty.
    Returns (samples, split_counts).
    """
    if expected_classes:
        for cls in expected_classes:
            cls_folder = split_dir / cls
            if not cls_folder.is_dir():
                raise ValueError(
                    f"Expected class directory '{cls}' is missing in '{split_name}' split at {cls_folder}."
                )
            has_image = any(
                p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
                for p in cls_folder.rglob("*")
            )
            if not has_image:
                raise ValueError(
                    f"Expected class '{cls}' contains no valid images in '{split_name}' split at {cls_folder}."
                )

    class_to_idx = {cls: idx for idx, cls in enumerate(class_names)}
    samples: List[Tuple[str, int]] = []
    counts: Dict[str, int] = {cls: 0 for cls in class_names}

    for cls in class_names:
        cls_folder = split_dir / cls
        if not cls_folder.is_dir():
            continue
        idx = class_to_idx[cls]
        img_files = sorted([
            p for p in cls_folder.rglob("*")
            if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ])
        for img_path in img_files:
            samples.append((str(img_path.resolve()), idx))
            counts[cls] += 1

    return samples, counts

def scan_dataset_directory(data_dir: str, class_names: List[str]) -> Tuple[List[Tuple[str, int]], Dict[str, int]]:
    """
    Scans flat data_dir looking for subfolders matching class_names.
    Returns list of (filepath, class_idx) and counts per class.
    """
    samples = []
    counts = {cls: 0 for cls in class_names}
    base_path = Path(data_dir)
    
    if not base_path.exists():
        return samples, counts
        
    for idx, class_name in enumerate(class_names):
        class_folder = base_path / class_name
        if not class_folder.is_dir():
            continue
            
        img_files = sorted([
            p for p in class_folder.rglob("*")
            if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ])
        for file in img_files:
            samples.append((str(file.resolve()), idx))
            counts[class_name] += 1
                
    return samples, counts

def create_data_loaders(
    data_dir: str,
    class_names: Optional[List[str]] = None,
    extra_samples: Optional[List[Tuple[str, int]]] = None,
    batch_size: int = 16,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    seed: int = 42,
    expected_classes: Optional[List[str]] = None,
    num_workers: int = 0
) -> Tuple[Optional[DataLoader], Optional[DataLoader], Optional[DataLoader], Dict[str, int], bool]:
    """
    Creates train, val, and test DataLoaders without data leakage.
    If data_dir contains existing 'train/', 'val/', and 'test/' directories,
    loads each split independently, preserving the prepared split assignments.
    Otherwise, splits the flat directory reproducibly using seed.
    Returns (train_loader, val_loader, test_loader, per_class_counts, is_synthetic_demo).
    """
    base_path = Path(data_dir)
    train_dir = base_path / "train"
    val_dir = base_path / "val"
    test_dir = base_path / "test"

    is_split_dir = train_dir.is_dir() and val_dir.is_dir() and test_dir.is_dir()

    if is_split_dir:
        # Determine active class names for prepared split mode
        if class_names is None:
            active_class_names = list(DEFAULT_HOUSE_ROOM_CLASSES)
        else:
            active_class_names = list(class_names)

        # Validate presence of expected room classes across all splits
        if expected_classes is None:
            if all(c in active_class_names for c in DEFAULT_HOUSE_ROOM_CLASSES):
                req_classes = list(DEFAULT_HOUSE_ROOM_CLASSES)
            elif any(c in active_class_names for c in DEFAULT_HOUSE_ROOM_CLASSES):
                req_classes = [c for c in DEFAULT_HOUSE_ROOM_CLASSES if c in active_class_names]
            else:
                req_classes = list(active_class_names)
        else:
            req_classes = list(expected_classes)

        train_samples, train_counts = scan_split_directory(
            train_dir, active_class_names, expected_classes=req_classes, split_name="train"
        )
        val_samples, val_counts = scan_split_directory(
            val_dir, active_class_names, expected_classes=req_classes, split_name="val"
        )
        test_samples, test_counts = scan_split_directory(
            test_dir, active_class_names, expected_classes=req_classes, split_name="test"
        )

        if extra_samples:
            for path, label in extra_samples:
                if 0 <= label < len(active_class_names):
                    train_samples.append((path, label))
                    train_counts[active_class_names[label]] += 1

        total_counts = {
            cls: train_counts[cls] + val_counts[cls] + test_counts[cls]
            for cls in active_class_names
        }
        total_samples = len(train_samples) + len(val_samples) + len(test_samples)

        if total_samples == 0:
            return None, None, None, total_counts, True

        is_synthetic_demo = (total_samples < 50) or any(
            "sample_" in p for p, _ in (train_samples + val_samples + test_samples)
        )

        train_dataset = RoomImageDataset(train_samples, transform=get_train_transforms())
        val_dataset = RoomImageDataset(val_samples, transform=get_eval_transforms())
        test_dataset = RoomImageDataset(test_samples, transform=get_eval_transforms())

        train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True, drop_last=False, num_workers=num_workers
        )
        val_loader = DataLoader(
            val_dataset, batch_size=batch_size, shuffle=False, drop_last=False, num_workers=num_workers
        )
        test_loader = DataLoader(
            test_dataset, batch_size=batch_size, shuffle=False, drop_last=False, num_workers=num_workers
        )

        return train_loader, val_loader, test_loader, total_counts, is_synthetic_demo

    # Fallback to flat directory scanning and reproducible splitting
    active_class_names = class_names if class_names is not None else settings.ROOM_CLASSES
    samples, counts = scan_dataset_directory(data_dir, active_class_names)
    
    if extra_samples:
        for path, label in extra_samples:
            if 0 <= label < len(active_class_names):
                samples.append((path, label))
                counts[active_class_names[label]] += 1
                
    total_samples = len(samples)
    if total_samples == 0:
        return None, None, None, counts, True

    # Detect if data is only minimal synthetic demo samples
    is_synthetic_demo = (total_samples < 50) or any("sample_" in p for p, _ in samples)
        
    random.seed(seed)
    train_samples, val_samples, test_samples = [], [], []
    
    class_to_samples = {i: [] for i in range(len(active_class_names))}
    for path, label in samples:
        class_to_samples[label].append((path, label))
        
    for label, items in class_to_samples.items():
        random.shuffle(items)
        n = len(items)
        if n == 0:
            continue
        elif n == 1:
            train_samples.append(items[0])
            test_samples.append(items[0])
            val_samples.append(items[0])
        elif n == 2:
            train_samples.append(items[0])
            test_samples.append(items[1])
            val_samples.append(items[1])
        else:
            n_train = max(1, int(n * train_ratio))
            n_val = max(1, int(n * val_ratio))
            if n_train + n_val >= n:
                n_train = max(1, n - 2)
                n_val = 1
            train_samples.extend(items[:n_train])
            val_samples.extend(items[n_train:n_train + n_val])
            test_samples.extend(items[n_train + n_val:])

    train_dataset = RoomImageDataset(train_samples, transform=get_train_transforms())
    val_dataset = RoomImageDataset(val_samples, transform=get_eval_transforms())
    test_dataset = RoomImageDataset(test_samples, transform=get_eval_transforms())
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, drop_last=False, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=False, num_workers=num_workers)
    
    return train_loader, val_loader, test_loader, counts, is_synthetic_demo
