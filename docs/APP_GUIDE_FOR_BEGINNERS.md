# 🎓 Quiz App Guide for Beginners

> **A complete guide for team members with no Django experience**

## Table of Contents
- [What is Django?](#what-is-django)
- [How This App Works](#how-this-app-works)
- [Project Structure Explained](#project-structure-explained)
- [The Request-Response Flow](#the-request-response-flow)
- [Key Concepts](#key-concepts)
- [How to Make Changes](#how-to-make-changes)

---

## What is Django?

**Django** is a web framework for Python that helps you build websites and web applications quickly.

Think of it like this:
- **Python** = The programming language (like English for computers)
- **Django** = A toolkit that gives you pre-built components for websites (like LEGO blocks)

### Why Django?
- ✅ Handles complex tasks automatically (database, security, user management)
- ✅ Follows a clear pattern (makes code organized and predictable)
- ✅ Has excellent documentation and community support

---

## How This App Works

### 🎯 What Does This App Do?

This is a **Quiz Application** where:
1. Users select a **subject** (like AI, Multimedia, etc.)
2. Users choose a **difficulty level** (Easy, Medium, Hard)
3. The app shows **10 random questions**
4. Users submit answers and see their **score immediately**

### 🔄 User Journey (Step-by-Step)

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────┐
│   Home Page │─────▶│ Select Difficulty│─────▶│  Take Quiz     │
│ (Choose     │      │ (Easy/Medium/    │      │ (10 Questions) │
│  Subject)   │      │  Hard)           │      │                │
└─────────────┘      └──────────────────┘      └────────────────┘
                                                         │
                                                         ▼
                                                ┌────────────────┐
                                                │   See Results  │
                                                │  (Score & Ans) │
                                                └────────────────┘
```

---

## Project Structure Explained

Let's break down what each folder and file does:

```
quiz-project/
├── 📁 apps/quiz_app/          # Main application folder
│   ├── models.py              # Database tables (what data we store)
│   ├── views.py               # Logic (what happens when user clicks)
│   ├── urls.py                # Routes (which URL leads where)
│   ├── templates/             # HTML files (what users see)
│   ├── static/                # CSS, JavaScript, images
│   └── admin.py               # Admin panel configuration
│
├── 📁 my_quiz_project/        # Project settings folder
│   ├── settings.py            # All configurations
│   └── urls.py                # Main URL routing
│
├── 📁 scripts/                # Helper scripts
│   ├── seed_database.py       # Adds sample data
│   └── view_database.py       # View what's in database
│
├── 📁 docs/                   # Documentation (you're here!)
├── db.sqlite3                 # Database file (stores all data)
├── manage.py                  # Django command tool
└── requirements.txt           # List of needed Python packages
```

### 🔑 Most Important Files

| File | What It Does | Example |
|------|--------------|---------|
| `models.py` | Defines database structure | "A Question has text, 4 options, and correct answer" |
| `views.py` | Contains logic for each page | "When user visits quiz page, fetch 10 questions" |
| `urls.py` | Maps URLs to views | "/quiz/AI/easy" → shows AI easy quiz |
| `templates/*.html` | HTML pages users see | Quiz page with questions and buttons |

---

## The Request-Response Flow

### How Django Handles a User Request

```
User types URL in browser
        ↓
    urls.py (finds matching route)
        ↓
    views.py (runs the function)
        ↓
    models.py (gets data from database)
        ↓
    views.py (prepares data)
        ↓
    templates/*.html (fills HTML with data)
        ↓
    Browser (shows page to user)
```

### 📝 Real Example: Taking a Quiz

Let's trace what happens when a user visits:
**`http://127.0.0.1:8000/quiz/CSW351-AI/easy/`**

#### Step 1: URL Routing (`urls.py`)
```python
# Django looks at this line in urls.py:
path('quiz/<str:subject_code>/<str:level>/', views.take_quiz, name='take_quiz')

# It extracts:
# subject_code = "CSW351-AI"
# level = "easy"
# Then calls: views.take_quiz(request, "CSW351-AI", "easy")
```

#### Step 2: View Logic (`views.py`)
```python
def take_quiz(request, subject_code, level):
    # 1. Get the subject from database
    subject = Subject.objects.get(code=subject_code)
    
    # 2. Get 10 random questions for this subject and level
    questions = get_random_questions(subject_code, level, num_questions=10)
    
    # 3. Prepare data to send to template
    context = {
        'subject': subject,
        'level': level,
        'questions': questions,
    }
    
    # 4. Render HTML template with data
    return render(request, 'quiz.html', context)
```

#### Step 3: Database Query (`models.py`)
```python
# get_random_questions() does:
# 1. Find the subject in database
subject = Subject.objects.get(code="CSW351-AI")

# 2. Get all questions for this subject and level
all_questions = Question.objects.filter(subject=subject, level="easy")

# 3. Shuffle them and pick 10
random.shuffle(all_questions)
return all_questions[:10]
```

#### Step 4: Template Rendering (`quiz.html`)
```html
<!-- Django fills in {{ variables }} with real data -->
<h1>{{ subject.name }} - {{ level }} Quiz</h1>

{% for question in questions %}
    <p>{{ question.question_text }}</p>
    <input type="radio" value="A"> {{ question.option_a }}
    <input type="radio" value="B"> {{ question.option_b }}
    <!-- ... -->
{% endfor %}
```

#### Step 5: User Sees
```
┌──────────────────────────────────────┐
│  CSW351-AI - Easy Quiz               │
│                                      │
│  Question 1: What is machine...?     │
│  ○ A. Option A                       │
│  ○ B. Option B                       │
│  ○ C. Option C                       │
│  ○ D. Option D                       │
│                                      │
│  [Submit Answers]                    │
└──────────────────────────────────────┘
```

---

## Key Concepts

### 1. 🗄️ Models (Database Tables)

**What**: Python classes that become database tables

**Example**:
```python
class Subject(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
```

**Becomes this database table**:
```
Subjects Table:
┌────┬──────────────┬─────────────────────┐
│ ID │ Code         │ Name                │
├────┼──────────────┼─────────────────────┤
│ 1  │ CSW351-AI    │ Artificial Intel... │
│ 2  │ INT353-MM    │ Multimedia          │
└────┴──────────────┴─────────────────────┘
```

### 2. 📋 Views (Logic)

**What**: Python functions that handle user requests

**Example**:
```python
def home(request):
    # Get all subjects from database
    subjects = Subject.objects.all()
    
    # Return HTML page with subjects
    return render(request, 'home.html', {'subjects': subjects})
```

**Does**: Fetches data → Prepares it → Sends to template

### 3. 🌐 URLs (Routes)

**What**: Maps web addresses to view functions

**Example**:
```python
urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<str:subject_code>/<str:level>/', views.take_quiz),
]
```

**Means**:
- `http://127.0.0.1:8000/` → calls `home()`
- `http://127.0.0.1:8000/quiz/CSW351-AI/easy/` → calls `take_quiz()`

### 4. 📄 Templates (HTML Pages)

**What**: HTML files with Django template language

**Example**:
```html
<!-- Static HTML -->
<h1>Quiz Results</h1>

<!-- Dynamic content (filled by Django) -->
<p>You scored {{ correct_count }} out of {{ total_questions }}</p>

<!-- Loop through data -->
{% for question in questions %}
    <p>{{ question.question_text }}</p>
{% endfor %}
```

### 5. 🎨 Static Files (CSS, JS, Images)

**What**: Files that don't change (stylesheets, scripts, images)

**Location**: `apps/quiz_app/static/`

**Example**:
```html
<!-- In HTML template -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
<script src="{% static 'js/quiz.js' %}"></script>
```

---

## How to Make Changes

### ✏️ Common Tasks

#### 1. Add a New Page

**Step 1**: Create view in `views.py`
```python
def my_new_page(request):
    return render(request, 'my_new_page.html')
```

**Step 2**: Add URL in `urls.py`
```python
path('my-page/', views.my_new_page, name='my_page'),
```

**Step 3**: Create template `templates/my_new_page.html`
```html
{% extends 'base.html' %}
{% block content %}
    <h1>My New Page</h1>
{% endblock %}
```

**Step 4**: Visit `http://127.0.0.1:8000/my-page/`

#### 2. Change How a Page Looks

Edit the HTML file in `apps/quiz_app/templates/`

Example: Make quiz title bigger
```html
<!-- Before -->
<h2>{{ subject.name }}</h2>

<!-- After -->
<h1 style="font-size: 3em;">{{ subject.name }}</h1>
```

#### 3. Add a New Field to Database

**Step 1**: Edit `models.py`
```python
class Question(models.Model):
    question_text = models.TextField()
    # NEW FIELD:
    difficulty_points = models.IntegerField(default=1)
```

**Step 2**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4. Change Website Colors/Styles

Edit `apps/quiz_app/static/css/custom.css`

```css
/* Change button color */
.btn-primary {
    background-color: #ff5733;
}

/* Change text size */
body {
    font-size: 18px;
}
```

---

## 🛠️ Essential Commands

| Command | What It Does |
|---------|--------------|
| `python manage.py runserver` | Starts the website (visit http://127.0.0.1:8000) |
| `python manage.py makemigrations` | Prepares database changes |
| `python manage.py migrate` | Applies database changes |
| `python manage.py createsuperuser` | Creates admin account |
| `python scripts/seed_database.py` | Adds sample quiz questions |
| `python scripts/view_database.py` | Shows what's in database |

---

## 🐛 Troubleshooting

### Problem: "Page not found (404)"
- **Check**: Is the URL spelled correctly?
- **Check**: Is there a matching path in `urls.py`?

### Problem: "No such table"
- **Fix**: Run migrations
```bash
python manage.py migrate
```

### Problem: "No questions showing"
- **Fix**: Seed the database
```bash
python scripts/seed_database.py
```

### Problem: Changes don't appear
- **Fix**: Refresh browser (Ctrl+F5)
- **Fix**: Restart server (Ctrl+C, then `python manage.py runserver`)

---

## 📚 Learning Resources

### For Complete Beginners
1. **Django Official Tutorial**: https://docs.djangoproject.com/en/stable/intro/tutorial01/
2. **Python Basics**: https://www.python.org/about/gettingstarted/

### For This Project
- Read `docs/DATABASE_GUIDE.md` - Understanding the database
- Read `docs/HOW_TO_ADD_QUESTIONS.md` - Adding quiz questions
- Read `docs/API_DOCUMENTATION.md` - Using the API

---

## 🎯 Quick Reference

### Django MVT Pattern
```
Model (models.py)     → Database structure
View (views.py)       → Logic/Processing  
Template (*.html)     → What user sees
```

### File Naming Conventions
- Python files: `lowercase_with_underscores.py`
- HTML files: `lowercase.html` or `snake_case.html`
- CSS/JS files: `lowercase.css`, `camelCase.js`

### Important Locations
- **Code**: `apps/quiz_app/`
- **HTML**: `apps/quiz_app/templates/`
- **Styles**: `apps/quiz_app/static/css/`
- **Database**: `db.sqlite3` (root folder)
- **Settings**: `my_quiz_project/settings.py`

---

## 📞 Need Help?

1. Check error messages carefully (they tell you what's wrong!)
2. Read the relevant documentation file in `docs/`
3. Try searching the error message online
4. Ask your team lead or senior developer

**Remember**: Everyone starts as a beginner. Don't be afraid to ask questions! 🚀

