# exams/services/ai_checker.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def check_text_originality(text_to_check: str) -> str:
    """
    Uses Gemini to analyze a piece of text for signs of being AI-generated or plagiarized.
    Returns a short string report.
    """
    if not text_to_check or len(text_to_check.split()) < 10:
        return "Answer is too short to analyze."

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an AI text analyzer. Your task is to evaluate the following text submitted by a student and determine the likelihood that it was written by an AI or plagiarized.
    Analyze its style, vocabulary, complexity, and sentence structure.
    
    Student's Answer: "{text_to_check}"

    Provide a brief, one-sentence conclusion. Start with "High likelihood," "Moderate likelihood," "Low likelihood," or "Appears original."
    For example: "Low likelihood of being AI-generated due to its simple language and slightly informal tone."
    or "Moderate likelihood of being AI-generated; the vocabulary is unusually advanced for this context."
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during originality check: {e}")
        return "Originality check could not be completed."