# Classroom AI 🚀

**Your AI Teaching Assistant. Intelligent Worksheet Generation and Grading.**

![Classroom AI Cover Image](https://user-images.githubusercontent.com/your-username/your-repo/blob/main/path-to-your-cover-image.png)
*(To use the cover image, upload it to your GitHub repository and replace the link above.)*

## About The Project

**Classroom AI** is an intelligent web application designed to be a dedicated teacher's assistant, automating the time-consuming tasks of creating and grading educational materials. Built with a robust Django backend and a modern user interface, this platform empowers educators to reclaim valuable time for teaching.

Checkout: https://aiforge-jyst.onrender.com

By handling the time-consuming aspects of content creation and evaluation, Classroom AI frees up educators to focus on what matters most: teaching, mentoring, and inspiring their students.

## Key Features ✨

* **AI Worksheet Generation**: Instantly generate custom worksheets and exams with multiple-choice and short-answer questions tailored to any subject, topic, and grade level using the Gemini API.
* **Role-Based System**: Separate, secure dashboards and permissions for **Teachers** and **Students**.
* **Teacher Dashboard**: A central hub for teachers to create, manage, and delete their own worksheets, review student attempts, and view class analytics.
* **Student Exam Platform**: A clean, modern interface for students to take exams online.
* **Automated & AI-Powered Grading**: Instantly grades multiple-choice questions and uses AI for nuanced evaluation of subjective answers, providing constructive feedback.
* **AI Originality Checker**: An integrated tool to analyze student submissions for originality and signs of being AI-generated.
* **PDF Export**: Download any generated worksheet as a PDF for offline use.

## Tech Stack 🛠️

* **Backend**: Django, Python
* **Frontend**: HTML, Tailwind CSS (via CDN)
* **Database**: PostgreSQL (Production), SQLite3 (Development)
* **AI Services**: Google Gemini API
* **Deployment**: Render, Gunicorn

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.8+
* Git

### Local Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your secret keys:
    ```
    GEMINI_API_KEY="your_google_gemini_api_key"
    SECRET_KEY="your_django_development_secret_key"
    ```

5.  **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

6.  **Create a superuser:**
    This will be your first admin/teacher account.
    ```sh
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```
    Your project will be available at `http://127.0.0.1:8000/`.

## Deployment

This application is configured for deployment on **Render**. The deployment process uses `gunicorn` as the web server and `whitenoise` for serving static files. The `build.sh` script in the repository automates the build process on Render by running `collectstatic` and `migrate` commands.

Key environment variables for production include `SECRET_KEY`, `DATABASE_URL`, `GEMINI_API_KEY`, and `DEBUG=False`.
