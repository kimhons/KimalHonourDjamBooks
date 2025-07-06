import docx
import os

def get_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

chapter_file = "/home/ubuntu/book_assessment/final_book_package/Chapter_12_The_Unattachment_Mindset.docx"
output_file = "/home/ubuntu/book_assessment/chapter_enhancements/chapter_12_original_text.md"

if os.path.exists(chapter_file):
    try:
        text_content = get_text(chapter_file)
        # Basic Markdown conversion (replace multiple newlines with double newline for paragraphs)
        markdown_content = text_content.replace('\n\n', '\n').replace('\n', '\n\n')
        
        with open(output_file, "w") as f:
            f.write(f"# Original Text: Chapter 12 - The Resilience Factor\n\n")
            f.write(markdown_content)
        print(f"Successfully extracted text from {chapter_file} to {output_file}")
    except Exception as e:
        print(f"Error processing {chapter_file}: {e}")
else:
    print(f"Error: File not found - {chapter_file}")

