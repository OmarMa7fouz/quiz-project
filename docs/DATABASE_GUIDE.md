# 🗄️ Database Guide for Beginners

> **Understanding the Quiz App Database Structure**

## Table of Contents
- [What is a Database?](#what-is-a-database)
- [Our Database Structure](#our-database-structure)
- [Database Tables Explained](#database-tables-explained)
- [How to View the Database](#how-to-view-the-database)
- [How to Add/Edit Data](#how-to-add-edit-data)
- [Common Database Operations](#common-database-operations)

---

## What is a Database?

### 🤔 Simple Explanation

A **database** is like a digital filing cabinet that stores information in organized tables.

Think of it like **Excel spreadsheets**:
- Each **table** = one spreadsheet
- Each **row** = one record (e.g., one question)
- Each **column** = one piece of information (e.g., question text)

### Our Database Type: SQLite

**SQLite** is a simple, file-based database perfect for development.

- ✅ No setup required
- ✅ Stored in one file: `db.sqlite3`
- ✅ Easy to backup (just copy the file)
- ✅ Great for learning and testing

**Location**: `C:\Users\USER\Downloads\My-Github\quiz-project\db.sqlite3`

---

## Our Database Structure

### 📊 Overview

Our quiz app has **2 main tables**:

```
┌─────────────────┐         ┌──────────────────┐
│   SUBJECTS      │         │    QUESTIONS     │
├─────────────────┤         ├──────────────────┤
│ • ID            │◄────────│ • ID             │
│ • Code          │         │ • Subject (FK)   │
│ • Name          │         │ • Question Text  │
│ • Description   │         │ • Option A       │
│ • Created At    │         │ • Option B       │
└─────────────────┘         │ • Option C       │
                            │ • Option D       │
     1 subject              │ • Correct Answer │
         ↕                  │ • Level          │
    many questions          │ • Explanation    │
                            │ • Created At     │
                            └──────────────────┘
```

**Relationship**: One Subject can have many Questions (One-to-Many)

---

## Database Tables Explained

### 📘 Table 1: SUBJECTS

**Purpose**: Stores information about quiz subjects (like AI, Multimedia, etc.)

**Structure**:
```
┌────┬──────────────┬─────────────────────────┬────────────────┬─────────────────────┐
│ ID │ Code         │ Name                    │ Description    │ Created At          │
├────┼──────────────┼─────────────────────────┼────────────────┼─────────────────────┤
│ 1  │ CSW351-AI    │ Artificial Intelligence │ Learn about AI │ 2024-10-18 10:30:00 │
│ 2  │ INT353-MM    │ Multimedia              │ Media concepts │ 2024-10-18 10:30:01 │
│ 3  │ CSW354-WEB   │ Web Technology          │ Web dev basics │ 2024-10-18 10:30:02 │
│ 4  │ CSW451-PP    │ Parallel Processing     │ Parallel comp  │ 2024-10-18 10:30:03 │
└────┴──────────────┴─────────────────────────┴────────────────┴─────────────────────┘
```

**Columns Explained**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | Integer | Unique identifier (auto-generated) | 1, 2, 3... |
| `code` | Text (50 chars) | Subject code (must be unique) | "CSW351-AI" |
| `name` | Text (100 chars) | Full subject name | "Artificial Intelligence" |
| `description` | Long Text | Subject description (optional) | "Learn about AI concepts" |
| `created_at` | DateTime | When subject was added | "2024-10-18 10:30:00" |

**In Django (`models.py`)**:
```python
class Subject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### 📗 Table 2: QUESTIONS

**Purpose**: Stores quiz questions with their options and correct answers

**Structure**:
```
┌────┬────────────┬──────────────────────────┬──────────┬──────────┬─────┬────────────┬────────────┐
│ ID │ Subject_ID │ Question Text            │ Option A │ Option B │ ... │ Correct    │ Level      │
├────┼────────────┼──────────────────────────┼──────────┼──────────┼─────┼────────────┼────────────┤
│ 1  │ 1          │ What is AI?              │ A thing  │ A robot  │ ... │ C          │ easy       │
│ 2  │ 1          │ What is ML?              │ Option A │ Option B │ ... │ B          │ medium     │
│ 3  │ 2          │ What is multimedia?      │ Option A │ Option B │ ... │ A          │ easy       │
└────┴────────────┴──────────────────────────┴──────────┴──────────┴─────┴────────────┴────────────┘
```

**Columns Explained**:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | Integer | Unique identifier | 1, 2, 3... |
| `subject_id` | Integer (Foreign Key) | Links to Subject table | 1 (points to CSW351-AI) |
| `question_text` | Long Text | The question | "What is machine learning?" |
| `option_a` | Text (500 chars) | First answer option | "A type of AI" |
| `option_b` | Text (500 chars) | Second answer option | "A robot" |
| `option_c` | Text (500 chars) | Third answer option | "A database" |
| `option_d` | Text (500 chars) | Fourth answer option | "A programming language" |
| `correct_answer` | Single Char | Correct option (A/B/C/D) | "A" |
| `level` | Text | Difficulty (easy/medium/hard) | "easy" |
| `explanation` | Long Text | Why answer is correct (optional) | "ML is a subset of AI..." |
| `created_at` | DateTime | When question was added | "2024-10-18 10:30:00" |

**In Django (`models.py`)**:
```python
class Question(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## Understanding Relationships

### 🔗 Foreign Keys (Connecting Tables)

A **Foreign Key** connects two tables together.

**Example**:
```
Subject Table:
┌────┬──────────────┬──────────────────────┐
│ ID │ Code         │ Name                 │
├────┼──────────────┼──────────────────────┤
│ 1  │ CSW351-AI    │ Artificial Intel...  │  ← This is referenced by questions
└────┴──────────────┴──────────────────────┘

Question Table:
┌────┬────────────┬──────────────────┐
│ ID │ Subject_ID │ Question Text    │
├────┼────────────┼──────────────────┤
│ 1  │ 1          │ What is AI?      │  ← Subject_ID = 1 links to Subject ID 1
│ 2  │ 1          │ What is ML?      │  ← Subject_ID = 1 links to Subject ID 1
│ 3  │ 2          │ What is MM?      │  ← Subject_ID = 2 links to Subject ID 2
└────┴────────────┴──────────────────┘
```

**In Code**:
```python
# Get a subject
subject = Subject.objects.get(code='CSW351-AI')

# Get all questions for this subject
questions = subject.questions.all()  # Django automatically provides this!
```

---

## How to View the Database

### Method 1: Django Admin Panel (Easiest) ⭐

**Step 1**: Create admin account (only once)
```bash
python manage.py createsuperuser
# Enter username, email, password
```

**Step 2**: Start server
```bash
python manage.py runserver
```

**Step 3**: Visit admin panel
```
http://127.0.0.1:8000/admin/
```

**Step 4**: Login and browse!

You'll see:
- List of all subjects
- List of all questions
- Add/Edit/Delete buttons
- Search and filter options

### Method 2: Using Python Script

Run the viewer script:
```bash
python scripts/view_database.py
```

This shows all data in a readable format.

### Method 3: Django Shell (For Developers)

```bash
python manage.py shell
```

Then run Python commands:
```python
# Import models
from apps.quiz_app.models import Subject, Question

# View all subjects
subjects = Subject.objects.all()
for subject in subjects:
    print(subject.code, subject.name)

# View all questions
questions = Question.objects.all()
print(f"Total questions: {questions.count()}")

# Get questions for specific subject
ai_questions = Question.objects.filter(subject__code='CSW351-AI')
print(f"AI questions: {ai_questions.count()}")

# Get only easy questions
easy_questions = Question.objects.filter(level='easy')
print(f"Easy questions: {easy_questions.count()}")
```

### Method 4: SQLite Browser (Advanced)

Download **DB Browser for SQLite**:
- Windows: https://sqlitebrowser.org/
- Open file: `db.sqlite3`
- Browse tables visually

---

## How to Add/Edit Data

### ✏️ Method 1: Django Admin (Recommended for Beginners)

**Adding a Subject**:
1. Go to http://127.0.0.1:8000/admin/
2. Click "Subjects" → "Add Subject"
3. Fill in:
   - Code: `CSW999-TEST`
   - Name: `Test Subject`
   - Description: `This is a test subject`
4. Click "Save"

**Adding a Question**:
1. Go to http://127.0.0.1:8000/admin/
2. Click "Questions" → "Add Question"
3. Fill in all fields
4. Select subject from dropdown
5. Choose difficulty level
6. Click "Save"

### 📝 Method 2: Python Script (Bulk Import)

Use the seed script to add many questions at once:

**Edit** `scripts/seed_database.py` and run:
```bash
python scripts/seed_database.py
```

**Example** (adding questions in script):
```python
from apps.quiz_app.models import Subject, Question

# Get or create subject
subject, created = Subject.objects.get_or_create(
    code='CSW351-AI',
    defaults={
        'name': 'Artificial Intelligence',
        'description': 'AI concepts and techniques'
    }
)

# Create question
question = Question.objects.create(
    subject=subject,
    question_text='What is machine learning?',
    option_a='A type of AI',
    option_b='A robot',
    option_c='A database',
    option_d='A programming language',
    correct_answer='A',
    level='easy',
    explanation='Machine learning is a subset of AI.'
)
```

### 🔧 Method 3: Management Script

Use the provided management script:
```bash
python scripts/manage_questions.py
```

Follow the prompts to add/edit questions interactively.

---

## Common Database Operations

### 🔍 Query Examples (Django ORM)

**ORM** = Object-Relational Mapping (fancy way to talk to database using Python)

#### Get All Records
```python
# Get all subjects
subjects = Subject.objects.all()

# Get all questions
questions = Question.objects.all()
```

#### Get One Record
```python
# Get subject by code
subject = Subject.objects.get(code='CSW351-AI')

# Get question by ID
question = Question.objects.get(id=1)
```

#### Filter Records
```python
# Get all easy questions
easy_questions = Question.objects.filter(level='easy')

# Get AI questions only
ai_questions = Question.objects.filter(subject__code='CSW351-AI')

# Get hard AI questions
hard_ai = Question.objects.filter(
    subject__code='CSW351-AI',
    level='hard'
)
```

#### Count Records
```python
# Count total questions
total = Question.objects.count()

# Count easy questions
easy_count = Question.objects.filter(level='easy').count()
```

#### Create Record
```python
# Create new subject
subject = Subject.objects.create(
    code='TEST101',
    name='Test Subject',
    description='For testing'
)
```

#### Update Record
```python
# Get question
question = Question.objects.get(id=1)

# Update field
question.question_text = 'Updated question text'
question.save()
```

#### Delete Record
```python
# Get and delete
question = Question.objects.get(id=1)
question.delete()
```

---

## Database File Management

### 📦 Backup Database

**Simple Copy** (recommended):
```bash
# Windows PowerShell
copy db.sqlite3 db_backup_2024-10-18.sqlite3

# Or manually copy the file
```

### 🔄 Reset Database (Start Fresh)

```bash
# 1. Delete database file
del db.sqlite3  # Windows

# 2. Delete migration files (except __init__.py)
# Go to: apps/quiz_app/migrations/
# Delete: 0001_initial.py, 0002_...py, etc.

# 3. Recreate database
python manage.py makemigrations
python manage.py migrate

# 4. Add data
python scripts/seed_database.py

# 5. Create admin user
python manage.py createsuperuser
```

### 📊 Export Data

```bash
# Export to JSON
python manage.py dumpdata quiz_app.Subject > subjects.json
python manage.py dumpdata quiz_app.Question > questions.json

# Export all
python manage.py dumpdata > full_backup.json
```

### 📥 Import Data

```bash
python manage.py loaddata subjects.json
python manage.py loaddata questions.json
```

---

## Understanding Migrations

### 🔄 What are Migrations?

**Migrations** = Instructions for changing database structure

Think of them as "version control for your database"

**When do you need migrations?**
- Adding a new field to a model
- Removing a field
- Creating a new model
- Changing field types

### Migration Workflow

```
Change models.py
      ↓
python manage.py makemigrations  ← Creates migration file
      ↓
python manage.py migrate         ← Applies changes to database
```

**Example**:
```python
# 1. Edit models.py - Add new field
class Question(models.Model):
    # ... existing fields ...
    tags = models.CharField(max_length=200)  # NEW FIELD

# 2. Run command
python manage.py makemigrations
# Creates: apps/quiz_app/migrations/0002_question_tags.py

# 3. Apply to database
python manage.py migrate
# Adds "tags" column to questions table
```

---

## Data Statistics

### 📊 Current Database Content

Our database contains:
- **4 Subjects** (AI, Multimedia, Web Tech, Parallel Processing)
- **360 Questions** (30 per difficulty level per subject)
  - 120 Easy questions
  - 120 Medium questions
  - 120 Hard questions

### View Statistics

Use Python shell:
```python
from apps.quiz_app.models import Subject, Question

# Total questions
print(f"Total: {Question.objects.count()}")

# Questions per subject
for subject in Subject.objects.all():
    count = subject.questions.count()
    print(f"{subject.code}: {count} questions")

# Questions per level
for level in ['easy', 'medium', 'hard']:
    count = Question.objects.filter(level=level).count()
    print(f"{level.title()}: {count} questions")
```

---

## Troubleshooting

### ❌ Problem: "no such table: quiz_app_question"

**Solution**: Run migrations
```bash
python manage.py migrate
```

### ❌ Problem: "Database is locked"

**Solution**: 
- Close Django admin panel
- Stop the server (Ctrl+C)
- Close DB Browser if open
- Restart server

### ❌ Problem: "No questions in database"

**Solution**: Seed the database
```bash
python scripts/seed_database.py
```

### ❌ Problem: "Foreign key constraint failed"

**Solution**: Make sure subject exists before adding questions
```python
# WRONG - Subject might not exist
question = Question.objects.create(
    subject_id=999,  # This subject doesn't exist!
    # ...
)

# RIGHT - Get existing subject
subject = Subject.objects.get(code='CSW351-AI')
question = Question.objects.create(
    subject=subject,
    # ...
)
```

---

## Best Practices

### ✅ Do's

- ✅ Always backup database before major changes
- ✅ Use Django admin for small edits
- ✅ Use scripts for bulk operations
- ✅ Test queries in shell before using in code
- ✅ Run migrations after model changes
- ✅ Keep backups of migration files

### ❌ Don'ts

- ❌ Don't edit `db.sqlite3` directly
- ❌ Don't delete migration files unless resetting
- ❌ Don't skip migrations
- ❌ Don't use raw SQL unless necessary
- ❌ Don't forget to save changes (`.save()`)

---

## Quick Reference

### Essential Commands

```bash
# View database
python manage.py shell
python scripts/view_database.py

# Access admin panel
python manage.py runserver
# Visit: http://127.0.0.1:8000/admin/

# Migrations
python manage.py makemigrations
python manage.py migrate

# Seed data
python scripts/seed_database.py

# Backup
copy db.sqlite3 backup.sqlite3
```

### Common Queries

```python
# Import
from apps.quiz_app.models import Subject, Question

# Count
Question.objects.count()

# Get all
Subject.objects.all()

# Filter
Question.objects.filter(level='easy')

# Get one
Subject.objects.get(code='CSW351-AI')

# Create
Subject.objects.create(code='TEST', name='Test')
```

---

## Learning Path

### For Complete Beginners

1. ✅ Understand what a database is (you're here!)
2. ✅ Use Django admin to view data
3. ✅ Practice simple queries in Django shell
4. ✅ Learn to add questions via admin
5. ✅ Try writing simple filter queries

### Next Steps

1. Read Django ORM documentation
2. Learn about database relationships
3. Practice writing complex queries
4. Learn about database optimization
5. Study migration system in detail

---

## Helpful Resources

- **Django Models**: https://docs.djangoproject.com/en/stable/topics/db/models/
- **Django ORM**: https://docs.djangoproject.com/en/stable/topics/db/queries/
- **Migrations**: https://docs.djangoproject.com/en/stable/topics/migrations/

---

## 📞 Need Help?

**Quick Checklist**:
- [ ] Is the server running?
- [ ] Have you run migrations?
- [ ] Is there data in the database?
- [ ] Are you in the right directory?

**Still stuck?** Check error messages carefully - they usually tell you exactly what's wrong!

Remember: Databases are just organized storage. Take it step by step! 🚀

