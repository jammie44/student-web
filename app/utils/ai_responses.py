import random
from typing import Dict, List

AI_RESPONSES: Dict[str, List[str]] = {
    "study_assistant": [
        "Great question! Let me break this down step by step.\n\n**Core concept:** The topic you're asking about connects to several important areas.\n\n**Step 1:** Start with the basics — understand the fundamental definitions.\n\n**Step 2:** Build on that foundation by looking at how the pieces interact.\n\n**Step 3:** Apply the concept to concrete examples to solidify your understanding.\n\nWould you like me to go deeper on any particular aspect?",
        "Excellent question! Here's a clear explanation:\n\n**The short answer:** The concept works by connecting key principles which leads to the outcome you're studying.\n\n**Why this matters:**\n- Solving related problems more efficiently\n- Connecting ideas across different topics\n- Building a stronger foundation for advanced study\n\nDo you have a specific example you'd like to work through together?",
        "I'd be happy to help you understand this topic!\n\n**Key Points:**\n1. The fundamental principle here is important to grasp first\n2. This leads to several practical consequences\n3. In practice, you'll see this applied in many real situations\n\n**Common misconceptions to avoid:**\n- Many students confuse related concepts — make sure you understand the distinction\n\nWhat aspect would you like to explore further?",
    ],
    "plagiarism": [
        "**📊 Plagiarism Analysis Report**\n\n---\n\n✅ **Originality Score: 89%**\n\n**Summary:** Your text shows strong original writing with a few areas to review.\n\n**⚠ Areas of Concern:**\n- Some sections use very common academic phrasing found across many sources\n- Consider adding citations for any factual claims\n\n**✅ Strengths:**\n- Your introduction is highly original\n- Personal analysis sections show genuine independent thought\n- Conclusion is well-written in your own voice\n\n**💡 Recommendations:**\n1. Add citations for facts or definitions sourced elsewhere\n2. Rephrase common academic phrases in your own words\n3. Add more personal analysis to strengthen originality",
        "**📊 Plagiarism Analysis Report**\n\n---\n\n✅ **Originality Score: 94%**\n\nYour writing is highly original. Excellent work!\n\n**Minor Observations:**\n- A few standard academic phrases are common across many papers — this is normal\n- One factual claim would benefit from a citation\n\n**✅ What You Did Well:**\n- Strong personal voice throughout\n- Original arguments and analysis\n- Well-structured academic writing\n\n*This text demonstrates strong academic integrity.*",
        "**📊 Plagiarism Analysis Report**\n\n---\n\n⚠ **Originality Score: 71%**\n\nSeveral sections require attention before submission.\n\n**🔴 High Priority:**\n- Introduction uses phrasing that closely mirrors template introductions — rewrite in your own words\n- One paragraph contains textbook language — paraphrase and cite the source\n\n**💡 Action Plan:**\n1. Rewrite the introduction completely\n2. Paraphrase flagged sections and add citations\n3. Run a second check after revisions\n\n*With these changes, your originality score should reach 85%+.*",
    ],
    "cv_generator": [
        "**📄 Professional CV — Generated**\n\n---\n\n# [Your Full Name]\n📧 your.email@example.com  |  📱 +1 (555) 000-0000  |  📍 City, Country\n\n---\n\n## Professional Summary\n\nDedicated professional with a strong academic background and hands-on experience. Proven ability to deliver high-quality outcomes and committed to continuous learning and growth.\n\n---\n\n## Education\n\n**Bachelor of Science in [Your Major]**\nUniversity of [Name] | Graduated: [Year]\n- Relevant coursework: [Course 1], [Course 2], [Course 3]\n\n---\n\n## Work Experience\n\n**[Job Title]** — [Company Name]  \n*[Start Date] – [End Date]*\n- Achieved [specific result] by implementing [approach]\n- Collaborated with team to deliver [project/outcome]\n\n---\n\n## Skills\n\n**Technical:** [Skill 1] · [Skill 2] · [Skill 3]\n**Soft Skills:** Communication · Leadership · Problem Solving\n\n---\n\n*Replace all bracketed items with your specific details. Quantify achievements wherever possible.*",
    ],
    "assignment": [
        "**📝 Formatted Assignment**\n\n---\n\n## Title: [Your Assignment Title]\n\n**Course:** [Course Name]  |  **Date:** [Submission Date]\n\n---\n\n### Introduction\n\nThis assignment examines [topic] with particular focus on [specific aspect]. This paper will argue that [your thesis statement], drawing on [sources/methods] to support this position.\n\n---\n\n### Background and Context\n\nTo fully understand [topic], it is necessary to first consider the broader context. [Background paragraph providing relevant historical or theoretical information.]\n\n---\n\n### Main Analysis\n\n#### Point 1: [First Argument]\n[Developed argument — state your point, provide evidence, explain significance.]\n\n#### Point 2: [Second Argument]\n[Developed argument — build on previous point, introduce new evidence.]\n\n---\n\n### Conclusion\n\nIn conclusion, this assignment has demonstrated that [restate thesis]. Through examination of [key points], it is clear that [overarching insight].\n\n---\n\n### References\n\nAuthor, A. (Year). *Title of Work*. Publisher.\n\n---\n\n*Formatted to academic standards. Replace placeholder text with your specific content.*",
    ],
    "research": [
        "**🔬 Research Summary Report**\n\n---\n\n## 📌 Objective\n\nThis research investigates [research question], aiming to [specific goal].\n\n---\n\n## 🔬 Methodology\n\n**Study Design:** [Quantitative / Qualitative / Mixed Methods]\n**Sample:** [n = X participants]\n**Analysis Method:** [Statistical / Thematic analysis]\n\n---\n\n## 📊 Key Findings\n\n**Finding 1:** [Primary result and significance]\n\n**Finding 2:** The data shows a pattern between [variable A] and [variable B].\n\n**Finding 3:** Qualitative analysis revealed three dominant themes:\n1. [Theme 1]\n2. [Theme 2]\n3. [Theme 3]\n\n---\n\n## ✅ Conclusions\n\nThe evidence supports that [conclusion]. These findings extend the literature by [novel contribution].\n\n---\n\n## 💡 Implications\n\n**Practical:** [What practitioners should do]\n**Academic:** [Future research directions]\n\n---\n\n*Summary generated from provided research content.*",
    ],
}


def get_ai_response(tool: str) -> str:
    """
    Returns a mock AI response for the given tool.
    To use a real AI (OpenAI, Anthropic, etc.), replace this function body.

    Example with OpenAI:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
    """
    responses = AI_RESPONSES.get(tool, AI_RESPONSES["study_assistant"])
    return random.choice(responses)
