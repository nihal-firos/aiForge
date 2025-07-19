# exams/services/grader.py
import os
import json
from .ai_checker import check_text_originality
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def grade_subjective_answer_with_ai(question_text, model_answer, student_answer):
    """
    Uses Gemini to evaluate a student's subjective answer.
    Returns a dictionary with a score and feedback.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert teacher evaluating a student's short answer.
    
    Question: "{question_text}"
    The ideal model answer is: "{model_answer}"
    The student's answer is: "{student_answer}"

    Evaluate the student's answer based on the model answer. Determine a score out of 5, where 5 is a perfect match and 0 is completely incorrect.
    Provide brief, constructive feedback for the student.

    Return your evaluation as a single, valid JSON object with two keys:
    1. "score" (an integer from 0 to 5)
    2. "feedback" (a string of 1-2 sentences)

    Do not include any text or formatting outside of the JSON object.
    Example: {{"score": 4, "feedback": "Your answer is good but could have mentioned the role of chlorophyll."}}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        result = json.loads(cleaned_response)
        return result
    except (json.JSONDecodeError, AttributeError, ValueError, KeyError) as e:
        print(f"Error parsing AI response for subjective grading: {e}")
        # Return a default value on failure
        return {"score": 0, "feedback": "Could not be graded automatically."}


def grade_exam_attempt(exam_attempt):
    # ... (the start of the function is the same)
    total_score = 0
    max_score = 0

    for student_answer in exam_attempt.answers.all():
        question = student_answer.question
        
        if question.question_type == 'mcq':
            # ... (MCQ grading logic is the same)
            max_score += 1
            if student_answer.answer_text.strip().upper() == question.correct_answer.strip().upper():
                student_answer.score = 1
                total_score += 1
            else:
                student_answer.score = 0
            student_answer.save()

        elif question.question_type == 'short_answer':
            max_score += 5
            
            # --- CALL THE AI CHECKER AND GRADER ---
            report = check_text_originality(student_answer.answer_text)
            ai_evaluation = grade_subjective_answer_with_ai(
                question.text,
                question.correct_answer,
                student_answer.answer_text
            )

            # --- SAVE THE RESULTS TO THE MODEL ---
            student_answer.originality_report = report
            student_answer.score = ai_evaluation.get('score', 0)
            student_answer.feedback = ai_evaluation.get('feedback', '')
            total_score += student_answer.score
            student_answer.save()

    # ... (percentage calculation logic is the same)
    if max_score > 0:
        final_percentage = (total_score / max_score) * 100
    else:
        final_percentage = 0
    exam_attempt.score = final_percentage
    exam_attempt.save()