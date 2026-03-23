"""
Mock AI response engine.
Replace the get_ai_response() call with a real OpenAI/Anthropic call
by swapping the function body — the rest of the app doesn't change.
"""
import random
from typing import Dict, List

AI_RESPONSES: Dict[str, List[str]] = {
    "study_assistant": [
        "Great question! Let me break this down step by step.\n\nThe key concept here involves understanding the underlying principles. First, we need to establish a foundation:\n\n**Core idea:** The topic you're asking about connects to several important areas that work together.\n\n**Step 1:** Start with the basics — make sure you understand the fundamental definitions.\n\n**Step 2:** Build on that foundation by looking at how the pieces interact.\n\n**Step 3:** Apply the concept to concrete examples to solidify your understanding.\n\nWould you like me to go deeper on any particular aspect?",

        "Excellent question! This is something many students find challenging at first, but once you see the pattern it becomes much clearer.\n\n**The short answer:** The concept works by [describing the mechanism] which leads to [the outcome].\n\n**Why this matters:** Understanding this helps you:\n- Solve related problems more efficiently\n- Connect ideas across different topics\n- Build a stronger foundation for advanced study\n\n**A helpful analogy:** Think of it like [relatable comparison] — just as [familiar thing] works by [familiar mechanism], this concept works similarly.\n\nDo you have a specific example you'd like to work through together?",

        "I'd be happy to help you understand this topic!\n\n**Key Points:**\n1. The fundamental principle is that [core concept]\n2. This leads to [consequence or application]\n3. In practice, you'll see this when [real-world example]\n\n**Common misconceptions to avoid:**\n- Many students think [wrong idea], but actually [correct idea]\n- Don't confuse [similar concept A] with [similar concept B]\n\n**For your studies:**\nFocus on mastering the core definition first, then work through practice problems. The more examples you see, the more intuitive it becomes.\n\nWhat aspect would you like to explore further?",

        "This is a fascinating area of study! Let me give you a thorough explanation.\n\n**Overview:** [Topic] is important because it forms the basis for understanding [related concepts].\n\n**Detailed breakdown:**\n\n*Part 1 — The Theory:* The theoretical framework suggests that [explanation]. This was first established by [context] and has since been refined.\n\n*Part 2 — The Practice:* In practical terms, this means [application]. You'll encounter this most often in [context].\n\n*Part 3 — Exam Tips:* When answering exam questions on this topic:\n- Always define your terms first\n- Use specific examples\n- Show your reasoning clearly\n\nIs there a specific part of this you'd like me to elaborate on?",
    ],

    "plagiarism": [
        "**📊 Plagiarism Analysis Report**\n\n---\n\n✅ **Originality Score: 89%**\n\n**Summary:** Your text shows strong original writing with a few areas to review.\n\n---\n\n**⚠ Areas of Concern:**\n\n*Paragraph 2, Lines 3–5:*\nThe phrasing here uses very common academic language that appears frequently across many sources. Consider rephrasing with your own voice.\n\n*Paragraph 4:*\nThis section contains a common definition that should be cited if sourced from a textbook.\n\n---\n\n**✅ Strengths:**\n- Your introduction is highly original\n- Personal analysis sections show genuine independent thought\n- Conclusion is well-written in your own voice\n\n---\n\n**💡 Recommendations:**\n1. Add citations for any facts or definitions sourced elsewhere\n2. Rephrase lines 3–5 of paragraph 2 in your own words\n3. Consider adding more personal analysis to strengthen originality\n\n*Overall: This looks like solid original work with minor improvements needed.*",

        "**📊 Plagiarism Analysis Report**\n\n---\n\n✅ **Originality Score: 94%**\n\nYour writing is highly original. Excellent work!\n\n---\n\n**Minor Observations:**\n\n- A few standard academic phrases are common across many papers — this is normal and acceptable\n- One factual claim in paragraph 3 would benefit from a citation\n\n---\n\n**✅ What You Did Well:**\n- Strong personal voice throughout\n- Original arguments and analysis\n- Well-structured academic writing\n\n---\n\n**💡 Final Suggestion:**\nAdd a reference for the statistic mentioned in paragraph 3. Everything else looks great!\n\n*This text demonstrates strong academic integrity.*",

        "**📊 Plagiarism Analysis Report**\n\n---\n\n⚠ **Originality Score: 71%**\n\nSeveral sections require attention before submission.\n\n---\n\n**🔴 High Priority:**\n\n*Introduction (Lines 1–4):*\nThis opening closely mirrors common template introductions. Rewrite entirely in your own words.\n\n*Paragraph 3 (Full):*\nThis paragraph contains phrasing that matches academic textbook language closely. Paraphrase and cite the source.\n\n---\n\n**🟡 Medium Priority:**\n\n*Paragraph 5:*\nThe definition provided here is standard — add a citation.\n\n---\n\n**💡 Action Plan:**\n1. Rewrite the introduction completely\n2. Paraphrase paragraph 3 and add citation\n3. Add references for all definitions\n4. Run a second check after revisions\n\n*With these changes, your originality score should reach 85%+.*",
    ],

    "cv_generator": [
        "**📄 Professional CV — Generated**\n\n---\n\n# [Your Full Name]\n📧 your.email@example.com  |  📱 +1 (555) 000-0000  |  📍 City, Country\n🔗 linkedin.com/in/yourname  |  💻 github.com/yourname\n\n---\n\n## Professional Summary\n\nDedicated and results-driven professional with a strong academic background and hands-on experience in [your field]. Proven ability to [key skill 1] and [key skill 2] while delivering high-quality outcomes. Passionate about [area of interest] and committed to continuous learning and growth.\n\n---\n\n## Education\n\n**Bachelor of Science in [Your Major]**\nUniversity of [Name] | Graduated: [Year] | GPA: [X.X]/4.0\n- Relevant coursework: [Course 1], [Course 2], [Course 3]\n- Honours/Awards: [If applicable]\n\n---\n\n## Work Experience\n\n**[Job Title]** — [Company Name]\n*[Start Month Year] – [End Month Year]*\n- Achieved [specific result] by implementing [approach], resulting in [measurable impact]\n- Collaborated with [team/department] to deliver [project/outcome]\n- Developed and maintained [system/process] used by [X] users/people\n\n---\n\n## Skills\n\n**Technical:** [Skill 1] · [Skill 2] · [Skill 3] · [Skill 4]\n**Soft Skills:** Communication · Leadership · Problem Solving · Team Collaboration\n**Languages:** English (Fluent) · [Other Language] ([Level])\n\n---\n\n## Projects\n\n**[Project Name]** | [Tech Stack Used]\n- Built [what it does] — [brief description of impact or outcome]\n- Repository: github.com/yourname/project\n\n---\n\n*Tip: Replace all bracketed items with your specific details. Quantify achievements wherever possible (e.g., \"increased efficiency by 30%\").*",
    ],

    "assignment": [
        "**📝 Formatted Assignment**\n\n---\n\n## Title: [Your Assignment Title]\n\n**Course:** [Course Name and Code]  \n**Student:** [Your Name]  \n**Date:** [Submission Date]  \n**Word Count:** ~[X] words\n\n---\n\n### Introduction\n\nThis assignment examines [topic] with particular focus on [specific aspect]. The significance of this subject lies in its direct relevance to [broader context]. This paper will argue that [your thesis statement], drawing on [sources/methods] to support this position.\n\n---\n\n### Background and Context\n\nTo fully understand [topic], it is necessary to first consider the broader context in which it exists. [Background paragraph with 3–4 sentences providing relevant historical, theoretical, or contextual information.]\n\nScholars such as [Author (Year)] have noted that [relevant point], while others argue that [contrasting view (Author, Year)]. This ongoing debate highlights the complexity of the subject.\n\n---\n\n### Main Analysis\n\n#### Point 1: [First Argument Heading]\n\n[Developed argument paragraph. State your point, provide evidence, explain significance.]\n\n#### Point 2: [Second Argument Heading]\n\n[Developed argument paragraph. Build on previous point, introduce new evidence.]\n\n#### Point 3: [Third Argument Heading]\n\n[Developed argument paragraph. Address counterarguments if applicable.]\n\n---\n\n### Conclusion\n\nIn conclusion, this assignment has demonstrated that [restate thesis]. Through examination of [key points covered], it is clear that [overarching insight]. The implications of these findings suggest that [broader significance or future direction].\n\n---\n\n### References\n\nAuthor, A. (Year). *Title of Work*. Publisher.\nAuthor, B., & Author, C. (Year). Article title. *Journal Name*, *Vol*(Issue), pages. DOI\n\n---\n\n*Formatted to academic standards. Replace placeholder text with your specific content.*",
    ],

    "research": [
        "**🔬 Research Summary Report**\n\n---\n\n## 📌 Objective\n\nThis research investigates [research question/problem], aiming to [specific goal]. The study addresses a gap in existing literature regarding [gap identified].\n\n---\n\n## 🔬 Methodology\n\n**Study Design:** [Quantitative / Qualitative / Mixed Methods]\n**Sample:** [n = X participants / documents / data points]\n**Data Collection:** [Surveys / Interviews / Experiments / Document analysis]\n**Analysis Method:** [Statistical analysis / Thematic analysis / etc.]\n\n---\n\n## 📊 Key Findings\n\n**Finding 1:** [Primary result] — [significance or implication]\n\n**Finding 2:** [Secondary result] — The data shows a [correlation / difference / pattern] between [variable A] and [variable B] (p < 0.05).\n\n**Finding 3:** Qualitative analysis revealed three dominant themes:\n1. [Theme 1] — present in [X]% of responses\n2. [Theme 2] — described as [characteristic]\n3. [Theme 3] — linked to [outcome]\n\n---\n\n## ✅ Conclusions\n\nThe evidence supports the hypothesis that [conclusion]. These findings are consistent with prior research by [Author, Year] but extend the literature by [novel contribution].\n\n---\n\n## 💡 Implications & Recommendations\n\n**Practical:** [What practitioners should do with this information]\n**Academic:** [How this contributes to the field / future research directions]\n**Policy:** [Relevant policy recommendations if applicable]\n\n---\n\n## 📚 Limitations\n\n- Sample size may limit generalisability\n- [Other specific limitation]\n- Future research should [suggestion]\n\n---\n\n*Summary generated from provided research content.*",
    ],
}


def get_ai_response(tool: str) -> str:
    """
    Returns a mock AI response for the given tool.
    To use a real AI API, replace this function body:

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
