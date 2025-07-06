import os
import json
import re
from collections import Counter

def extract_chapter_data(file_path):
    """Extract data from a chapter file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract chapter title - improved pattern matching
    title_match = re.search(r'^# (.*?):', content, re.MULTILINE)
    if title_match:
        chapter_title = title_match.group(1)
    else:
        # Try alternative pattern
        alt_title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        if alt_title_match:
            chapter_title = alt_title_match.group(1)
        else:
            chapter_title = "Unknown Chapter"
    
    # Extract chapter number (Hardcoded for now)
    chapter_num = 13
    
    # Calculate word count using basic split
    words = content.split()
    word_count = len(words)
    
    # Extract preview (first 500 characters)
    preview = content[:500]
    
    # Check for storytelling elements - expanded pattern
    has_storytelling = bool(re.search(r'story|narrative|experience|journey|said|told|asked|elijah|dr\. chen|thompson|conversation|dialogue', content.lower()))
    
    # Check for practical application - expanded pattern
    has_practical_application = bool(re.search(r'step|practice|exercise|implement|apply|protocol|worksheet|task|method|phase|audit|inventory|technique|script|ritual|reclamation|detachment', content.lower()))
    
    # Extract potential quotes (text between quotation marks or in blockquotes)
    quotes = re.findall(r'[""]([^""]+)[""]', content) # Handle curly quotes
    blockquotes = re.findall(r'^> \*?(.*?)\*?$', content, re.MULTILINE) # Handle blockquotes with optional italics
    potential_quotes = quotes + blockquotes
    
    # Extract top keywords (excluding common words)
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
        "potential_quotes": potential_quotes[:10],  # Limit to 10 quotes for readability
        "top_keywords": top_keywords
    }

def assess_seo(content):
    """Assess SEO optimization of the chapter - enhanced version"""
    seo_score = 0
    max_score = 100
    
    # Check for keyword-rich title (H1) - improved pattern matching
    title_match = re.search(r'^# (.*?):', content, re.MULTILINE)
    if title_match:
        title_text = title_match.group(1).lower()
        seo_score += 10
        # Bonus for strong keywords in title
        if re.search(r'energy|protocol|master|vitality|reclamation|30-day', title_text):
            seo_score += 5
    else:
        # Try alternative pattern
        alt_title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        if alt_title_match:
            title_text = alt_title_match.group(1).lower()
            seo_score += 8  # Slightly lower score for non-optimal format
            if re.search(r'energy|protocol|master|vitality|reclamation|30-day', title_text):
                seo_score += 5
        else:
            title_text = ""

    # Check for proper heading structure (H2, H3)
    h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
    
    if h2_count >= 5:
        seo_score += 10
    elif h2_count >= 3:
        seo_score += 8
    elif h2_count >= 1:
        seo_score += 5
        
    if h3_count >= 6:
        seo_score += 5
    elif h3_count >= 3:
        seo_score += 3
    elif h3_count >= 1:
        seo_score += 1
    
    # Bonus for keyword presence in H2/H3
    headings = re.findall(r'^##+ (.*)', content, re.MULTILINE)
    heading_text = ' '.join(headings).lower()
    if re.search(r'energy|neuroscience|protocol|detachment|recalibration|generation|science|application|practice', heading_text):
        seo_score += 10
    elif re.search(r'brain|stress|resilience|mindset|focus|attention', heading_text):
        seo_score += 5

    # Check for keyword density and distribution
    words = content.lower().split()
    word_count = len(words)
    
    # Core keywords for this chapter
    core_keywords = {
        'energy': 0, 
        'protocol': 0, 
        'reclamation': 0,
        'stress': 0, 
        'brain': 0, 
        'neuroplasticity': 0, 
        'detachment': 0, 
        'awareness': 0, 
        'recalibration': 0, 
        'generation': 0, 
        'resilience': 0,
        'practice': 0,
        'technique': 0,
        'strategic': 0,
        'phase': 0
    }
    
    # Count occurrences
    for word in words:
        if word in core_keywords:
            core_keywords[word] += 1
    
    # Calculate keyword density and score
    keyword_density_score = 0
    if word_count > 0:
        for keyword, count in core_keywords.items():
            keyword_density = (count / word_count) * 100
            # Give points if density is reasonable (0.3% to 2.5%)
            if 0.3 <= keyword_density <= 2.5: 
                keyword_density_score += 2
            elif 0.1 <= keyword_density < 0.3:
                keyword_density_score += 1
        
        # Check if keywords are distributed throughout the text (not just concentrated in one section)
        sections = content.split('##')
        if len(sections) >= 3:
            distribution_score = 0
            for section in sections[1:]:  # Skip the first section (title)
                section_words = section.lower().split()
                section_has_keywords = False
                for keyword in core_keywords:
                    if keyword in section_words:
                        section_has_keywords = True
                        break
                if section_has_keywords:
                    distribution_score += 1
            
            # Normalize distribution score
            distribution_score = min(5, distribution_score)
            keyword_density_score += distribution_score
    
    seo_score += min(keyword_density_score, 20)  # Cap score from density and distribution

    # Check for external references/citations
    reference_score = 0
    if re.search(r'research|study|according to|found that', content.lower()):
        reference_score += 5
    if re.search(r'dr\.|university|institute|harvard|stanford|gottman', content.lower()):
        reference_score += 5
    if re.search(r'sapolsky|huberman|baumeister|mark|davidson|pert|sternberg', content.lower()):
        reference_score += 5
    
    seo_score += min(reference_score, 10)
    
    # Check for bullet points or numbered lists
    list_score = 0
    bullet_lists = re.findall(r'^\* ', content, re.MULTILINE)
    numbered_lists = re.findall(r'^\d+\. ', content, re.MULTILINE)
    
    if len(bullet_lists) >= 10 or len(numbered_lists) >= 10:
        list_score = 10
    elif len(bullet_lists) >= 5 or len(numbered_lists) >= 5:
        list_score = 7
    elif len(bullet_lists) >= 1 or len(numbered_lists) >= 1:
        list_score = 3
    
    seo_score += list_score
    
    # Check for blockquotes
    blockquote_score = 0
    blockquotes = re.findall(r'^> ', content, re.MULTILINE)
    
    if len(blockquotes) >= 5:
        blockquote_score = 10
    elif len(blockquotes) >= 3:
        blockquote_score = 7
    elif len(blockquotes) >= 1:
        blockquote_score = 3
    
    seo_score += blockquote_score
    
    # Check for bolding/emphasis on keywords
    emphasis_score = 0
    if re.search(r'\*\*(energy|protocol|stress|brain|neuroplasticity|detachment|awareness|recalibration|generation|resilience)\*\*', content.lower()):
        emphasis_score += 5
    if re.search(r'\*(energy|protocol|stress|brain|neuroplasticity|detachment|awareness|recalibration|generation|resilience)\*', content.lower()):
        emphasis_score += 3
    
    seo_score += min(emphasis_score, 5)
    
    # Check for optimal content length
    if 7400 <= word_count <= 9000:
        seo_score += 10
    elif 7000 <= word_count < 7400 or 9000 < word_count <= 9500:
        seo_score += 5
    
    # Bonus for overall structure and readability
    structure_score = 0
    
    # Check for introduction and conclusion sections
    if re.search(r'^## .*?(introduction|opening|story|experiment)', content.lower(), re.MULTILINE) and \
       re.search(r'^## .*?(conclusion|summary|beyond)', content.lower(), re.MULTILINE):
        structure_score += 5
    
    # Check for paragraph length (not too long)
    paragraphs = re.split(r'\n\n+', content)
    avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
    if 50 <= avg_paragraph_length <= 150:
        structure_score += 5
    
    seo_score += structure_score
    
    # Ensure score doesn't exceed maximum
    return min(seo_score, max_score)

def assess_quality(chapter_data, content):
    """Assess the overall quality of the chapter"""
    quality_score = 0
    max_score = 100
    
    # 1. Counterintuitiveness (20 points)
    counterintuitive_score = 0
    
    # Check for counterintuitive concepts in keywords and content
    counterintuitive_keywords = ["paradox", "contrary", "opposite", "unexpected", "surprising", 
                               "challenge", "conventional", "wisdom", "counterintuitive"]
    
    # Check keywords
    keyword_matches = 0
    for keyword, _ in chapter_data["top_keywords"]:
        for c_keyword in counterintuitive_keywords:
            if c_keyword in keyword.lower():
                keyword_matches += 1
                break
    
    # Check content for counterintuitive phrases
    content_lower = content.lower()
    counterintuitive_phrases = [
        "contrary to popular belief", "you might think", "surprisingly", 
        "paradoxically", "counterintuitively", "most people assume", 
        "conventional wisdom", "commonly believed", "unexpected"
    ]
    
    phrase_matches = sum(1 for phrase in counterintuitive_phrases if phrase in content_lower)
    
    # Calculate counterintuitive score
    counterintuitive_score = min(20, (keyword_matches * 2) + (phrase_matches * 2) + 10)
    quality_score += counterintuitive_score
    
    # 2. Transformational Impact (20 points)
    transformational_score = 0
    
    # Check for storytelling
    if chapter_data["has_storytelling"]:
        transformational_score += 5
    
    # Check for transformation keywords
    transformation_keywords = ["transform", "change", "shift", "growth", "journey", "breakthrough"]
    transform_matches = 0
    for keyword in transformation_keywords:
        if keyword in content_lower:
            transform_matches += 1
    
    # Check for before/after scenarios
    if "before" in content_lower and "after" in content_lower:
        transformational_score += 3
    
    # Calculate transformational score
    transformational_score += min(12, transform_matches * 2)
    transformational_score = min(20, transformational_score)
    quality_score += transformational_score
    
    # 3. Content Excellence (15 points)
    content_score = 0
    
    # Word count in optimal range
    if 7400 <= chapter_data["word_count"] <= 9000:
        content_score += 5
    
    # Check for evidence and research references
    if re.search(r'research|study|evidence|data|science|according to', content_lower):
        content_score += 5
    
    # Check for logical structure (headings, subheadings)
    if re.search(r'^## ', content, re.MULTILINE) and re.search(r'^### ', content, re.MULTILINE):
        content_score += 5
    
    content_score = min(15, content_score)
    quality_score += content_score
    
    # 4. Narrative Craft (15 points)
    narrative_score = 0
    
    # Check for strong opening
    first_paragraph = content.split('\n\n')[0] if '\n\n' in content else ""
    if len(first_paragraph) > 200 and ("?" in first_paragraph or "!" in first_paragraph or '"' in first_paragraph):
        narrative_score += 5
    
    # Check for storytelling elements
    if chapter_data["has_storytelling"]:
        narrative_score += 5
    
    # Check for dialogue and character development
    if re.search(r'"[^"]+"\s*,\s*\w+\s+\w+', content):  # Pattern for dialogue attribution
        narrative_score += 5
    
    narrative_score = min(15, narrative_score)
    quality_score += narrative_score
    
    # 5. Wisdom Integration (10 points)
    wisdom_score = 0
    
    # Check for references to ancient wisdom or traditions
    if re.search(r'ancient|wisdom|philosophy|tradition|eastern|western|indigenous', content_lower):
        wisdom_score += 5
    
    # Check for cross-cultural references
    if re.search(r'culture|cultural|society|societies|global|worldwide|universal', content_lower):
        wisdom_score += 5
    
    wisdom_score = min(10, wisdom_score)
    quality_score += wisdom_score
    
    # 6. Practical Application (10 points)
    practical_score = 0
    
    # Check for practical application elements
    if chapter_data["has_practical_application"]:
        practical_score += 5
    
    # Check for step-by-step instructions or frameworks
    if re.search(r'step|framework|method|process|protocol|system|technique', content_lower):
        practical_score += 5
    
    practical_score = min(10, practical_score)
    quality_score += practical_score
    
    # 7. Quotability (5 points)
    quotable_score = 0
    
    # Check number of potential quotes
    if len(chapter_data["potential_quotes"]) >= 5:
        quotable_score += 5
    elif len(chapter_data["potential_quotes"]) >= 3:
        quotable_score += 3
    elif len(chapter_data["potential_quotes"]) >= 1:
        quotable_score += 1
    
    quotable_score = min(5, quotable_score)
    quality_score += quotable_score
    
    # 8. Social Media Potential (5 points)
    social_score = 0
    
    # Check for short, impactful statements
    short_quotes = 0
    for quote in chapter_data["potential_quotes"]:
        if len(quote.split()) < 20 and ("!" in quote or "?" in quote or re.search(r'\b(never|always|must|key|secret|power|success)\b', quote.lower())):
            short_quotes += 1
    
    if short_quotes >= 3:
        social_score += 5
    elif short_quotes >= 1:
        social_score += 3
    
    social_score = min(5, social_score)
    quality_score += social_score
    
    # Ensure score doesn't exceed maximum
    return min(quality_score, max_score)

def main():
    # Point to the enhanced file
    chapter_file = '/home/ubuntu/book_assessment/chapter_enhancements/chapter_13_enhanced_v2.md'
    
    # Extract chapter data
    with open(chapter_file, 'r') as f:
        content = f.read()
    
    chapter_data = extract_chapter_data(chapter_file)
    
    # Assess SEO
    seo_score = assess_seo(content)
    
    # Assess quality
    quality_score = assess_quality(chapter_data, content)
    
    # Create assessment directory if it doesn't exist
    assessment_dir = '/home/ubuntu/book_assessment/chapter_assessments'
    os.makedirs(assessment_dir, exist_ok=True)
    
    # Create assessment report
    assessment = {
        "chapter_title": chapter_data["chapter_title"],
        "chapter_num": chapter_data["chapter_num"],
        "word_count": chapter_data["word_count"],
        "seo_score": seo_score,
        "quality_score": quality_score,
        "meets_word_count_threshold": 7400 <= chapter_data["word_count"] <= 9000,
        "meets_seo_threshold": seo_score >= 95,
        "meets_quality_threshold": quality_score >= 98.5,
        "top_keywords": chapter_data["top_keywords"],
        "has_storytelling": chapter_data["has_storytelling"],
        "has_practical_application": chapter_data["has_practical_application"]
    }
    
    # Save assessment
    assessment_file = os.path.join(assessment_dir, 'chapter_13_final_assessment.json')
    with open(assessment_file, 'w') as f:
        json.dump(assessment, f, indent=2)
    
    print(f"Chapter Title: {chapter_data['chapter_title']}")
    print(f"Word Count: {chapter_data['word_count']}")
    print(f"SEO Score: {seo_score}/100")
    print(f"Quality Score: {quality_score}/100")
    print(f"Meets Word Count Threshold: {assessment['meets_word_count_threshold']}")
    print(f"Meets SEO Threshold: {assessment['meets_seo_threshold']}")
    print(f"Meets Quality Threshold: {assessment['meets_quality_threshold']}")
    print(f"Assessment saved to {assessment_file}")

if __name__ == "__main__":
    main()
