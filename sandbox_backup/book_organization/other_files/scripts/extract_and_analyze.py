import os
import docx
import re
import json
from collections import Counter

def extract_text_from_docx(file_path):
    """Extract text from a docx file."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def count_words(text):
    """Count words in text."""
    return len(re.findall(r'\b\w+\b', text))

def analyze_chapter(file_path, file_name):
    """Analyze a chapter and return key metrics."""
    text = extract_text_from_docx(file_path)
    word_count = count_words(text)
    
    # Extract chapter number and title
    match = re.match(r'Chapter_(\d+)_(.+)\.docx', file_name)
    if match:
        chapter_num = match.group(1)
        chapter_title = match.group(2).replace('_', ' ')
    else:
        # Handle introduction and conclusion
        if 'Introduction' in file_name:
            chapter_num = 'Intro'
            chapter_title = 'The Power of Being Unbothered'
        elif 'Conclusion' in file_name:
            chapter_num = 'Conclusion'
            chapter_title = 'Your Unbothered Era'
        else:
            chapter_num = 'Unknown'
            chapter_title = file_name
    
    # Identify key concepts and themes
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    common_words = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'it', 'for', 
                   'you', 'with', 'on', 'as', 'are', 'be', 'this', 'your', 'by', 'an',
                   'from', 'at', 'not', 'or', 'have', 'was', 'but', 'what', 'all', 'when',
                   'we', 'they', 'can', 'will', 'their', 'has', 'more', 'if', 'about'}
    
    # Remove common words
    for word in common_words:
        if word in word_freq:
            del word_freq[word]
    
    # Get top keywords
    top_keywords = word_freq.most_common(15)
    
    # Check for quotable lines (sentences with powerful words or phrases)
    quotable_indicators = ['never', 'always', 'must', 'remember', 'imagine', 'truth', 
                          'power', 'freedom', 'success', 'transform', 'secret', 'key',
                          'essential', 'critical', 'vital', 'fundamental', 'revolutionary',
                          'breakthrough', 'discover', 'unlock', 'master', 'extraordinary']
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    potential_quotes = []
    
    for sentence in sentences:
        if len(sentence.split()) > 5 and len(sentence.split()) < 25:  # Reasonable quote length
            for indicator in quotable_indicators:
                if indicator in sentence.lower():
                    potential_quotes.append(sentence.strip())
                    break
    
    # Limit to top 5 quotes
    potential_quotes = potential_quotes[:5]
    
    # Identify if chapter has practical applications
    practical_indicators = ['step', 'technique', 'method', 'practice', 'exercise', 'action',
                           'implement', 'apply', 'try', 'do', 'create', 'build', 'develop',
                           'establish', 'start', 'begin', 'follow', 'use', 'utilize']
    
    has_practical_application = any(indicator in text.lower() for indicator in practical_indicators)
    
    # Check for storytelling elements
    story_indicators = ['story', 'example', 'case', 'experience', 'journey', 'client',
                       'person', 'individual', 'situation', 'scenario', 'instance']
    
    has_storytelling = any(indicator in text.lower() for indicator in story_indicators)
    
    # Save first 500 characters as preview
    preview = text[:500].replace('\n', ' ').strip() + '...'
    
    return {
        'chapter_num': chapter_num,
        'chapter_title': chapter_title,
        'word_count': word_count,
        'top_keywords': top_keywords,
        'potential_quotes': potential_quotes,
        'has_practical_application': has_practical_application,
        'has_storytelling': has_storytelling,
        'preview': preview,
        'file_path': file_path
    }

def main():
    book_dir = '/home/ubuntu/book_assessment/final_book_package/'
    output_dir = '/home/ubuntu/book_assessment/chapter_analysis/'
    
    # Get all docx files
    files = [f for f in os.listdir(book_dir) if f.endswith('.docx')]
    
    # Sort files to ensure proper order
    def sort_key(filename):
        if 'Introduction' in filename:
            return 0
        elif 'Conclusion' in filename:
            return 999
        else:
            match = re.search(r'Chapter_(\d+)', filename)
            if match:
                return int(match.group(1))
            return 500
    
    files.sort(key=sort_key)
    
    # Analyze each chapter
    all_chapters = []
    total_word_count = 0
    
    for file in files:
        file_path = os.path.join(book_dir, file)
        analysis = analyze_chapter(file_path, file)
        all_chapters.append(analysis)
        total_word_count += analysis['word_count']
        
        # Save individual chapter analysis
        chapter_output = os.path.join(output_dir, f"analysis_{file.replace('.docx', '.json')}")
        with open(chapter_output, 'w') as f:
            json.dump(analysis, f, indent=2)
    
    # Save summary of all chapters
    summary = {
        'book_title': 'Why Caring Less Makes You Unstoppable',
        'total_chapters': len(files) - 2,  # Excluding intro and conclusion
        'total_word_count': total_word_count,
        'average_chapter_length': total_word_count / (len(files) - 2) if len(files) > 2 else 0,
        'chapters': all_chapters
    }
    
    with open(os.path.join(output_dir, 'book_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Analysis complete. Analyzed {len(files)} files with total word count of {total_word_count}.")

if __name__ == "__main__":
    main()
