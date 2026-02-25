\# SAM2 Image Segmentation Deployment



\## Description

Web application for image segmentation using Meta's SAM2 model with FastAPI backend and Streamlit frontend.



\## Project Structure

\- fast\_api.py     → FastAPI backend server

\- img2segment.py  → SAM2 segmentation logic

\- strim.py        → Streamlit frontend UI

\- sam2/           → SAM2 model files



\## Installation

pip install -r req.txt



\## Usage



\### 1. Start FastAPI server

python fast\_api.py



\### 2. Start Streamlit app

streamlit run strim.py



\## How it works

1\. Upload an image

2\. Click two points on the image

3\. SAM2 segments the selected area

4\. Download the segmented result

