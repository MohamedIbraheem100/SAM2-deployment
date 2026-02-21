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
# class SegmentRequest(BaseModel):
#     image_base64: str
#     x: int
#     y: int
class SegmentRequest(BaseModel):
    image_base64: str
    points: list  # [[x1, y1], [x2, y2]]
    
app = FastAPI(title="SAM2_api")

@app.post("/segment")
async def segment_image(request: SegmentRequest):
    try:
        #  debug:
        print("Received points:", request.points)
        print("Length of Base64 string:", len(request.image_base64))
        
        encoded_data = request.image_base64.split(",")[-1]
        image_data = base64.b64decode(encoded_data)
        
        
       
        
        image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")
        source_image_np = np.array(image_pil)
        
         
        results = []
        for point in request.points:
            segmented_np = img2segmnt(source_image_np, point)
            segmented_rgba = cv2.cvtColor(segmented_np, cv2.COLOR_BGRA2RGBA)
            final_image = Image.fromarray(segmented_rgba)  
             
        img_bytes = io.BytesIO()
        final_image.save(img_bytes, format="PNG")
        encoded_result = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        results.append(encoded_result)
        
        

        return {
            "status": "success",
            "segmented_image": results
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8010)