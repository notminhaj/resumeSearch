import os
import faiss
import numpy as np
import requests
from flask import Flask, request, render_template, send_from_directory
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Set up Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize models
embedder = SentenceTransformer('all-mpnet-base-v2')  # Switched to all-mpnet-base-v2 for better embeddings

# Initialize FAISS index
dimension = 768  # Adjusted for all-mpnet-base-v2 embedding size
faiss_index = faiss.IndexFlatL2(dimension)
metadata = []  # Store candidate info

# Mistral API Key
MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"
MODEL_NAME = "mistral-medium"  # Recommended model

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

# Function to get reasoning from Mistral API
def get_mistral_reasoning(job_description, resume_text):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    
    prompt = (f"Job description: {job_description}\n"
              f"Resume: {resume_text[:4000]}\n"
              "Briefly summarize why this candidate is a good match for the role.")
    
    response = requests.post(
        url, headers=headers,
        json={
            "model": MODEL_NAME,  # Using mistral-medium
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        }
    )
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return f"Error: {response.status_code}, {response.text}"
    
    json_response = response.json()
    if "choices" not in json_response:
        print("Unexpected API response:", json_response)
        return "Error: Unexpected API response"

    return json_response["choices"][0]["message"]["content"]

# Function to rank candidates using an LLM
def rank_candidates(job_description, candidates):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    
    prompt = f"Given the following job description:\n{job_description}\n\nRank the candidates from best to worst based on how well they fit the role.\n\nCandidates:\n"
    for i, candidate in enumerate(candidates):
        prompt += f"{i+1}. Name: {candidate['name']}\nExplanation: {candidate['explanation']}\n\n"
    
    response = requests.post(
        url, headers=headers,
        json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }
    )
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return candidates  # Return the original list if ranking fails
    
    json_response = response.json()
    if "choices" not in json_response:
        print("Unexpected API response:", json_response)
        return candidates  # Return the original list if ranking fails
    
    ranked_text = json_response["choices"][0]["message"]["content"].split("\n")
    ranked_candidates = []
    for line in ranked_text:
        for candidate in candidates:
            if candidate['name'] in line:
                ranked_candidates.append(candidate)
                break
    
    return ranked_candidates if ranked_candidates else candidates  # Return ranked list or original list

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload multiple resumes endpoint
@app.route('/upload', methods=['POST'])
def upload_resumes():
    resume_files = request.files.getlist('resumes')
    if not resume_files:
        return 'No files uploaded'
    
    for resume_file in resume_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(file_path)
        resume_text = extract_text_from_pdf(file_path)
        embedding = embedder.encode(resume_text, convert_to_tensor=True).cpu().numpy()
        faiss_index.add(np.array([embedding]))
        metadata.append({'name': resume_file.filename, 'file_path': file_path})
    
    return render_template('upload_success.html')  # New template

# Search candidates endpoint
@app.route('/search', methods=['POST'])
def search_candidates():
    job_description = request.form['job_description']
    num_candidates = int(request.form.get('num_candidates', 5))  # Default to 5
    query_embedding = embedder.encode(job_description, convert_to_tensor=True).cpu().numpy()
    distances, indices = faiss_index.search(np.array([query_embedding]), 10)  # Retrieve 10 candidates first
    results = []
    for idx in indices[0]:
        if idx < len(metadata):  # Ensure valid index
            meta = metadata[idx]
            resume_text = extract_text_from_pdf(meta['file_path'])
            explanation = get_mistral_reasoning(job_description, resume_text)
            results.append({
                'name': meta['name'],
                'explanation': explanation,
                'resume_link': f'/resumes/{os.path.basename(meta["file_path"])}'
            })
    
    # Rank candidates using LLM
    ranked_results = rank_candidates(job_description, results)
    
    # Return only the requested number of candidates
    return render_template('results.html', results=ranked_results[:num_candidates])

# Serve resume files
@app.route('/resumes/<filename>')
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the app
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)