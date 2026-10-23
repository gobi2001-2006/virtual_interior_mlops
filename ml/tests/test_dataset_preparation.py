import pytest
from pathlib import Path
from PIL import Image
import tempfile
import json
import shutil

from ml.scripts.prepare_dataset import (
    compute_file_hash,
    compute_dhash,
    hamming_distance,
    inspect_and_prepare_dataset,
    SOURCE_CLASS_MAPPING,
    EXCLUDED_CATEGORIES
)


def test_label_mapping_and_exclusions():
    """Verify semantic label mapping policies and documented exclusions."""
    assert SOURCE_CLASS_MAPPING["bedroom"] == "Bedroom"
    assert SOURCE_CLASS_MAPPING["living"] == "LivingRoom"
    assert SOURCE_CLASS_MAPPING["kitchen"] == "Kitchen"
    assert SOURCE_CLASS_MAPPING["dining"] == "DiningRoom"
    assert SOURCE_CLASS_MAPPING["bathroom"] == "Bathroom"
    assert SOURCE_CLASS_MAPPING["office"] == "HomeOffice"

    # Verify exclusions are explicit
    assert "gaming room" in EXCLUDED_CATEGORIES
    assert "terrace" in EXCLUDED_CATEGORIES
    assert "laundry" in EXCLUDED_CATEGORIES
    assert "yard" in EXCLUDED_CATEGORIES


def test_hashing_and_near_duplicate_detection():
    """Verify SHA256 and perceptual dHash duplicate clustering."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create two identical images
        img1 = Image.new("RGB", (64, 64), color="blue")
        p1 = tmp_path / "img1.jpg"
        p2 = tmp_path / "img2.jpg"
        img1.save(p1)
        img1.save(p2)

        # Create a third different image
        img3 = Image.new("RGB", (64, 64), color="red")
        p3 = tmp_path / "img3.jpg"
        img3.save(p3)

        hash1 = compute_file_hash(p1)
        hash2 = compute_file_hash(p2)
        hash3 = compute_file_hash(p3)

        assert hash1 == hash2
        assert hash1 != hash3

        d1 = compute_dhash(p1)
        d2 = compute_dhash(p2)
        d3 = compute_dhash(p3)
        assert hamming_distance(d1, d2) == 0


def test_missing_dataset_reporting():
    """Verify that an absent download folder generates an accurate report with download command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        empty_download = tmp_path / "non_existent_folder"
        proc_dir = tmp_path / "processed"

        report = inspect_and_prepare_dataset(str(empty_download), str(proc_dir))
        assert report["status"] == "absent"
        assert "kaggle datasets download" in report["download_instructions"]["kaggle_cli"]

        # Check JSON and MD files exist
        assert (proc_dir / "dataset_report.json").exists()
        assert (proc_dir / "dataset_report.md").exists()

        with open(proc_dir / "dataset_report.json") as f:
            data = json.load(f)
            assert data["status"] == "absent"


def test_corrupt_images_and_dataset_preparation():
    """Verify corrupted images are rejected and valid images split cleanly into train/val/test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        download_dir = tmp_path / "downloads"
        bedroom_dir = download_dir / "bedroom"
        bedroom_dir.mkdir(parents=True)

        # Create 10 valid images
        for i in range(10):
            img = Image.new("RGB", (32, 32), color=(i * 20, 50, 100))
            img.save(bedroom_dir / f"bed_{i}.jpg")

        # Create 1 corrupt image
        with open(bedroom_dir / "corrupt.jpg", "wb") as f:
            f.write(b"NOT_A_VALID_JPEG_HEADER")

        proc_dir = tmp_path / "processed"
        report = inspect_and_prepare_dataset(str(download_dir), str(proc_dir), seed=42)

        assert report["status"] == "prepared"
        assert report["statistics"]["corrupted_images"] == 1
        assert report["statistics"]["valid_images"] == 10
        assert (proc_dir / "train" / "Bedroom").exists()


def test_required_classes_validation():
    """Verify checks that stop preprocessing if required classes are missing or have too few images."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        download_dir = tmp_path / "downloads"
        bedroom_dir = download_dir / "bedroom"
        bedroom_dir.mkdir(parents=True)

        for i in range(10):
            img = Image.new("RGB", (32, 32), color=(i * 20, 50, 100))
            img.save(bedroom_dir / f"bed_{i}.jpg")

        proc_dir = tmp_path / "processed"

        # Missing required class 'Bathroom'
        with pytest.raises(ValueError, match="Required room class 'Bathroom' is missing"):
            inspect_and_prepare_dataset(
                str(download_dir),
                str(proc_dir),
                required_classes=["Bedroom", "Bathroom"],
                min_samples_per_class=5
            )

        # Insufficient samples in Bedroom (10 < 20)
        with pytest.raises(ValueError, match="has insufficient images"):
            inspect_and_prepare_dataset(
                str(download_dir),
                str(proc_dir),
                required_classes=["Bedroom"],
                min_samples_per_class=20
            )
