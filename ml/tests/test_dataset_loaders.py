import os
import shutil
from pathlib import Path
import pytest
from PIL import Image

from backend.app.ml.dataset import (
    create_data_loaders,
    DEFAULT_HOUSE_ROOM_CLASSES,
    SUPPORTED_IMAGE_EXTENSIONS
)

PROCESSED_HOUSE_ROOMS_DIR = Path("ml/data/processed/house_rooms")

@pytest.mark.skipif(
    not PROCESSED_HOUSE_ROOMS_DIR.exists() or not (PROCESSED_HOUSE_ROOMS_DIR / "train").exists(),
    reason="Prepared dataset ml/data/processed/house_rooms not found"
)
def test_prepared_split_loading_and_counts():
    """
    Verifies that create_data_loaders loads the prepared train, val, and test splits
    independently without re-splitting, producing accurate counts and is_synthetic_demo=False.
    """
    train_loader, val_loader, test_loader, counts, is_synthetic_demo = create_data_loaders(
        data_dir=str(PROCESSED_HOUSE_ROOMS_DIR),
        batch_size=16
    )

    assert train_loader is not None
    assert val_loader is not None
    assert test_loader is not None

    # Expected split totals from dataset report
    assert len(train_loader.dataset) == 4620
    assert len(val_loader.dataset) == 987
    assert len(test_loader.dataset) == 1003

    # Total dataset should be 6610
    total_samples = len(train_loader.dataset) + len(val_loader.dataset) + len(test_loader.dataset)
    assert total_samples == 6610

    # Ensure synthetic demo flag is False for the real dataset
    assert is_synthetic_demo is False

    # Check exact per-class counts across all splits
    expected_class_counts = {
        "Bathroom": 740,
        "Bedroom": 1083,
        "DiningRoom": 1176,
        "HomeOffice": 1240,
        "Kitchen": 1207,
        "LivingRoom": 1164
    }
    for cls, expected_count in expected_class_counts.items():
        assert counts.get(cls) == expected_count, f"Count mismatch for {cls}: expected {expected_count}, got {counts.get(cls)}"

@pytest.mark.skipif(
    not PROCESSED_HOUSE_ROOMS_DIR.exists() or not (PROCESSED_HOUSE_ROOMS_DIR / "train").exists(),
    reason="Prepared dataset ml/data/processed/house_rooms not found"
)
def test_no_cross_split_path_overlap():
    """
    Verifies that there is strict zero-overlap in file paths across train, val, and test splits.
    """
    train_loader, val_loader, test_loader, _, _ = create_data_loaders(
        data_dir=str(PROCESSED_HOUSE_ROOMS_DIR),
        batch_size=16
    )

    train_paths = {p for p, _ in train_loader.dataset.samples}
    val_paths = {p for p, _ in val_loader.dataset.samples}
    test_paths = {p for p, _ in test_loader.dataset.samples}

    assert len(train_paths & val_paths) == 0, f"Found {len(train_paths & val_paths)} overlapping paths between train and val"
    assert len(train_paths & test_paths) == 0, f"Found {len(train_paths & test_paths)} overlapping paths between train and test"
    assert len(val_paths & test_paths) == 0, f"Found {len(val_paths & test_paths)} overlapping paths between val and test"

    total_unique = len(train_paths | val_paths | test_paths)
    assert total_unique == 6610

@pytest.mark.skipif(
    not PROCESSED_HOUSE_ROOMS_DIR.exists() or not (PROCESSED_HOUSE_ROOMS_DIR / "train").exists(),
    reason="Prepared dataset ml/data/processed/house_rooms not found"
)
def test_class_mapping_consistency():
    """
    Verifies that label indices consistently map to the directory class name across all splits.
    """
    class_names = list(DEFAULT_HOUSE_ROOM_CLASSES)
    train_loader, val_loader, test_loader, _, _ = create_data_loaders(
        data_dir=str(PROCESSED_HOUSE_ROOMS_DIR),
        class_names=class_names,
        batch_size=16
    )

    class_to_idx = {cls: idx for idx, cls in enumerate(class_names)}

    for split_name, loader in [("train", train_loader), ("val", val_loader), ("test", test_loader)]:
        for path_str, label in loader.dataset.samples:
            path = Path(path_str)
            # The folder name immediately under the split is the class name
            # (or for nested paths, ensure it belongs to the expected class folder)
            expected_class = class_names[label]
            assert path.parent.name == expected_class or expected_class in path.parts, (
                f"Mismatch in {split_name}: file {path} has label {label} ({expected_class})"
            )
            assert class_to_idx[expected_class] == label

