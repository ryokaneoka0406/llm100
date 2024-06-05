import streamlit as st
import os
import json
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import cv2
import torch
from transformers import AutoTokenizer, AutoModel
import ollama

def save_frames(video_path, output_folder, interval=1):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    frame_count = 0
    success = True

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while success:
        success, frame = cap.read()
        if success and frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            frame_filename = os.path.join(output_folder, f"frame_{timestamp:.2f}s.jpg")
            cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    st.write("Finished saving frames.")

def caption_from_image(image_path):
    with open(image_path, 'rb') as file:
        response = ollama.chat(
            model='llava',
            messages=[
            {
                'role': 'user',
                'content': 'What is strange about this image?',
                'images': [file.read()],
            },
            ],
        )
    return response['message']['content']

def caption_into_vector(caption, tokenizer, model):
    inputs = tokenizer(caption, return_tensors='pt', max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embeddings.tolist()

def preprocess(video_path):
    output_folder = 'movie/frames'
    model_name = "intfloat/multilingual-e5-base"
    model_path = f"model/{model_name}"
    json_output = 'image_and_caption.json'

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path)

    save_frames(video_path, output_folder)

    image_data = []
    for filename in os.listdir(output_folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(output_folder, filename)
            caption = caption_from_image(image_path)
            embedding = caption_into_vector(caption, tokenizer, model)

            image_info = {
                'image_path': image_path,
                'image_title': os.path.basename(image_path),
                'caption': caption,
                'embedding': embedding
            }
            image_data.append(image_info)

    with open(json_output, 'w', encoding='utf-8') as json_file:
        json.dump(image_data, json_file, indent=4, ensure_ascii=False)

    st.write(f"Saved data to {json_output}")

def search_scene(json_file, query):
    model_name = "intfloat/multilingual-e5-base"
    model_path = f"model/{model_name}"
    model = SentenceTransformer(model_path)

    with open(json_file, 'r') as file:
        data = json.load(file)

    query_vector = model.encode([f"query: {query}"], normalize_embeddings=True)[0]
    data_vectors = [item['embedding'] for item in data]

    similarities = []
    for vector in data_vectors:
        similarity = 1 - cosine(query_vector, vector)
        similarities.append(similarity)

    sorted_indices = np.argsort(similarities)[::-1]

    results = []
    for index in sorted_indices:
        results.append((data[index]['image_title'], similarities[index]))

    return results

# Streamlitアプリの設定
st.title('Video Scene Search App')

# 1. ユーザーの任意の動画をアップロードしてもらう
if 'video_processed' not in st.session_state:
    st.session_state['video_processed'] = False

video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if video_file is not None and not st.session_state['video_processed']:
    video_path = os.path.join("movie", video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())
    st.session_state['video_path'] = video_path
    with st.spinner("Processing video..."):
        preprocess(video_path)
    st.session_state['video_processed'] = True
    st.success("Video processed successfully! You can now submit a query.")

# 2. ユーザーにクエリを入力してもらう
query = st.text_input("Enter your search query:")

if st.button("Search"):
    if st.session_state['video_processed'] and query:
        with st.spinner("Searching scenes..."):
            results = search_scene('image_and_caption.json', query)
        st.write("Search Results:")
        for result in results:
            st.write(f"Scene: {result[0]}, Similarity: {result[1]}")
    else:
        st.error("Please upload a video and enter a query.")