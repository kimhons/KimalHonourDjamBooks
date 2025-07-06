import docx
import os

def get_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

chapter_file = "/home/ubuntu/book_assessment/final_book_package/Chapter_11_The_Null_Value_Principle.docx"
output_file = "/home/ubuntu/book_assessment/chapter_enhancements/chapter_11_original_text.md"

if os.path.exists(chapter_file):
    try:
        text = get_text(chapter_file)
        with open(output_file, "w") as f:
            f.write(f"# Original Text: Chapter 11 - The Null Value Principle\n\n")
            f.write(text)
        print(f"Successfully extracted text from {chapter_file} to {output_file}")
    except Exception as e:
        print(f"Error processing {chapter_file}: {e}")
else:
    print(f"Error: File not found - {chapter_file}")

