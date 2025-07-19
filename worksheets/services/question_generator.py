# worksheets/services/question_generator.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions_from_ai(topic, grade_level, num_mcq, num_short_answer):
    """
    Uses the Gemini API to generate worksheet questions and returns a parsed dictionary.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    # A robust prompt asking for a JSON output
    prompt = f"""
    As an expert educator, create a worksheet for {grade_level} students on the topic of "{topic}".
    Generate the following:
    1. Exactly {num_mcq} multiple-choice questions (MCQs). Each MCQ must have 4 options labeled "A", "B", "C", and "D".
    2. Exactly {num_short_answer} short-answer questions. Provide a concise model answer for each.

    Return the entire output as a single, valid JSON object. Do not include any text or formatting outside of the JSON.
    The JSON object must have two keys: "mcqs" and "short_answers".
    - "mcqs" should be a list of objects, where each object has "question" (string), "options" (an object with keys "A", "B", "C", "D"), and "answer" (the correct letter, e.g., "C").
    - "short_answers" should be a list of objects, where each object has "question" (string) and "answer" (string).
    """

    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError, ValueError) as e:
        print(f"Error parsing AI response: {e}")
        # Return an empty structure on failure
        return {"mcqs": [], "short_answers": []}