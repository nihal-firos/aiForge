# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Profile

def register(request):
    if request.user.is_authenticated:
        return redirect('/') # Or to their respective dashboard

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            
            # Create the user profile with the selected role
            Profile.objects.create(user=new_user, role=form.cleaned_data['role'])
            
            # Log the user in and redirect to the appropriate dashboard
            login(request, new_user)
            if new_user.profile.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    """
    Redirects users to the appropriate page based on their role and authentication status.
    """
    if request.user.is_authenticated:
        # Use a try-except block to handle users that might not have a profile (e.g., superuser)
        try:
            if request.user.profile.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        except AttributeError:
            # Default redirect for users without a profile, like an admin
            return redirect('teacher_dashboard')
    else:
        # If not logged in, redirect to the login page
        return redirect('login')