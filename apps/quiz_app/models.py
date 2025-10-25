from django.db import models
import random


class Subject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def total_questions(self):
        return self.questions.count()
    
    def questions_by_level(self, level):
        return self.questions.filter(level=level)


class Question(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subject', 'level', 'id']

    def __str__(self):
        return f"{self.subject.code} [{self.level}] - {self.question_text[:50]}"
    
    @property
    def points(self):
        points_map = {'easy': 1, 'medium': 2, 'hard': 3}
        return points_map.get(self.level, 1)
    
    def get_options(self):
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }
    
    def check_answer(self, selected_option):
        return selected_option.upper() == self.correct_answer


# Utility functions
def get_random_questions(subject_code, level='easy', num_questions=10):
    try:
        subject = Subject.objects.get(code=subject_code)
        all_questions = list(Question.objects.filter(subject=subject, level=level))
        if not all_questions:
            return []
        random.shuffle(all_questions)
        return all_questions[:num_questions]
    except Subject.DoesNotExist:
        return []


def get_all_subjects():
    return Subject.objects.all()


def get_subject_levels(subject_code):
    try:
        subject = Subject.objects.get(code=subject_code)
        levels = Question.objects.filter(subject=subject).values_list('level', flat=True).distinct()
        return list(levels)
    except Subject.DoesNotExist:
        return []
