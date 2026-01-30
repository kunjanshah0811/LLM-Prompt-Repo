from database import PromptDatabase

def seed_database():
    """Populate database with example prompts from Wolfram Prompt Repository"""
    db = PromptDatabase()
    
    # Check if database already has data
    if db.get_prompt_count() > 0:
        print(f"Database already contains {db.get_prompt_count()} prompts. Skipping seed.")
        return
    
    # Sample prompts inspired by Wolfram Prompt Repository
    sample_prompts = [
        {
            "title": "Sentiment Analysis for Survey Responses",
            "description": "Analyze the sentiment of open-ended survey responses and categorize them",
            "prompt_text": """Analyze the sentiment of the following survey response and categorize it as positive, negative, or neutral. Also provide a brief explanation of your reasoning.

Survey Response: [INSERT RESPONSE HERE]

Please provide:
1. Sentiment: [Positive/Negative/Neutral]
2. Confidence: [High/Medium/Low]
3. Key phrases that influenced your decision
4. Brief explanation""",
            "category": "Qualitative Analysis",
            "tags": "sentiment, survey, analysis, social-science",
            "use_case": "Analyzing open-ended survey questions in social research"
        },
        {
            "title": "Interview Transcript Coding",
            "description": "Code interview transcripts using thematic analysis approach",
            "prompt_text": """You are a qualitative research assistant. Read the following interview transcript excerpt and identify the main themes present. Code the text using thematic analysis principles.

Transcript: [INSERT TRANSCRIPT HERE]

Please provide:
1. List of themes identified (with brief descriptions)
2. Relevant quotes supporting each theme
3. Potential sub-themes
4. Any emergent patterns or insights""",
            "category": "Qualitative Analysis",
            "tags": "interview, coding, thematic-analysis, qualitative",
            "use_case": "Coding interview data for qualitative research projects"
        },
        {
            "title": "Research Question Generator",
            "description": "Generate research questions based on a topic and research area",
            "prompt_text": """Based on the following research topic and area, generate 5 potential research questions that would be suitable for empirical investigation in the social sciences.

Research Area: [INSERT AREA, e.g., Education, Sociology, Political Science]
Topic: [INSERT SPECIFIC TOPIC]

For each research question, provide:
1. The research question
2. Research method suggestion (qualitative/quantitative/mixed)
3. Brief rationale for why this question is important""",
            "category": "Research Design",
            "tags": "research-questions, methodology, planning",
            "use_case": "Developing research questions for new projects"
        },
        {
            "title": "Literature Review Summarizer",
            "description": "Summarize academic papers for literature review purposes",
            "prompt_text": """Summarize the following academic paper in a structured format suitable for a literature review.

Paper Title: [INSERT TITLE]
Abstract/Key Sections: [INSERT TEXT]

Please provide:
1. Main research question/objective
2. Methodology used
3. Key findings
4. Theoretical contribution
5. Limitations
6. Relevance to [YOUR RESEARCH TOPIC]""",
            "category": "Literature Review",
            "tags": "literature-review, summarization, academic-writing",
            "use_case": "Synthesizing literature for research papers"
        },
        {
            "title": "Data Categorization for Content Analysis",
            "description": "Categorize text data into predefined categories for content analysis",
            "prompt_text": """You are assisting with a content analysis study. Categorize the following text into one or more of the predefined categories. Be consistent and objective.

Categories: [INSERT YOUR CATEGORIES, e.g., Political, Economic, Social, Environmental]

Text to categorize: [INSERT TEXT HERE]

Please provide:
1. Primary category
2. Secondary categories (if applicable)
3. Confidence level
4. Key words/phrases that informed your decision
5. Any ambiguities or edge cases noted""",
            "category": "Content Analysis",
            "tags": "categorization, content-analysis, coding",
            "use_case": "Coding textual data for systematic content analysis"
        },
        {
            "title": "Social Media Post Analysis",
            "description": "Analyze social media posts for research purposes",
            "prompt_text": """Analyze the following social media post from a social science research perspective.

Post: [INSERT POST TEXT]

Please analyze:
1. Main topic/theme
2. Sentiment and emotional tone
3. Target audience
4. Persuasive techniques used (if any)
5. Potential biases or framing
6. Cultural or social context
7. Research implications""",
            "category": "Digital Methods",
            "tags": "social-media, digital-research, discourse-analysis",
            "use_case": "Analyzing social media data for research"
        },
        {
            "title": "Survey Question Improvement",
            "description": "Improve survey questions to reduce bias and increase clarity",
            "prompt_text": """Review the following survey question and provide recommendations to improve it. Consider potential biases, clarity, validity, and best practices in survey design.

Original Question: [INSERT QUESTION]

Please provide:
1. Issues identified (bias, leading language, ambiguity, etc.)
2. Improved version of the question
3. Explanation of changes made
4. Alternative versions (if applicable)
5. Recommendations for response options (if applicable)""",
            "category": "Research Design",
            "tags": "survey-design, methodology, question-design",
            "use_case": "Improving survey instruments for research studies"
        },
        {
            "title": "Hypothesis Generator",
            "description": "Generate testable hypotheses based on research variables",
            "prompt_text": """Based on the following research variables and context, generate testable hypotheses suitable for empirical research in the social sciences.

Independent Variable(s): [INSERT VARIABLES]
Dependent Variable(s): [INSERT VARIABLES]
Research Context: [INSERT CONTEXT]

Please provide:
1. 3-5 testable hypotheses
2. Expected direction of relationship for each
3. Theoretical justification
4. Suggested method for testing (experimental, survey, observational, etc.)""",
            "category": "Research Design",
            "tags": "hypothesis, theory, research-design",
            "use_case": "Developing hypotheses for quantitative research"
        },
        {
            "title": "Focus Group Discussion Guide",
            "description": "Create discussion guide questions for focus groups",
            "prompt_text": """Create a focus group discussion guide for the following research topic. Include opening, introductory, transition, key, and ending questions.

Research Topic: [INSERT TOPIC]
Target Participants: [INSERT DESCRIPTION]
Research Objectives: [INSERT OBJECTIVES]

Please provide:
1. Opening question (ice breaker)
2. Introductory questions (2-3)
3. Transition questions (2-3)
4. Key questions (3-5, most important)
5. Ending question
6. Suggested probes for each section""",
            "category": "Qualitative Methods",
            "tags": "focus-group, interview-guide, qualitative",
            "use_case": "Preparing for focus group data collection"
        },
        {
            "title": "Statistical Result Interpreter",
            "description": "Interpret statistical results in plain language for research papers",
            "prompt_text": """Interpret the following statistical results in clear, accessible language suitable for the results section of a research paper. Avoid jargon where possible.

Statistical Test: [INSERT TEST TYPE, e.g., t-test, ANOVA, regression]
Results: [INSERT STATISTICS, e.g., t(98) = 3.45, p < .001, d = 0.68]
Context: [BRIEF DESCRIPTION OF WHAT WAS BEING TESTED]

Please provide:
1. Plain language interpretation
2. What the results mean for the hypothesis
3. Effect size interpretation (if applicable)
4. Suggested visualization type
5. Possible limitations to note""",
            "category": "Data Analysis",
            "tags": "statistics, interpretation, writing",
            "use_case": "Writing up quantitative results in research papers"
        }
    ]
    
    # Add all prompts to database
    for prompt in sample_prompts:
        db.add_prompt(
            title=prompt["title"],
            description=prompt["description"],
            prompt_text=prompt["prompt_text"],
            category=prompt["category"],
            tags=prompt["tags"],
            use_case=prompt["use_case"]
        )
    
    print(f"Successfully seeded database with {len(sample_prompts)} prompts!")

if __name__ == "__main__":
    seed_database()
