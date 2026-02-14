import base64
import io
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import uvicorn

# 1. تعريف شكل البيانات (Base64 + Coordinates)
class SegmentRequest(BaseModel):
    image_base64: str
    x: int
    y: int

app = FastAPI(title="SAM2_api")

@app.post("/segment")
async def segment_image(request: SegmentRequest):
    try:
        encoded_data = request.image_base64.split(",")[-1]
        image_data = base64.b64decode(encoded_data)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        
        width, height = image.size
        if request.x >= width or request.y >= height:
            raise HTTPException(status_code=422, detail=f"Coordinates out of bounds. Image size: {width}x{height}")

        # pixels = image.load()
        # pixels[request.x, request.y] = (255, 0, 0) 

        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        encoded_result = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

        return {
            "status": "success",
            "segmented_image": encoded_result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)