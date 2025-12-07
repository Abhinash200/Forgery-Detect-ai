import sys
import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'frontend_streamlit'))

try:
    from model_loader import detector
except ImportError:
    class MockDetector:
        def predict(self, image):
            import random
            is_forged = random.choice([True, False])
            confidence = random.uniform(0.70, 0.99)
            return {
                "is_forged": is_forged,
                "confidence": confidence,
                "label": "Forged" if is_forged else "Authentic"
            }
    detector = MockDetector()

app = FastAPI()

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        result = detector.predict(image)
        return result
    except Exception as e:
        return {"error": str(e), "is_forged": False, "confidence": 0.0}

if __name__ == "__main__":
    print("Starting Backend API on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
