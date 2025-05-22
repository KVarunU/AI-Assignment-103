from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

def load_cleaned_faqs(filepath):
    questions = []
    answers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        blocks = f.read().strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) == 2:
                q = lines[0].replace("Q:", "").strip()
                a = lines[1].replace("A:", "").strip()
                questions.append(q)
                answers.append(a)
    return questions, answers

def generate_and_store_embeddings(cleaned_faq_path, index_path, answers_path):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    questions, answers = load_cleaned_faqs(cleaned_faq_path)

    print(f"📌 Generating embeddings for {len(questions)} questions...")
    embeddings = model.encode(questions)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    # Save FAISS index
    faiss.write_index(index, index_path)
    print(f"✅ FAISS index saved to {index_path}")

    # Save answers list
    with open(answers_path, 'wb') as f:
        pickle.dump(answers, f)
    print(f"✅ Answers saved to {answers_path}")

if __name__ == "__main__":
    cleaned_faq_path = "/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/faq_data/cleaned_faqs.txt"
    index_path = "/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/embeddings/faiss_index.index"
    answers_path = "/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/embeddings/answers.pkl"

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    generate_and_store_embeddings(cleaned_faq_path, index_path, answers_path)