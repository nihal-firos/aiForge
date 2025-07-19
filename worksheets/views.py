# worksheets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorksheetGeneratorForm
from .models import Worksheet, Question
from .services.question_generator import generate_questions_from_ai
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from .models import Worksheet


def create_worksheet(request):
    if request.method == 'POST':
        form = WorksheetGeneratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # 1. Call the Gemini AI service
            ai_content = generate_questions_from_ai(
                topic=data['topic'],
                grade_level=data['grade_level'],
                num_mcq=data['num_mcq'],
                num_short_answer=data['num_short_answer']
            )

            # 2. Create Worksheet and Question objects in the database
            worksheet = Worksheet.objects.create(
                title=data['topic'], subject=data['subject'], grade_level=data['grade_level']
            )

            for mcq in ai_content.get('mcqs', []):
                Question.objects.create(
                    worksheet=worksheet, text=mcq['question'], question_type='mcq',
                    options=mcq['options'], correct_answer=mcq['answer']
                )

            for sa in ai_content.get('short_answers', []):
                Question.objects.create(
                    worksheet=worksheet, text=sa['question'], question_type='short_answer',
                    correct_answer=sa['answer']
                )

            return redirect('worksheet_detail', pk=worksheet.pk)
    else:
        form = WorksheetGeneratorForm()

    return render(request, 'worksheets/create_worksheet.html', {'form': form})

def worksheet_detail(request, pk):
    worksheet = get_object_or_404(Worksheet, pk=pk)
    return render(request, 'worksheets/worksheet_detail.html', {'worksheet': worksheet})

def download_worksheet_pdf(request, pk):
    worksheet = get_object_or_404(Worksheet, pk=pk)
    
    # Create an HttpResponse with the PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{worksheet.title}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # --- Start writing the PDF ---
    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, height - inch, worksheet.title)
    
    p.setFont("Helvetica", 12)
    p.drawString(inch, height - 1.25*inch, f"Subject: {worksheet.subject} | Grade: {worksheet.grade_level}")

    # Set initial y position for questions
    y = height - 2*inch
    
    # Loop through questions and write them to the PDF
    for i, question in enumerate(worksheet.questions.all(), 1):
        p.drawString(inch, y, f"{i}. {question.text}")
        y -= 0.3*inch
        
        if question.question_type == 'mcq':
            for key, value in question.options.items():
                p.drawString(inch * 1.2, y, f"{key}) {value}")
                y -= 0.3*inch
        
        # Add space before next question
        y -= 0.2*inch
        
        # Add a new page if content gets too low
        if y < inch:
            p.showPage()
            y = height - inch
            p.setFont("Helvetica", 12)


    # --- Close the PDF object cleanly ---
    p.showPage()
    p.save()

    return response

@login_required
def teacher_dashboard(request):
    """
    Displays a list of worksheets created by the logged-in teacher.
    """
    # This filter is the key to enforcing ownership.
    worksheets = Worksheet.objects.filter(created_by=request.user).annotate(
        attempt_count=Count('examattempt'),
        average_score=Avg('examattempt__score')
    ).order_by('-created_at')

    context = {
        'worksheets': worksheets
    }
    return render(request, 'worksheets/teacher_dashboard.html', context)


@login_required
def worksheet_attempts(request, worksheet_pk):
    """
    Displays a list of all student attempts for a specific worksheet.
    """
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk)
    # Use `prefetch_related` to efficiently get the student's username
    attempts = worksheet.examattempt_set.all().prefetch_related('student').order_by('-start_time')
    
    context = {
        'worksheet': worksheet,
        'attempts': attempts,
    }
    return render(request, 'worksheets/worksheet_attempts.html', context)

@login_required
def delete_worksheet(request, worksheet_pk):
    # Fetch the worksheet, ensuring it belongs to the logged-in teacher
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk, created_by=request.user)
    
    if request.method == 'POST':
        # If the form is submitted, delete the object and redirect
        worksheet.delete()
        return redirect('teacher_dashboard')
        
    # If it's a GET request, show the confirmation page
    context = {'worksheet': worksheet}
    return render(request, 'worksheets/delete_confirm.html', context)