def test_missing_expected_class_fails_loudly(tmp_path):
    """
    Verifies that create_data_loaders raises ValueError if an expected class folder is missing.
    """
    for split in ["train", "val", "test"]:
        for cls in DEFAULT_HOUSE_ROOM_CLASSES:
            # Omit 'Kitchen' in 'val'
            if split == "val" and cls == "Kitchen":
                continue
            folder = tmp_path / split / cls
            folder.mkdir(parents=True, exist_ok=True)
            dummy_img = folder / "img1.jpg"
            Image.new("RGB", (64, 64), color="blue").save(dummy_img)

    with pytest.raises(ValueError) as excinfo:
        create_data_loaders(data_dir=str(tmp_path))

    assert "missing in 'val' split" in str(excinfo.value)
    assert "Kitchen" in str(excinfo.value)

def test_empty_expected_class_fails_loudly(tmp_path):
    """
    Verifies that create_data_loaders raises ValueError if an expected class folder contains no valid images.
    """
    for split in ["train", "val", "test"]:
        for cls in DEFAULT_HOUSE_ROOM_CLASSES:
            folder = tmp_path / split / cls
            folder.mkdir(parents=True, exist_ok=True)
            # Leave 'LivingRoom' empty in 'test'
            if split == "test" and cls == "LivingRoom":
                continue
            dummy_img = folder / "img1.png"
            Image.new("RGB", (64, 64), color="red").save(dummy_img)

    with pytest.raises(ValueError) as excinfo:
        create_data_loaders(data_dir=str(tmp_path))

    assert "contains no valid images in 'test' split" in str(excinfo.value)
    assert "LivingRoom" in str(excinfo.value)

def test_supported_extensions_and_recursive_loading(tmp_path):
    """
    Verifies recursive traversal and support for .jpg, .jpeg, .png, and .webp while ignoring other files.
    """
    for split in ["train", "val", "test"]:
        for cls in DEFAULT_HOUSE_ROOM_CLASSES:
            folder = tmp_path / split / cls
            folder.mkdir(parents=True, exist_ok=True)
            
            # Direct files
            Image.new("RGB", (32, 32)).save(folder / "img1.jpg")
            Image.new("RGB", (32, 32)).save(folder / "img2.jpeg")
            
            # Nested subfolder
            sub = folder / "nested_subfolder"
            sub.mkdir()
            Image.new("RGB", (32, 32)).save(sub / "img3.png")
            Image.new("RGB", (32, 32)).save(sub / "img4.webp")
            
            # Non-image file to ignore
            (sub / "notes.txt").write_text("not an image")

    train_loader, val_loader, test_loader, counts, is_demo = create_data_loaders(
        data_dir=str(tmp_path)
    )

    # Each split has 6 classes * 4 images = 24 images
    assert len(train_loader.dataset) == 24
    assert len(val_loader.dataset) == 24
    assert len(test_loader.dataset) == 24

    # Each class has 4 images * 3 splits = 12 images
    for cls in DEFAULT_HOUSE_ROOM_CLASSES:
        assert counts[cls] == 12

def test_fallback_flat_directory_loading(tmp_path):
    """
    Verifies backward compatibility: flat directory without train/val/test splits
    falls back to random reproducible splitting.
    """
    for cls in DEFAULT_HOUSE_ROOM_CLASSES:
        folder = tmp_path / cls
        folder.mkdir(parents=True, exist_ok=True)
        for i in range(10):
            Image.new("RGB", (32, 32)).save(folder / f"sample_{i}.jpg")

    train_loader, val_loader, test_loader, counts, is_demo = create_data_loaders(
        data_dir=str(tmp_path),
        class_names=DEFAULT_HOUSE_ROOM_CLASSES,
        train_ratio=0.7,
        val_ratio=0.15,
        seed=42
    )

    assert train_loader is not None
    assert val_loader is not None
    assert test_loader is not None
    total = len(train_loader.dataset) + len(val_loader.dataset) + len(test_loader.dataset)
    assert total == 60
    assert counts["Bathroom"] == 10
