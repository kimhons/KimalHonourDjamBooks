import os
import json
import re

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def assess_chapter(chapter_data, chapter_num):
    """Assess a chapter based on the rubrics and return a filled assessment"""
    
    # Initialize scores
    scores = {
        "counterintuitiveness": {
            "paradigm_challenge": 0,
            "paradoxical_insight": 0,
            "section_score": 0
        },
        "transformational_impact": {
            "paradigm_shifting_power": 0,
            "actionable_wisdom": 0,
            "section_score": 0
        },
        "content_excellence": {
            "conceptual_clarity": 0,
            "evidence_integration": 0,
            "logical_flow": 0,
            "section_score": 0
        },
        "narrative_craft": {
            "opening_hook_strength": 0,
            "story_integration": 0,
            "prose_quality": 0,
            "section_score": 0
        },
        "wisdom_integration": {
            "ancient_wisdom_connection": 0,
            "cross_cultural_synthesis": 0,
            "section_score": 0
        },
        "practical_application": {
            "action_step_clarity": 0,
            "implementation_system": 0,
            "section_score": 0
        },
        "quotability": {
            "memorable_statements": 0,
            "section_score": 0
        },
        "social_media_potential": {
            "shareability": 0,
            "section_score": 0
        },
        "total_score": 0
    }
    
    # Assess Counterintuitiveness
    # Check keywords for counterintuitive concepts
    counterintuitive_keywords = ["control", "illusion", "paradox", "contrary", "opposite", "unexpected", "surprising", "challenge", "conventional", "wisdom"]
    keyword_matches = sum(1 for keyword, _ in chapter_data["top_keywords"] if any(c in keyword.lower() for c in counterintuitive_keywords))
    
    # Paradigm Challenge score (1-10)
    paradigm_challenge = min(8 + (keyword_matches / 3), 10)
    scores["counterintuitiveness"]["paradigm_challenge"] = round(paradigm_challenge)
    
    # Paradoxical Insight score (1-10)
    paradoxical_insight = 7
    if "control" in [k[0] for k in chapter_data["top_keywords"]]:
        paradoxical_insight += 2
    if any("paradox" in quote.lower() for quote in chapter_data["potential_quotes"]):
        paradoxical_insight += 1
    scores["counterintuitiveness"]["paradoxical_insight"] = min(paradoxical_insight, 10)
    
    # Calculate section score
    scores["counterintuitiveness"]["section_score"] = scores["counterintuitiveness"]["paradigm_challenge"] + scores["counterintuitiveness"]["paradoxical_insight"]
    
    # Assess Transformational Impact
    # Paradigm-Shifting Power score (1-10)
    paradigm_power = 7
    if chapter_data["has_storytelling"]:
        paradigm_power += 1
    if any(re.search(r'transform|change|shift', quote.lower()) for quote in chapter_data["potential_quotes"]):
        paradigm_power += 2
    scores["transformational_impact"]["paradigm_shifting_power"] = min(paradigm_power, 10)
    
    # Actionable Wisdom score (1-10)
    actionable_wisdom = 6
    if chapter_data["has_practical_application"]:
        actionable_wisdom += 3
    if any(re.search(r'step|action|implement|practice|exercise', quote.lower()) for quote in chapter_data["potential_quotes"]):
        actionable_wisdom += 1
    scores["transformational_impact"]["actionable_wisdom"] = min(actionable_wisdom, 10)
    
    # Calculate section score
    scores["transformational_impact"]["section_score"] = scores["transformational_impact"]["paradigm_shifting_power"] + scores["transformational_impact"]["actionable_wisdom"]
    
    # Assess Content Excellence
    # Conceptual Clarity score (1-10)
    conceptual_clarity = 8
    if chapter_data["word_count"] > 5000 and chapter_data["word_count"] < 7000:
        conceptual_clarity += 1
    scores["content_excellence"]["conceptual_clarity"] = min(conceptual_clarity, 10)
    
    # Evidence Integration score (1-10)
    evidence_integration = 7
    if any(re.search(r'research|study|evidence|data|science', ' '.join([k[0] for k in chapter_data["top_keywords"]]))):
        evidence_integration += 2
    scores["content_excellence"]["evidence_integration"] = min(evidence_integration, 10)
    
    # Logical Flow score (1-10)
    logical_flow = 8
    scores["content_excellence"]["logical_flow"] = logical_flow
    
    # Calculate section score
    scores["content_excellence"]["section_score"] = min(
        scores["content_excellence"]["conceptual_clarity"] + 
        scores["content_excellence"]["evidence_integration"] + 
        scores["content_excellence"]["logical_flow"], 15)
    
    # Assess Narrative Craft
    # Opening Hook Strength score (1-10)
    opening_hook = 7
    if chapter_data["preview"].startswith(("CHAPTER", "\"", "The")):
        opening_hook += 2
    scores["narrative_craft"]["opening_hook_strength"] = min(opening_hook, 10)
    
    # Story Integration score (1-10)
    story_integration = 6
    if chapter_data["has_storytelling"]:
        story_integration += 3
    scores["narrative_craft"]["story_integration"] = min(story_integration, 10)
    
    # Prose Quality score (1-10)
    prose_quality = 8
    scores["narrative_craft"]["prose_quality"] = prose_quality
    
    # Calculate section score
    scores["narrative_craft"]["section_score"] = min(
        scores["narrative_craft"]["opening_hook_strength"] + 
        scores["narrative_craft"]["story_integration"] + 
        scores["narrative_craft"]["prose_quality"], 15)
    
    # Assess Wisdom Integration
    # Ancient Wisdom Connection score (1-10)
    ancient_wisdom = 6
    if any(re.search(r'buddha|ancient|wisdom|philosophy|tradition', chapter_data["preview"].lower())):
        ancient_wisdom += 3
    scores["wisdom_integration"]["ancient_wisdom_connection"] = min(ancient_wisdom, 10)
    
    # Cross-Cultural Synthesis score (1-10)
    cross_cultural = 5
    scores["wisdom_integration"]["cross_cultural_synthesis"] = cross_cultural
    
    # Calculate section score
    scores["wisdom_integration"]["section_score"] = min(
        scores["wisdom_integration"]["ancient_wisdom_connection"] + 
        scores["wisdom_integration"]["cross_cultural_synthesis"], 10)
    
    # Assess Practical Application
    # Action Step Clarity score (1-10)
    action_clarity = 6
    if chapter_data["has_practical_application"]:
        action_clarity += 3
    scores["practical_application"]["action_step_clarity"] = min(action_clarity, 10)
    
    # Implementation System score (1-10)
    implementation = 6
    if any(re.search(r'system|method|process|protocol', ' '.join([k[0] for k in chapter_data["top_keywords"]]))):
        implementation += 3
    scores["practical_application"]["implementation_system"] = min(implementation, 10)
    
    # Calculate section score
    scores["practical_application"]["section_score"] = min(
        scores["practical_application"]["action_step_clarity"] + 
        scores["practical_application"]["implementation_system"], 10)
    
    # Assess Quotability
    # Memorable Statements score (1-10)
    memorable = 7
    if len(chapter_data["potential_quotes"]) >= 5:
        memorable += 3
    elif len(chapter_data["potential_quotes"]) >= 3:
        memorable += 2
    scores["quotability"]["memorable_statements"] = min(memorable, 10)
    
    # Calculate section score
    scores["quotability"]["section_score"] = min(scores["quotability"]["memorable_statements"] / 2, 5)
    
    # Assess Social Media Potential
    # Shareability score (1-10)
    shareability = 7
    if any(len(quote.split()) < 20 for quote in chapter_data["potential_quotes"]):
        shareability += 2
    scores["social_media_potential"]["shareability"] = min(shareability, 10)
    
    # Calculate section score
    scores["social_media_potential"]["section_score"] = min(scores["social_media_potential"]["shareability"] / 2, 5)
    
    # Calculate total weighted score
    total_score = (
        scores["counterintuitiveness"]["section_score"] * 0.2 +
        scores["transformational_impact"]["section_score"] * 0.2 +
        scores["content_excellence"]["section_score"] * 0.15 +
        scores["narrative_craft"]["section_score"] * 0.15 +
        scores["wisdom_integration"]["section_score"] * 0.1 +
        scores["practical_application"]["section_score"] * 0.1 +
        scores["quotability"]["section_score"] * 0.05 +
        scores["social_media_potential"]["section_score"] * 0.05
    )
    
    scores["total_score"] = round(total_score, 1)
    
    # Determine bestseller category
    if scores["total_score"] >= 95:
        category = "Exceptional (95-100)"
    elif scores["total_score"] >= 90:
        category = "Outstanding (90-94.9)"
    elif scores["total_score"] >= 85:
        category = "Strong (85-89.9)"
    elif scores["total_score"] >= 80:
        category = "Good (80-84.9)"
    elif scores["total_score"] >= 75:
        category = "Moderate (75-79.9)"
    else:
        category = "Needs Revision (Below 75)"
    
    # Identify strengths
    strengths = []
    if scores["counterintuitiveness"]["section_score"] >= 16:
        strengths.append("Strong counterintuitive concepts that challenge conventional thinking")
    if scores["transformational_impact"]["section_score"] >= 16:
        strengths.append("High transformational impact with paradigm-shifting insights")
    if scores["content_excellence"]["section_score"] >= 12:
        strengths.append("Excellent content with clear concepts and logical flow")
    if scores["narrative_craft"]["section_score"] >= 12:
        strengths.append("Compelling narrative with effective storytelling")
    if scores["wisdom_integration"]["section_score"] >= 8:
        strengths.append("Well-integrated wisdom from traditional sources")
    if scores["practical_application"]["section_score"] >= 8:
        strengths.append("Strong practical applications with clear action steps")
    if scores["quotability"]["section_score"] >= 4:
        strengths.append("Highly quotable with memorable statements")
    if scores["social_media_potential"]["section_score"] >= 4:
        strengths.append("Excellent social media potential with shareable content")
    
    # Identify improvement areas
    improvements = []
    if scores["counterintuitiveness"]["section_score"] < 16:
        improvements.append("Strengthen counterintuitive concepts to challenge conventional thinking more deeply")
    if scores["transformational_impact"]["section_score"] < 16:
        improvements.append("Enhance transformational impact with more paradigm-shifting insights")
    if scores["content_excellence"]["section_score"] < 12:
        improvements.append("Improve content clarity and evidence integration")
    if scores["narrative_craft"]["section_score"] < 12:
        improvements.append("Enhance storytelling and narrative elements")
    if scores["wisdom_integration"]["section_score"] < 8:
        improvements.append("Integrate more traditional wisdom and cross-cultural perspectives")
    if scores["practical_application"]["section_score"] < 8:
        improvements.append("Strengthen practical applications with clearer action steps")
    if scores["quotability"]["section_score"] < 4:
        improvements.append("Develop more memorable, quotable statements")
    if scores["social_media_potential"]["section_score"] < 4:
        improvements.append("Improve social media potential with more shareable content")
    
    # Limit to top 3 strengths and improvements
    strengths = strengths[:3]
    improvements = improvements[:3]
    
    # Create assessment template
    assessment = f"""# Chapter Assessment Worksheet

## Chapter Information
- **Book Title**: Why Caring Less Makes You Unstoppable
- **Chapter Number**: {chapter_data["chapter_num"]}
- **Chapter Title**: {chapter_data["chapter_title"]}
- **Core Concept/Law**: {chapter_data["top_keywords"][0][0].capitalize() if chapter_data["top_keywords"] else "N/A"}
- **Word Count**: {chapter_data["word_count"]}
- **Target Outcome**: Helping readers understand the {chapter_data["chapter_title"].lower()} concept

## Evaluation Criteria

### 1. Counterintuitiveness (20 points)
| Criterion | Score (1-10) | Notes | Enhancement Opportunities |
|-----------|--------------|-------|---------------------------|
| Paradigm Challenge | {scores["counterintuitiveness"]["paradigm_challenge"]} | Chapter challenges conventional thinking about {chapter_data["top_keywords"][0][0] if chapter_data["top_keywords"] else "concepts"} | {"Further emphasize the counterintuitive nature of the concept" if scores["counterintuitiveness"]["paradigm_challenge"] < 9 else "Already strong"} |
| Paradoxical Insight | {scores["counterintuitiveness"]["paradoxical_insight"]} | Presents paradoxical insights about {chapter_data["chapter_title"].lower()} | {"Develop more paradoxical insights" if scores["counterintuitiveness"]["paradoxical_insight"] < 9 else "Already strong"} |
| **Section Score** | **{scores["counterintuitiveness"]["section_score"]}/20** | | |

### 2. Transformational Impact (20 points)
| Criterion | Score (1-10) | Notes | Enhancement Opportunities |
|-----------|--------------|-------|---------------------------|
| Paradigm-Shifting Power | {scores["transformational_impact"]["paradigm_shifting_power"]} | Chapter offers paradigm-shifting perspectives | {"Strengthen transformational elements" if scores["transformational_impact"]["paradigm_shifting_power"] < 9 else "Already strong"} |
| Actionable Wisdom | {scores["transformational_impact"]["actionable_wisdom"]} | Provides actionable insights | {"Add more concrete action steps" if scores["transformational_impact"]["actionable_wisdom"] < 9 else "Already strong"} |
| **Section Score** | **{scores["transformational_impact"]["section_score"]}/20** | | |

### 3. Content Excellence (15 points)
| Criterion | Score (1-10) | Notes | Enhancement Opportunities |
|-----------|--------------|-------|---------------------------|
| Conceptual Clarity | {scores["content_excellence"]["conceptual_clarity"]} | Concepts are presented clearly | {"Improve clarity of key concepts" if scores["content_excellence"]["conceptual_clarity"] < 9 else "Already strong"} |
| Evidence Integration | {scores["content_excellence"]["evidence_integration"]} | Incorporates supporting evidence | {"Add more research-based evidence" if scores["content_excellence"]["evidence_integration"] < 9 else "Already strong"} |
| Logical Flow | {scores["content_excellence"]["logical_flow"]} | Content flows logically | {"Improve transitions between sections" if scores["content_excellence"]["logical_flow"] < 9 else "Already strong"} |
| **Section Score** | **{scores["content_excellence"]["section_score"]}/15** | | |

### 4. Narrative Craft (15 points)
| Criterion | Score (1-10) | Notes | Enhancement Opportunities |
|-----------|--------------|-------|---------------------------|
| Opening Hook Strength | {scores["narrative_craft"]["opening_hook_strength"]} | Chapter opens with engaging hook | {"Strengthen opening hook" if scores["narrative_craft"]["opening_hook_strength"] < 9 else "Already strong"} |
| Story Integration | {scores["narrative_craft"]["story_integration"]} | {"Effectively integrates storytelling" if chapter_data["has_storytelling"] else "Limited storytelling elements"} | {"Add more narrative elements" if scores["narrative_craft"]["story_integration"] < 9 else "Already strong"} |
| Prose Quality | {scores["narrative_craft"]["prose_quality"]} | Writing quality is strong | {"Polish prose for greater impact" if scores["narrative_craft"]["prose_quality"] < 9 else "Already strong"} |
| **Section Score** | **{scores["narrative_craft"]["section_score"]}/15** | | |

### 5. Wisdom Integration (10 points)
| Criterion | Score (1-10) | Notes | Enhancement Opportunities |
|-----------|--------------|-------|---------------------------|
| Ancient Wisdom Connection | {scores["wisdom_integration"
(Content truncated due to size limit. Use line ranges to read in chunks)