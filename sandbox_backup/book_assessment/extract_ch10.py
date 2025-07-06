import docx
import os

def get_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# Define file paths
input_docx = "/home/ubuntu/book_assessment/final_book_package/Chapter_10_The_Resilience_Factor.docx"
output_md = "/home/ubuntu/book_assessment/chapter_enhancements/chapter_10_original_text.md"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_md), exist_ok=True)

# Extract text and save to markdown file
text_content = get_text(input_docx)
with open(output_md, "w") as f:
    f.write(text_content)

print(f"Extracted text from {input_docx} to {output_md}")
