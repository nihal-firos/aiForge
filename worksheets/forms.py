# worksheets/forms.py
from django import forms

class WorksheetGeneratorForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g., Science'}))
    grade_level = forms.CharField(max_length=50, required=True, label="Grade Level", widget=forms.TextInput(attrs={'placeholder': 'e.g., 8th Grade'}))
    topic = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g., The Solar System'}))
    num_mcq = forms.IntegerField(min_value=0, initial=5, label="Number of Multiple Choice Questions")
    num_short_answer = forms.IntegerField(min_value=0, initial=3, label="Number of Short Answer Questions")