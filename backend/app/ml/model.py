import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

class RoomClassifier(nn.Module):
    """
    Transfer learning model based on MobileNetV3-Small.
    Replaces the default 1000-class classifier head with a dropout-regularized
    custom head tailored for interior room categories.
    """
    def __init__(self, num_classes: int = 7, pretrained: bool = True, freeze_backbone: bool = False):
        super(RoomClassifier, self).__init__()
        
        weights = MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        self.backbone = mobilenet_v3_small(weights=weights)
        
        if freeze_backbone:
            for param in self.backbone.features.parameters():
                param.requires_grad = False
                
        # MobileNetV3-Small last classifier layer input features is 1024
        in_features = self.backbone.classifier[0].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Linear(in_features, 1024),
            nn.Hardswish(inplace=True),
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(1024, num_classes)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

def build_model(num_classes: int = 7, pretrained: bool = True) -> RoomClassifier:
    return RoomClassifier(num_classes=num_classes, pretrained=pretrained)
