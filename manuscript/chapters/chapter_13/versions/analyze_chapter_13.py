import os
import json
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

def extract_chapter_data(file_path):
    """Extract data from a chapter file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract chapter title
    title_match = re.search(r'# (.*?):', content)
    if title_match:
        chapter_title = title_match.group(1)
    else:
        chapter_title = "Unknown Chapter"
    
    # Extract chapter number
    chapter_num = 13
    
    # Calculate word count
    words = word_tokenize(content)
    word_count = len(words)
    
    # Extract preview (first 500 characters)
    preview = content[:500]
    
    # Check for storytelling elements
    has_storytelling = bool(re.search(r'story|narrative|experience|journey', content.lower()))
    
    # Check for practical application
    has_practical_application = bool(re.search(r'step|practice|exercise|implement|apply', content.lower()))
    
    # Extract potential quotes (text between quotation marks or in blockquotes)
    quotes = re.findall(r'[""]([^""]+)["""]', content)
    blockquotes = re.findall(r'> *(.*?)\n', content)
    potential_quotes = quotes + blockquotes
    
    # Extract top keywords (excluding common words)
    common_words = {'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'for', 'it', 'with', 'as', 'on', 'by', 'this', 'be', 'are', 'or', 'an', 'from', 'at', 'your', 'you', 'not', 'but', 'what', 'all', 'when', 'how', 'can', 'will', 'more', 'about', 'which', 'their', 'they', 'them', 'there', 'than', 'been', 'has', 'have', 'had', 'would', 'could', 'should', 'was', 'were', 'who', 'whom', 'whose', 'where', 'why', 'one', 'two', 'three', 'first', 'second', 'third'}
    words_lower = [word.lower() for word in words if word.isalpha() and word.lower() not in common_words]
    word_freq = Counter(words_lower)
    top_keywords = word_freq.most_common(10)
    
    return {
        "chapter_title": chapter_title,
        "chapter_num": chapter_num,
        "word_count": word_count,
        "preview": preview,
        "has_storytelling": has_storytelling,
        "has_practical_application": has_practical_application,
        "potential_quotes": potential_quotes,
        "top_keywords": top_keywords
    }

def assess_seo(content):
    """Assess SEO optimization of the chapter"""
    seo_score = 0
    max_score = 100
    
    # Check for keyword-rich title
    if re.search(r'# .*?:.*', content):
        seo_score += 10
    
    # Check for proper heading structure (H1, H2, H3)
    if re.search(r'# ', content):
        seo_score += 10
    if re.search(r'## ', content):
        seo_score += 10
    if re.search(r'### ', content):
        seo_score += 5
    
    # Check for keyword density
    words = word_tokenize(content.lower())
    word_count = len(words)
    
    # Extract potential keywords from title
    title_match = re.search(r'# (.*?):', content)
    if title_match:
        title = title_match.group(1).lower()
        title_words = word_tokenize(title)
        title_keywords = [word for word in title_words if word.isalpha() and len(word) > 3]
        
        # Check keyword density for title keywords
        for keyword in title_keywords:
            keyword_count = words.count(keyword)
            keyword_density = (keyword_count / word_count) * 100
            if 0.5 <= keyword_density <= 2.5:
                seo_score += 5
    
    # Check for internal links/cross-references
    if re.search(r'\[.*?\]\(.*?\)', content):
        seo_score += 10
    
    # Check for external references
    if re.search(r'research|study|according to|found that', content.lower()):
        seo_score += 10
    
    # Check for bullet points or numbered lists
    if re.search(r'\* |1\. |2\. |3\. ', content):
        seo_score += 10
    
    # Check for blockquotes
    if re.search(r'> ', content):
        seo_score += 10
    
    # Check for image descriptions or references
    if re.search(r'!\[.*?\]\(.*?\)', content):
        seo_score += 5
    
    # Check for meta description-like summary
    paragraphs = content.split('\n\n')
    if len(paragraphs) > 1 and 100 <= len(paragraphs[1]) <= 160:
        seo_score += 5
    
    # Check for optimal content length
    if word_count >= 7400 and word_count <= 9000:
        seo_score += 10
    
    # Ensure score doesn't exceed maximum
    return min(seo_score, max_score)

def main():
    chapter_file = '/home/ubuntu/book_assessment/chapter_enhancements/chapter_13_enhanced.md'
    
    # Extract chapter data
    chapter_data = extract_chapter_data(chapter_file)
    
    # Read content for SEO assessment
    with open(chapter_file, 'r') as f:
        content = f.read()
    
    # Assess SEO
    seo_score = assess_seo(content)
    
    # Create assessment directory if it doesn't exist
    assessment_dir = '/home/ubuntu/book_assessment/chapter_assessments'
    os.makedirs(assessment_dir, exist_ok=True)
    
    # Save chapter data for assessment
    chapter_data_file = os.path.join(assessment_dir, 'chapter_13_data.json')
    with open(chapter_data_file, 'w') as f:
        json.dump(chapter_data, f, indent=2)
    
    print(f"Chapter Title: {chapter_data['chapter_title']}")
    print(f"Word Count: {chapter_data['word_count']}")
    print(f"SEO Score: {seo_score}/100")
    print(f"Chapter data saved to {chapter_data_file}")
    
    # Return data for further processing
    return {
        "chapter_data": chapter_data,
        "seo_score": seo_score
    }

if __name__ == "__main__":
    main()
