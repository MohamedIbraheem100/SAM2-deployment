import torch
import torchvision
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
import cv2

image_path = input("Enter image path: ")



# input_point = np.array([[400,800]])
# input_label = np.array([1])
x= input('x corrdinate')
y= input('y corrdinate')
input_point = [int(x),int(y)]


def img2segmnt(source_image , input_point ):
    
    source_image = Image.open(image_path)
    source_image = np.array(source_image.convert("RGB")) 
    
       
    sam2_checkpoint = "D:\\NTI\\git task\\SAM2-deployment\\sam2.1_hiera_large.pt"
    model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
    sam2_model = build_sam2(model_cfg, sam2_checkpoint , device='cpu')
    predictor = SAM2ImagePredictor(sam2_model)
    predictor.set_image(source_image)
    
    input_point = np.array([input_point])
    input_label = np.array([1])
    
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    
    best_mask_index = np.argmax(scores)
    mask_input = logits[best_mask_index]

    # masks, scores, _ = predictor.predict(
    # point_coords=input_point,
    # point_labels=input_label,
    # mask_input=mask_input[None, :, :],
    # multimask_output=False,
    # )
    
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    alpha = (masks[1] * 255).astype(np.uint8)

    rgba = np.dstack([image, alpha])
    imagePNG=cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)  
    cv2.imwrite("segmented2.png", imagePNG)
    
    
    return imagePNG  
  
img2segmnt(image_path , input_point )