import torch
import numpy as np
from backend.app.ml.model import build_model
from backend.app.ml.transforms import get_train_transforms, get_eval_transforms
from backend.app.ml.evaluate import evaluate_model_on_loader
from backend.app.ml.dataset import RoomImageDataset
from torch.utils.data import DataLoader

def test_model_architecture():
    model = build_model(num_classes=7, pretrained=False)
    assert model is not None
    # Test forward pass with synthetic batch (B=2, C=3, H=224, W=224)
    dummy_input = torch.randn(2, 3, 224, 224)
    output = model(dummy_input)
    assert output.shape == (2, 7)

def test_transforms_output_shape():
    eval_transform = get_eval_transforms()
    from PIL import Image
    test_img = Image.new("RGB", (400, 300), color=(100, 150, 200))
    tensor = eval_transform(test_img)
    assert tensor.shape == (3, 224, 224)
    assert tensor.dtype == torch.float32

def test_evaluation_metric_computation():
    # Model evaluation on synthetic loader
    model = build_model(num_classes=7, pretrained=False)
    # Create 4 synthetic samples
    samples = []
    dataset = RoomImageDataset([], transform=None)
    # Manually pass tensors
    class DummyDataset(torch.utils.data.Dataset):
        def __len__(self): return 4
        def __getitem__(self, idx):
            return torch.randn(3, 224, 224), idx % 7
            
    loader = DataLoader(DummyDataset(), batch_size=2)
    metrics = evaluate_model_on_loader(model, loader, ["C0", "C1", "C2", "C3", "C4", "C5", "C6"])
    assert "accuracy" in metrics
    assert "macro_f1" in metrics
    assert "confusion_matrix" in metrics
    assert len(metrics["confusion_matrix"]) == 7
