# exams/views.py
from django.shortcuts import render
from worksheets.models import Worksheet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from worksheets.models import Worksheet
from .models import ExamAttempt, StudentAnswer
from .services.grader import grade_exam_attempt
# NOTE: We'll add @login_required later to protect this page
# from django.contrib.auth.decorators import login_required 

# @login_required
def student_dashboard(request):
    worksheets = Worksheet.objects.all().order_by('-created_at')
    context = {
        'worksheets': worksheets
    }
    return render(request, 'exams/student_dashboard.html', context)

@login_required
def student_dashboard(request):
    worksheets = Worksheet.objects.all().order_by('-created_at')
    context = {'worksheets': worksheets}
    return render(request, 'exams/student_dashboard.html', context)

# View to create an ExamAttempt and redirect to the first question
@login_required
def start_exam(request, worksheet_pk):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk)
    # Create a new attempt
    exam_attempt, created = ExamAttempt.objects.get_or_create(
        student=request.user,
        worksheet=worksheet,
        completed=False  # Find an incomplete test or create one
    )
    return redirect('take_exam', attempt_pk=exam_attempt.pk)

# View for the main exam interface
@login_required
def take_exam(request, attempt_pk):
    exam_attempt = get_object_or_404(ExamAttempt, pk=attempt_pk, student=request.user)
    
    if exam_attempt.completed:
        return redirect('exam_results', attempt_pk=exam_attempt.pk)

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')
        answer_text = request.POST.get('answer')
        question = get_object_or_404(exam_attempt.worksheet.questions, pk=question_pk)
        StudentAnswer.objects.update_or_create(
            exam_attempt=exam_attempt,
            question=question,
            defaults={'answer_text': answer_text}
        )
    
    answered_question_ids = exam_attempt.answers.values_list('question_id', flat=True)
    next_question = exam_attempt.worksheet.questions.exclude(id__in=answered_question_ids).first()

    if next_question:
        total_questions = exam_attempt.worksheet.questions.count()
        question_number = len(answered_question_ids) + 1
        
        # --- PERFORM CALCULATION IN THE VIEW ---
        progress = 0
        if total_questions > 0:
            # Calculate the progress percentage
            progress = ((question_number - 1) / total_questions) * 100
        
        context = {
            'exam_attempt': exam_attempt,
            'question': next_question,
            'question_number': question_number,
            'total_questions': total_questions,
            'progress': progress, # <-- Add the result to the context
        }
        return render(request, 'exams/take_exam.html', context)
    else:
        # Exam is finished, grade it and show results
        exam_attempt.completed = True
        grade_exam_attempt(exam_attempt)
        exam_attempt.save()
        return redirect('exam_results', attempt_pk=exam_attempt.pk)


# NEW VIEW for showing results
@login_required
def exam_results(request, attempt_pk):
    exam_attempt = get_object_or_404(ExamAttempt, pk=attempt_pk, student=request.user)
    context = {
        'exam_attempt': exam_attempt
    }
    return render(request, 'exams/exam_results.html', context)