from flask import Flask, request, render_template, session
from pymongo import MongoClient
import datetime
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# App setup
app = Flask(__name__)
app.secret_key = 'super-secret-key'

# MongoDB for logging
client = MongoClient("mongodb://localhost:27017/")
db = client['chatbot_logs']
logs = db['conversations']

# Load FAISS index and answers
faiss_index = faiss.read_index("/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/embeddings/faiss_index.index")
with open("/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/embeddings/answers.pkl", "rb") as f:
    answers = pickle.load(f)

# Load the embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini
genai.configure(api_key="your-gemini-api-key")
gemini_model = genai.GenerativeModel("gemini-pro")

def search_faq(user_query):
    """Search FAISS index and return best matched answer."""
    embedding = embedder.encode([user_query])
    D, I = faiss_index.search(np.array(embedding), k=1)
    top_score = D[0][0]
    best_answer = answers[I[0][0]]

    return top_score, best_answer

@app.route("/", methods=["GET", "POST"])
def chat():
    response = None

    if request.method == "POST":
        user_query = request.form["query"]

        # Store chat session in Flask session
        history = session.get("history", [])
        history.append({"user": user_query})
        session["history"] = history

        # Search for an answer
        score, answer = search_faq(user_query)

        # Optional: Gemini-enhanced response
        prompt = f"User asked: {user_query}\nAnswer based on policy: {answer}"
        gemini_response = gemini_model.generate_content(prompt).text

        # Save to MongoDB
        logs.insert_one({
            "timestamp": datetime.datetime.now(),
            "query": user_query,
            "answer": answer,
            "enhanced_response": gemini_response,
            "score": float(score)
        })

        response = gemini_response

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)