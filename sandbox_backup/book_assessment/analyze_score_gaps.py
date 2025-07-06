import json
import pandas as pd
import numpy as np

# Load the assessment summary
with open('/home/ubuntu/book_assessment/chapter_assessments/assessment_summary.json', 'r') as f:
    assessment_data = json.load(f)

# Create a dataframe to analyze the scores
chapter_scores = {}
dimensions = [
    "counterintuitiveness", 
    "transformational_impact", 
    "content_excellence", 
    "narrative_craft", 
    "wisdom_integration", 
    "practical_application", 
    "quotability", 
    "social_media_potential"
]

# Extract scores for each chapter and dimension
for chapter_num, scores in assessment_data["chapter_scores"].items():
    chapter_scores[chapter_num] = {}
    for dimension in dimensions:
        if dimension in scores:
            chapter_scores[chapter_num][dimension] = scores[dimension]["section_score"]
        else:
            chapter_scores[chapter_num][dimension] = 0

# Convert to dataframe for easier analysis
df = pd.DataFrame.from_dict(chapter_scores, orient='index')

# Calculate current normalized scores (out of 100)
# The weights for each dimension based on the assessment rubric
weights = {
    "counterintuitiveness": 0.20,
    "transformational_impact": 0.20,
    "content_excellence": 0.15,
    "narrative_craft": 0.15,
    "wisdom_integration": 0.10,
    "practical_application": 0.10,
    "quotability": 0.05,
    "social_media_potential": 0.05
}

# Calculate the maximum possible score for each dimension
max_scores = {
    "counterintuitiveness": 20,
    "transformational_impact": 20,
    "content_excellence": 15,
    "narrative_craft": 15,
    "wisdom_integration": 10,
    "practical_application": 10,
    "quotability": 5,
    "social_media_potential": 5
}

# Calculate normalized scores (out of 100)
normalized_scores = pd.DataFrame(index=df.index, columns=df.columns)
for chapter in df.index:
    for dimension in df.columns:
        normalized_scores.loc[chapter, dimension] = (df.loc[chapter, dimension] / max_scores[dimension]) * 100

# Calculate weighted scores
weighted_scores = pd.DataFrame(index=df.index, columns=df.columns)
for chapter in df.index:
    for dimension in df.columns:
        weighted_scores.loc[chapter, dimension] = normalized_scores.loc[chapter, dimension] * weights[dimension]

# Calculate total scores
total_scores = weighted_scores.sum(axis=1)

# Calculate the gap to reach 98.5
gap_to_target = 98.5 - total_scores

# Calculate the average gap per dimension (weighted by importance)
avg_gap_per_dimension = {}
for dimension in dimensions:
    # Calculate the current average score for this dimension
    current_avg = normalized_scores[dimension].mean()
    # Calculate the maximum possible improvement
    max_improvement = 100 - current_avg
    # Calculate the gap contribution needed from this dimension
    avg_gap_per_dimension[dimension] = {
        'current_avg': current_avg,
        'max_improvement': max_improvement,
        'weight': weights[dimension],
        'weighted_gap': gap_to_target.mean() * weights[dimension] / sum(weights.values()),
        'required_improvement': min(max_improvement, gap_to_target.mean() * weights[dimension] / sum(weights.values()) / weights[dimension])
    }

# Identify the dimensions that need the most improvement
dimension_improvement_priority = sorted(
    [(d, avg_gap_per_dimension[d]['required_improvement']) for d in dimensions],
    key=lambda x: x[1],
    reverse=True
)

# Calculate target scores for each chapter and dimension
target_scores = pd.DataFrame(index=df.index, columns=df.columns)
for chapter in df.index:
    for dimension in df.columns:
        current_normalized = normalized_scores.loc[chapter, dimension]
        required_improvement = min(
            100 - current_normalized,  # Can't exceed 100%
            avg_gap_per_dimension[dimension]['required_improvement']
        )
        target_scores.loc[chapter, dimension] = current_normalized + required_improvement

# Calculate the new weighted scores
new_weighted_scores = pd.DataFrame(index=df.index, columns=df.columns)
for chapter in df.index:
    for dimension in df.columns:
        new_weighted_scores.loc[chapter, dimension] = target_scores.loc[chapter, dimension] * weights[dimension]

# Calculate new total scores
new_total_scores = new_weighted_scores.sum(axis=1)

# Save the analysis results
analysis_results = {
    'current_scores': {
        'raw': df.to_dict(),
        'normalized': normalized_scores.to_dict(),
        'weighted': weighted_scores.to_dict(),
        'total': total_scores.to_dict()
    },
    'gap_analysis': {
        'gap_to_target': gap_to_target.to_dict(),
        'dimension_gaps': avg_gap_per_dimension,
        'improvement_priority': dimension_improvement_priority
    },
    'target_scores': {
        'normalized': target_scores.to_dict(),
        'weighted': new_weighted_scores.to_dict(),
        'total': new_total_scores.to_dict()
    }
}

with open('/home/ubuntu/book_assessment/score_gap_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

# Print summary of findings
print("Current Average Score: {:.1f}/100".format(total_scores.mean()))
print("Gap to Target (98.5): {:.1f}".format(gap_to_target.mean()))
print("\nDimension Improvement Priorities:")
for dimension, required_improvement in dimension_improvement_priority:
    print(f"{dimension}: Current Avg {avg_gap_per_dimension[dimension]['current_avg']:.1f}%, Required Improvement {required_improvement:.1f}%")

print("\nNew Projected Average Score: {:.1f}/100".format(new_total_scores.mean()))
