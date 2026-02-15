import base64
import io
import cv2
import os
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import uvicorn
from img2segment import img2segmnt

# (Base64 + Coordinates)
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
        # image = Image.open(io.BytesIO(image_data)).convert("RGB")
        temp_filename = "temp_input.png"
        
        with open(temp_filename, "wb") as f:
            f.write(image_data)
        
        # width, height = image.size
        # if request.x >= width or request.y >= height:
        #     raise HTTPException(status_code=422, detail=f"Coordinates out of bounds. Image size: {width}x{height}")
        
        image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")
        source_image_np = np.array(image_pil)
        
        input_point = [request.x, request.y]

        # pixels = image.load()
        # pixels[request.x, request.y] = (255, 0, 0) 
        segmented_np = img2segmnt(source_image_np, input_point)
        
        segmented_rgba = cv2.cvtColor(segmented_np, cv2.COLOR_BGRA_RGBA)
        final_image = Image.fromarray(segmented_rgba)   
             
        img_bytes = io.BytesIO()
        final_image.save(img_bytes, format="PNG")
        encoded_result = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return {
            "status": "success",
            "segmented_image": encoded_result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)