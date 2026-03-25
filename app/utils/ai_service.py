"""
Real AI service using Anthropic Claude claude-sonnet-4-5.
Replaces the old mock ai_responses.py completely.
"""
import os
import anthropic

# Initialise client — reads ANTHROPIC_API_KEY from environment
_client = None

def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Add it in your Render service environment variables."
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _call(system: str, user: str, max_tokens: int = 1500) -> str:
    """Single call to Claude claude-sonnet-4-5 and return the text response."""
    message = get_client().messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


# ── Tool-specific system prompts ─────────────────────────────────────────────

SYSTEM_STUDY = """You are an expert Study Assistant helping university and high school students.
When answering questions:
- Give the correct, specific answer immediately — never give vague or generic responses
- Use clear headings, bullet points, and examples where helpful
- Explain concepts at the right level for a student
- Include relevant facts, formulas, definitions, or examples as needed
- Be thorough but concise
- Never say "the concept" or "the topic" — always use the actual subject name
- Format your response with markdown for clarity"""

SYSTEM_PLAGIARISM = """You are an expert academic plagiarism and originality checker.
Analyse the provided text carefully and:
1. Assess the writing style — is it consistent, or does it shift register suddenly?
2. Identify phrases that sound copied from textbooks, Wikipedia, or common sources
3. Look for sudden changes from simple to very academic language (a red flag)
4. Check if arguments are developed or just assembled from generic statements
5. Give a realistic originality score (0-100%)
6. List specific sentences or phrases that appear problematic with reasons
7. Provide actionable, specific improvement suggestions

Be strict and realistic. Do NOT give the same canned response regardless of input.
Format clearly with sections: Score, Issues Found, Strengths, Recommendations."""

SYSTEM_CV = """You are a professional CV writer and career coach.
When given a description of someone's background, role, or field:
- Write a complete, polished, professional CV/resume
- Use real, specific content relevant to the person's field — NOT placeholder brackets
- Include: Professional Summary, Education, Work Experience, Skills, Projects, Certifications
- Use strong action verbs and quantified achievements where possible
- Tailor language to the specific industry or role mentioned
- Format clearly with proper sections and bullet points
- Make it genuinely impressive and presentable

Never use [Your Name], [Company], or any bracket placeholders in your output.
If details are not provided, make reasonable professional assumptions based on the field."""

SYSTEM_ASSIGNMENT = """You are an expert academic writer and editor.
When given a piece of student writing to format:
- Actually rewrite and format THE USER'S SPECIFIC TEXT — do not use placeholders
- Improve academic tone, structure, grammar, and clarity
- Organise into proper sections: Introduction, Body (with subheadings), Conclusion
- Add academic language and transitions
- Suggest or add a reference section with plausible citations matching the topic
- Preserve the student's core ideas but elevate the expression
- The output must be ready to submit — no bracket placeholders whatsoever

Format with clear markdown headings and structure."""

SYSTEM_RESEARCH = """You are an expert research analyst and academic summariser.
When given research text, an essay, or article:
- Provide a structured, detailed summary of the ACTUAL content provided
- Extract and clearly state: Main Objective, Key Arguments, Evidence Used, Conclusions
- Identify the theoretical framework or approach used
- Note any gaps, limitations, or areas for further research
- Use clear academic language
- Never use placeholder brackets — always refer to the actual content

Structure your response with clear sections and be specific to what was actually written."""


# ── Public functions called by routes ────────────────────────────────────────

def answer_study_question(question: str, history: list = None) -> str:
    """Study assistant — answers the actual question asked."""
    messages = []
    if history:
        for msg in history[-8:]:  # keep last 8 turns for context
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})

    message = get_client().messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        system=SYSTEM_STUDY,
        messages=messages,
    )
    return message.content[0].text


def check_plagiarism(text: str) -> str:
    """Analyse text for plagiarism — actually reads the provided text."""
    return _call(
        SYSTEM_PLAGIARISM,
        f"Please analyse this text for plagiarism and originality:\n\n{text}",
        max_tokens=1200,
    )


def generate_cv(description: str) -> str:
    """Generate a real, filled-in CV based on the description provided."""
    return _call(
        SYSTEM_CV,
        f"Create a complete, professional CV based on this information:\n\n{description}",
        max_tokens=2000,
    )


def format_assignment(text: str) -> str:
    """Actually format and improve the student's specific text."""
    return _call(
        SYSTEM_ASSIGNMENT,
        f"Format and improve this student assignment text into a polished academic piece:\n\n{text}",
        max_tokens=2000,
    )


def summarise_research(text: str) -> str:
    """Summarise the actual research text provided."""
    return _call(
        SYSTEM_RESEARCH,
        f"Provide a detailed research summary of this text:\n\n{text}",
        max_tokens=1500,
    )


# ── Credit costs per tool ─────────────────────────────────────────────────────
CREDIT_COSTS = {
    "study_assistant": 2,
    "plagiarism": 3,
    "cv_generator": 5,
    "assignment": 4,
    "research": 3,
}
