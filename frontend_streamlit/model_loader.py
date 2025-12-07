import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
import logging
import timm
import numpy as np
import cv2
import base64
import io
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "efficientnet_fantasyid.pth")

logger = logging.getLogger(__name__)

class ForgeryDetectionModel:
    def __init__(self):
        self.model = None
        self.cam = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.load_model()

    def load_model(self):
        if not os.path.exists(MODEL_PATH):
            logger.warning(f"Model file not found at {MODEL_PATH}. Running in MOCK mode.")
            self.model = None
            return

        try:
            self.model = timm.create_model('efficientnet_b0', pretrained=False, num_classes=2)
            
            state_dict = torch.load(MODEL_PATH, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            target_layers = [self.model.conv_head]
            self.cam = GradCAM(model=self.model, target_layers=target_layers)
            
            logger.info("Model and GradCAM loaded successfully!")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def generate_heatmap_b64(self, image_tensor, original_image):
        try:
            grayscale_cam = self.cam(input_tensor=image_tensor, targets=None)
            grayscale_cam = grayscale_cam[0, :]
            
            img_resized = original_image.resize((224, 224))
            rgb_img = np.array(img_resized, dtype=np.float32) / 255.0
            
            visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
            visualization_pil = Image.fromarray(visualization)
            
            buffer = io.BytesIO()
            visualization_pil.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            return img_str
        except Exception as e:
            logger.error(f"GradCAM generation failed: {e}")
            return None

    def predict(self, image: Image.Image):
        if self.model is None:
            import random
            is_forged = random.choice([True, False])
            confidence = random.uniform(0.70, 0.99)
            
            try:
                img_np = np.array(image.resize((224, 224)))
                heatmap = cv2.applyColorMap(img_np, cv2.COLORMAP_JET)
                overlay = cv2.addWeighted(img_np, 0.6, heatmap, 0.4, 0)
                pil_overlay = Image.fromarray(overlay)
                buffer = io.BytesIO()
                pil_overlay.save(buffer, format="PNG")
                heatmap_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            except:
                heatmap_b64 = None

            return {
                "is_forged": is_forged,
                "confidence": confidence,
                "label": "Forged" if is_forged else "Authentic",
                "message": "Model not found. Showing MOCK result.",
                "heatmap_b64": heatmap_b64
            }

        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            forged_prob = probabilities[0][1].item()
            authentic_prob = probabilities[0][0].item()
            
            is_forged = forged_prob > authentic_prob
            confidence = forged_prob if is_forged else authentic_prob
            
        heatmap_b64 = self.generate_heatmap_b64(image_tensor, image)

        return {
            "is_forged": is_forged,
            "confidence": confidence,
            "label": "Forged" if is_forged else "Authentic",
            "details": {
                "forged_probability": forged_prob,
                "authentic_probability": authentic_prob
            },
            "heatmap_b64": heatmap_b64
        }

detector = ForgeryDetectionModel()
