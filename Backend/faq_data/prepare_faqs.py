from utils import load_and_clean_faq, save_cleaned_faqs

raw_path = "/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/faq_data/raw_faqs.txt"
cleaned_path = "/Users/hephaestus/Documents/AI/AI-Assignment-103/Backend/faq_data/cleaned_faqs.txt"

faqs = load_and_clean_faq(raw_path)
save_cleaned_faqs(faqs, cleaned_path)
print(f"✔ Cleaned and saved {len(faqs)} FAQs.")
