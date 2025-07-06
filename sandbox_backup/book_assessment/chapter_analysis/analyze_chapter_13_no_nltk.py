import os
import json
import re
from collections import Counter

# No NLTK needed for this version

def extract_chapter_data(file_path):
    """Extract data from a chapter file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract chapter title
    title_match = re.search(r'^# (.*?):', content, re.MULTILINE)
    if title_match:
        chapter_title = title_match.group(1)
    else:
        chapter_title = "Unknown Chapter"
    
    # Extract chapter number (Hardcoded for now, adjust if needed)
    chapter_num = 13
    
    # Calculate word count using basic split
    words = content.split()
    word_count = len(words)
    
    # Extract preview (first 500 characters)
    preview = content[:500]
    
    # Check for storytelling elements
    has_storytelling = bool(re.search(r'story|narrative|experience|journey|said|told|asked|elijah|dr\. chen', content.lower()))
    
    # Check for practical application
    has_practical_application = bool(re.search(r'step|practice|exercise|implement|apply|protocol|worksheet|task|method|phase|audit|inventory|technique|script|ritual', content.lower()))
    
    # Extract potential quotes (text between quotation marks or in blockquotes)
    quotes = re.findall(r'["“]([^"”]+)["”]', content) # Handle curly quotes
    blockquotes = re.findall(r'^> \*?(.*?)\*?$', content, re.MULTILINE) # Handle blockquotes with optional italics
    potential_quotes = quotes + blockquotes
    
    # Extract top keywords (excluding common words, basic approach)
    common_words = {
        'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'for', 'it', 'with', 'as', 'on', 'by', 'this', 'be', 'are', 'or', 'an', 'from', 'at', 
        'your', 'you', 'not', 'but', 'what', 'all', 'when', 'how', 'can', 'will', 'more', 'about', 'which', 'their', 'they', 'them', 'there', 
        'than', 'been', 'has', 'have', 'had', 'would', 'could', 'should', 'was', 'were', 'who', 'whom', 'whose', 'where', 'why', 
        'one', 'two', 'three', 'first', 'second', 'third', 'day', 'days', 'dr', 'chen', 'elijah', 'his', 'her', 'he', 'she', 'i', 'me', 'my', 
        'we', 'us', 'our', 'if', 'so', 'just', 'like', 'up', 'out', 'into', 'through', 'over', 'under', 'again', 'further', 'then', 'once', 
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 
        'also', 'use', 'into', 'its', 'even', 'often', 'rather', 'within', 'via', 'may', 'make', 'get', 'do', 'go'
    }
    # Basic word extraction and lowercasing
    words_for_freq = re.findall(r'\b\w+\b', content.lower())
    words_lower = [word for word in words_for_freq if word not in common_words and len(word) > 3]
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
    """Assess SEO optimization of the chapter (NLTK-free, enhanced)"""
    seo_score = 0
    max_score = 100
    
    # Check for keyword-rich title (H1)
    title_match = re.search(r'^# (.*?):(.*)', content, re.MULTILINE)
    if title_match:
        seo_score += 10
        title_text = title_match.group(1).lower() + ' ' + title_match.group(2).lower()
        # Bonus for strong keywords in title
        if re.search(r'energy|protocol|master|vitality|reclamation', title_text):
             seo_score += 5
    else:
        title_text = ""

    # Check for proper heading structure (H2, H3)
    h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
    if h2_count > 2:
        seo_score += 10
    if h3_count > 4:
        seo_score += 5
    # Bonus for keyword presence in H2/H3
    headings = re.findall(r'^##+ (.*)', content, re.MULTILINE)
    heading_text = ' '.join(headings).lower()
    if re.search(r'energy|neuroscience|protocol|detachment|recalibration|generation|science|application|practice', heading_text):
        seo_score += 5

    # Check for keyword density (simplified, focusing on core concepts)
    words = content.lower().split()
    word_count = len(words)
    core_keywords = ['energy', 'protocol', 'stress', 'brain', 'neuroplasticity', 'detachment', 'awareness', 'recalibration', 'generation', 'resilience']
    keyword_density_score = 0
    if word_count > 0:
        for keyword in core_keywords:
            keyword_count = words.count(keyword)
            keyword_density = (keyword_count / word_count) * 100
            # Give points if density is reasonable (0.3% to 2.5%)
            if 0.3 <= keyword_density <= 2.5: 
                keyword_density_score += 2 # Award points per keyword
        seo_score += min(keyword_density_score, 15) # Cap score from density

    # Check for internal links/cross-references (Markdown format - Placeholder)
    # Assuming internal links would be added later or structure implies them
    # if re.search(r'\[[^\]]+\]\([^):]+\)', content): # Basic check for [text](link) - avoid http links
    #     seo_score += 5 # Reduced score as it's a placeholder

    # Check for external references/citations (keywords)
    if re.search(r'research|study|according to|found that|dr\.|university|institute|harvard|stanford|gottman|sapolsky|huberman|baumeister|mark|davidson|pert|sternberg', content.lower()):
        seo_score += 10
    
    # Check for bullet points or numbered lists
    if re.search(r'^\* |^\d+\. ', content, re.MULTILINE):
        seo_score += 10
    
    # Check for blockquotes
    if re.search(r'^> ', content, re.MULTILINE):
        seo_score += 10
    
    # Check for bolding/emphasis on keywords
    if re.search(r'\*\*(energy|protocol|stress|brain|neuroplasticity|detachment|awareness|recalibration|generation|resilience)\*\*', content.lower()):
        seo_score += 5

    # Check for image descriptions or references (Markdown format - Placeholder)
    # if re.search(r'!\[[^\]]*\]\([^)]+\)', content): # Basic check for ![alt](src)
    #     seo_score += 5
    
    # Check for meta description-like summary (approximate check on second paragraph length)
    paragraphs = content.split('\n\n')
    intro_summary_found = False
    if len(paragraphs) > 1:
        # Check second paragraph (often intro summary)
        if 100 <= len(paragraphs[1]) <= 200:
             intro_summary_found = True
        # Check first paragraph after first H2 (often section summary)
        h2_indices = [m.start() for m in re.finditer(r'^## ', content, re.MULTILINE)]
        if h2_indices:
            first_h2_index = h2_indices[0]
            text_after_h2 = content[first_h2_index:]
            paras_after_h2 = text_after_h2.split('\n\n')
            if len(paras_after_h2) > 1 and 100 <= len(paras_after_h2[1]) <= 200:
                intro_summary_found = True
    if intro_summary_found:
        seo_score += 5
    
    # Check for optimal content length
    if 7400 <= word_count <= 9000:
        seo_score += 10
    
    # Ensure score doesn't exceed maximum
    return min(seo_score, max_score)

def main():
    # Point to the new enhanced file
    chapter_file = '/home/ubuntu/book_assessment/chapter_enhancements/chapter_13_enhanced_v2.md'
    
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
    
    # Save chapter data for assessment with new name
    chapter_data_file = os.path.join(assessment_dir, 'chapter_13_data_v2.json')
    with open(chapter_data_file, 'w') as f:
        json.dump(chapter_data, f, indent=2)
    
    print(f"Chapter Title: {chapter_data['chapter_title']}")
    print(f"Word Count: {chapter_data['word_count']}")
    print(f"SEO Score: {seo_score}/100")
    print(f"Chapter data saved to {chapter_data_file}")

if __name__ == "__main__":
    main()

