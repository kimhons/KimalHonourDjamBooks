import docx
import os

def get_text(filename):
    try:
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

chapter_file = "/home/ubuntu/book_assessment/final_book_package/Chapter_8_The_Power_of_Selective_Ignorance.docx"
chapter_text = get_text(chapter_file)

if chapter_text:
    # Save the extracted text to a temporary file for easier handling
    output_file = "/home/ubuntu/book_assessment/chapter_enhancements/chapter_8_original_text.md"
    try:
        with open(output_file, "w") as f:
            f.write(chapter_text)
        print(f"Extracted text from {chapter_file} to {output_file}")
        
        # Also get word count
        word_count = len(chapter_text.split())
        print(f"Original word count for Chapter 8: {word_count}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
else:
    print(f"Failed to extract text from {chapter_file}")

