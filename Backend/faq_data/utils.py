def load_and_clean_faq(filepath):
    """
    Load raw FAQ text, extract (question, answer) pairs, and return them as a list of tuples.
    """
    faqs = []
    with open(filepath, 'r', encoding='utf-8') as file:
        # Split the file into blocks separated by blank lines
        blocks = file.read().strip().split("\n\n")

        for block in blocks:
            lines = block.strip().split("\n")

            # Ensure each block has exactly 2 lines: one question and one answer
            if len(lines) == 2 and lines[0].startswith("Q:") and lines[1].startswith("A:"):
                question = lines[0].replace("Q:", "").strip()
                answer = lines[1].replace("A:", "").strip()
                faqs.append((question, answer))

    return faqs

def save_cleaned_faqs(faqs, out_file_path):
    """
    Save the cleaned (question, answer) pairs into a cleaned FAQ text file.
    """
    with open(out_file_path, 'w', encoding='utf-8') as f:
        for q, a in faqs:
            f.write(f"Q: {q}\nA: {a}\n\n")
