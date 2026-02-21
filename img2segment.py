import torch
import torchvision
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
import cv2
import os




def img2segmnt(source_image , input_point ):
        
    # sam2_checkpoint = "sam2/checkpoints/sam2.1_hiera_large.pt"
    # model_cfg = "sam2\sam2\sam2_hiera_l.yaml"
    

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    sam2_checkpoint = "sam2.1_hiera_large.pt"
    model_cfg = "sam2\configs\sam2.1\sam2.1_hiera_l.yaml"

    
    sam2_model = build_sam2(model_cfg, sam2_checkpoint ,device='cpu')
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
    alpha = (masks[best_mask_index] * 255).astype(np.uint8)


    

    rgba = np.dstack([source_image, alpha])
    imagePNG=cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)  
    
    
    
    return imagePNG  
  
# img2segmnt(source_image , input_point )