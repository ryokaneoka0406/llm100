import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import cv2
from PIL import Image

import time
import os

import streamlit as st
import cv2
import google.generativeai as genai
from PIL import Image
import numpy as np
import time

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Initialize Google Generative AI model
gemini_pro_vision = genai.GenerativeModel("gemini-1.5-flash-latest")

def capture_image(cap):
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture image from camera")
        return None
    return frame

def send_image_to_google(image):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    response = gemini_pro_vision.generate_content([pil_image])
    return response.text

def main():
    st.title("Gemini Flash Capture Demo")

    run = st.checkbox('Run Camera')
    capture_interval = 2 # Capture interval in seconds

    if run:
        # Open the camera
        cap = cv2.VideoCapture(0)

        while run:
            frame = capture_image(cap)
            if frame is not None:
                # Display the captured frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, channels="RGB")

                # Send the frame to Google AI
                summary = send_image_to_google(frame)
                st.write(summary)

            # Wait for the next capture
            time.sleep(capture_interval)

        # Release the camera
        cap.release()

if __name__ == "__main__":
    main()
