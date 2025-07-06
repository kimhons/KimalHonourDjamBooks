import os
import json
import re

# Define file paths
input_file = '/home/ubuntu/book_assessment/chapter_enhancements/conclusion_enhanced_v2.md'
output_file = '/home/ubuntu/book_assessment/chapter_assessments/conclusion_final_assessment_v2.json'

# Read the content of the file
with open(input_file, 'r') as f:
    content = f.read()

# Extract chapter title
title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
chapter_title = title_match.group(1) if title_match else "Unknown Chapter"

# Get word count using wc command
import subprocess
wc_output = subprocess.check_output(['wc', '-w', input_file]).decode('utf-8')
word_count = int(wc_output.strip().split()[0])

# Analyze SEO
def analyze_seo(content, title):
    score = 0
    max_score = 100
    
    # Check if title is present and formatted properly
    if title and title != "Unknown Chapter":
        score += 10
    
    # Check for headings (## headings)
    headings = re.findall(r'^##\s+(.*?)$', content, re.MULTILINE)
    if len(headings) >= 3:
        score += 20
    elif len(headings) >= 2:
        score += 10
    
    # Check for lists
    lists = re.findall(r'^\*\s+(.*?)$', content, re.MULTILINE)
    if len(lists) >= 5:
        score += 15
    elif len(lists) >= 3:
        score += 10
    
    # Check for blockquotes
    blockquotes = re.findall(r'^>\s+(.*?)$', content, re.MULTILINE)
    if len(blockquotes) >= 2:
        score += 10
    elif len(blockquotes) >= 1:
        score += 5
    
    # Check for bold text (emphasis)
    bold_text = re.findall(r'\*\*(.*?)\*\*', content)
    if len(bold_text) >= 10:
        score += 15
    elif len(bold_text) >= 5:
        score += 10
    
    # Check for keywords related to the book's theme
    keywords = ['unbothered', 'energy', 'control', 'detachment', 'mindset', 
                'strategic', 'neuroscience', 'focus', 'freedom', 'resilience', 
                'manifesto', 'principles', 'conclusion', 'era']
    
    keyword_count = 0
    for keyword in keywords:
        keyword_count += len(re.findall(r'\b' + keyword + r'\b', content.lower()))
    
    if keyword_count >= 25:
        score += 30
    elif keyword_count >= 15:
        score += 20
    elif keyword_count >= 8:
        score += 10
    
    return min(score, max_score)  # Cap at max_score

# Analyze quality
def analyze_quality(content, title):
    score = 0
    max_score = 100
    
    # Check for comprehensive content (based on word count)
    if word_count >= 3000:
        score += 25
    elif word_count >= 2500:
        score += 20
    elif word_count >= 2000:
        score += 15
    
    # Check for structure (conclusion, summary, call to action)
    if title and len(re.findall(r'^##\s+(.*?)$', content, re.MULTILINE)) >= 3:
        score += 15
    
    # Check for synthesis of key concepts
    synthesis_terms = ['neuroscience', 'physics', 'biochemistry', 'equations', 
                       'principles', 'detachment', 'control', 'energy', 'mindset']
    synthesis_count = 0
    for term in synthesis_terms:
        synthesis_count += len(re.findall(r'\b' + term + r'\b', content.lower()))
    
    if synthesis_count >= 10:
        score += 25
    elif synthesis_count >= 6:
        score += 15
    
    # Check for call to action / forward-looking statements
    call_to_action = re.findall(r'begin|start|journey|era|commit|own it|step up', content.lower())
    if len(call_to_action) >= 5:
        score += 20
    elif len(call_to_action) >= 3:
        score += 10
    
    # Check for resonance and impact (subjective, approximated by strong language)
    impact_words = ['liberation', 'limitless', 'profound', 'transformation', 'ultimate', 
                    'magnetic', 'inevitable', 'unshakable', 'powerful']
    impact_count = 0
    for word in impact_words:
        impact_count += len(re.findall(r'\b' + word + r'\b', content.lower()))
    
    if impact_count >= 8:
        score += 15
    elif impact_count >= 4:
        score += 10
        
    # Additional check for expert citations and research references
    expert_references = re.findall(r'Dr\.|research|studies|University|Institute|Center', content)
    if len(expert_references) >= 10:
        score += 25
    elif len(expert_references) >= 5:
        score += 15

    return min(score, max_score)  # Cap at max_score

# Perform analyses
seo_score = analyze_seo(content, chapter_title)
quality_score = analyze_quality(content, chapter_title)

# Check if thresholds are met
word_count_threshold_min = 2000
word_count_threshold_max = 3000
seo_threshold = 95
quality_threshold = 98.5

meets_word_count = word_count_threshold_min <= word_count <= word_count_threshold_max
meets_seo = seo_score >= seo_threshold
meets_quality = quality_score >= quality_threshold
all_thresholds_met = meets_word_count and meets_seo and meets_quality

# Prepare results
assessment_results = {
    "chapter_title": chapter_title,
    "word_count": word_count,
    "seo_score": seo_score,
    "quality_score": quality_score,
    "meets_word_count_threshold": meets_word_count,
    "meets_seo_threshold": meets_seo,
    "meets_quality_threshold": meets_quality,
    "all_thresholds_met": all_thresholds_met
}

# Save results to file
with open(output_file, 'w') as f:
    json.dump(assessment_results, f, indent=4)

# Print results to console
print(f"Chapter Title: {chapter_title}")
print(f"Word Count: {word_count}")
print(f"SEO Score: {seo_score}/100")
print(f"Quality Score: {quality_score}/100")
print(f"Meets Word Count Threshold ({word_count_threshold_min}-{word_count_threshold_max}): {meets_word_count}")
print(f"Meets SEO Threshold (≥{seo_threshold}): {meets_seo}")
print(f"Meets Quality Threshold (≥{quality_threshold}): {meets_quality}")
print(f"All Thresholds Met: {all_thresholds_met}")
print(f"Assessment saved to {output_file}")
