import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.ml.model import build_model
from backend.app.ml.transforms import get_eval_transforms

DEFAULT_SIX_CLASSES: List[str] = [
    "Bedroom",
    "LivingRoom",
    "Kitchen",
    "DiningRoom",
    "Bathroom",
    "HomeOffice"
]

class InferenceService:
    _instance = None

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.current_model: Optional[torch.nn.Module] = None
        self.loaded_version: Optional[str] = None
        self.is_trained: bool = False
        self.transform = get_eval_transforms()
        self.classes: List[str] = getattr(settings, "TARGET_ROOM_CLASSES", DEFAULT_SIX_CLASSES)
        
    @classmethod
    def get_instance(cls) -> "InferenceService":
        if cls._instance is None:
            cls._instance = InferenceService()
        return cls._instance

    def load_model(self, version_tag: Optional[str] = None) -> bool:
        """
        Loads the specified or active model version weights.
        Returns True if a trained checkpoint was loaded, False if not found.
        """
        target_version = version_tag or settings.ACTIVE_MODEL_VERSION
        weights_file = Path(settings.MODEL_ARTIFACT_DIR) / f"model_{target_version}.pth"
        metadata_file = Path(settings.MODEL_ARTIFACT_DIR) / f"model_{target_version}.json"
        
        if not weights_file.exists():
            logger.warning(
                f"Trained model weights not found at {weights_file}. "
                "Operating in honest Demo Fallback mode until a model is trained."
            )
            self.current_model = None
            self.loaded_version = target_version
            self.is_trained = False
            return False
            
        try:
            # Check metadata if available to verify class ordering
            classes = list(getattr(settings, "TARGET_ROOM_CLASSES", DEFAULT_SIX_CLASSES))
            if metadata_file.exists():
                try:
                    with open(metadata_file, "r") as f:
                        meta = json.load(f)
                    meta_classes = meta.get("classes", [])
                    if meta_classes:
                        valid_meta = [c for c in meta_classes if c != "Other"]
                        if len(valid_meta) == 6:
                            classes = valid_meta
                except Exception as meta_err:
                    logger.warning(f"Metadata verification notice for {target_version}: {meta_err}")

            self.classes = classes
            num_classes = len(self.classes)
            model = build_model(num_classes=num_classes, pretrained=False)
            state_dict = torch.load(str(weights_file), map_location=self.device)

            # Adapt checkpoint classifier head if checkpoint contains 7 classes (including Other)
            clf_weight_key = "backbone.classifier.3.weight"
            clf_bias_key = "backbone.classifier.3.bias"
            if clf_weight_key in state_dict and state_dict[clf_weight_key].shape[0] != num_classes:
                if state_dict[clf_weight_key].shape[0] == 7 and num_classes == 6:
                    state_dict = state_dict.copy()
                    state_dict[clf_weight_key] = state_dict[clf_weight_key][:6]
                    state_dict[clf_bias_key] = state_dict[clf_bias_key][:6]

            model.load_state_dict(state_dict)
            model.to(self.device)
            model.eval()
            
            self.current_model = model
            self.loaded_version = target_version
            self.is_trained = True
            logger.info(
                f"Loaded trained model version '{target_version}' ({num_classes} classes: {', '.join(self.classes)}) on {self.device}."
            )
            return True
        except Exception as e:
            logger.error(f"Failed to load model weights for {target_version}: {e}")
            self.current_model = None
            self.is_trained = False
            return False

    def predict(self, image_input: Image.Image) -> Dict[str, Any]:
        """
        Runs CPU inference on a PIL Image with MobileNetV3-Small.
        Uses torch.inference_mode() and ImageNet evaluation transforms.
        Returns predicted room, confidence, finite 6-class probabilities, and latency.
        """
        start_time = time.time()
        
        # Check if model needs initial loading
        if self.current_model is None and not self.is_trained and self.loaded_version is None:
            self.load_model()
            
        # If trained model is available:
        if self.current_model is not None and self.is_trained:
            try:
                rgb_img = image_input.convert("RGB")
                tensor = self.transform(rgb_img).unsqueeze(0).to(self.device)
                
                with torch.inference_mode():
                    logits = self.current_model(tensor)
                    probs_tensor = F.softmax(logits, dim=1)[0]
                    probs = probs_tensor.cpu().numpy()
                    
                # Ensure finite, well-behaved probabilities summing to 1.0
                probs = np.nan_to_num(probs, nan=0.0, posinf=1.0, neginf=0.0)
                prob_sum = float(probs.sum())
                if prob_sum > 0:
                    probs = probs / prob_sum

                probabilities: Dict[str, float] = {
                    cls: round(float(probs[idx]), 4)
                    for idx, cls in enumerate(self.classes)
                }

                top_idx = int(probs.argmax())
                predicted_room = self.classes[top_idx]
                confidence = round(float(probs[top_idx]), 4)

                top_indices = probs.argsort()[::-1]
                top_preds = [
                    {"class_name": self.classes[idx], "confidence": round(float(probs[idx]), 4)}
                    for idx in top_indices[:3]
                ]
                
                latency_ms = round((time.time() - start_time) * 1000, 2)
                logger.info(
                    f"Inference completed: version={self.loaded_version}, predicted={predicted_room}, "
                    f"confidence={confidence:.4f}, latency={latency_ms}ms"
                )

                return {
                    "model_version": self.loaded_version or settings.ACTIVE_MODEL_VERSION,
                    "predicted_room": predicted_room,
                    "predicted_room_type": predicted_room,
                    "confidence": confidence,
                    "probabilities": probabilities,
                    "top_predictions": top_preds,
                    "is_demo_fallback": False,
                    "latency_ms": latency_ms
                }
            except Exception as e:
                logger.error(f"Inference error with trained model: {e}")
                
        # Honest Demo Fallback:
        # Analyzes basic image composition/aspect ratio and returns a labeled fallback
        w, h = image_input.size
        aspect = w / max(1, h)
        if aspect > 1.3:
            primary_guess = "LivingRoom"
            second_guess = "DiningRoom"
            third_guess = "Bedroom"
        elif aspect < 0.9:
            primary_guess = "Bathroom"
            second_guess = "HomeOffice"
            third_guess = "Kitchen"
        else:
            primary_guess = "Bedroom"
            second_guess = "LivingRoom"
            third_guess = "HomeOffice"
            
        latency_ms = round((time.time() - start_time) * 1000, 2)
        fallback_probs: Dict[str, float] = {cls: 0.05 for cls in self.classes}
        fallback_probs[primary_guess] = 0.65
        fallback_probs[second_guess] = 0.20
        tot = sum(fallback_probs.values())
        fallback_probs = {k: round(v / tot, 4) for k, v in fallback_probs.items()}

        return {
            "model_version": f"{self.loaded_version or settings.ACTIVE_MODEL_VERSION}-demo-fallback",
            "predicted_room": primary_guess,
            "predicted_room_type": primary_guess,
            "confidence": 0.65,
            "probabilities": fallback_probs,
            "top_predictions": [
                {"class_name": primary_guess, "confidence": 0.65},
                {"class_name": second_guess, "confidence": 0.20},
                {"class_name": third_guess, "confidence": 0.15}
            ],
            "is_demo_fallback": True,
            "latency_ms": latency_ms
        }
