from django.db import models
import random


class Subject(models.Model):
    """Stores subjects only"""
    code = models.CharField(max_length=50, unique=True, verbose_name='Subject Code')
    name = models.CharField(max_length=100, verbose_name='Subject Name')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def total_questions(self):
        """Get total number of questions for this subject"""
        return self.questions.count()
    
    def questions_by_level(self, level):
        """Get questions filtered by difficulty level"""
        return self.questions.filter(level=level)


class Question(models.Model):
    """Stores questions for each subject"""
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', verbose_name='Subject')
    question_text = models.TextField(verbose_name='Question Text')
    option_a = models.CharField(max_length=500, verbose_name='Option A')
    option_b = models.CharField(max_length=500, verbose_name='Option B')
    option_c = models.CharField(max_length=500, verbose_name='Option C')
    option_d = models.CharField(max_length=500, verbose_name='Option D')
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ], verbose_name='Correct Answer')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy', verbose_name='Difficulty Level')
    explanation = models.TextField(blank=True, verbose_name='Explanation')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['subject', 'level', 'id']

    def __str__(self):
        return f"{self.subject.code} [{self.level}] - {self.question_text[:50]}"
    
    def get_options(self):
        """Get formatted options dictionary"""
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d
        }
    
    @property
    def points(self):
        """Get points based on difficulty level"""
        points_map = {'easy': 1, 'medium': 2, 'hard': 3}
        return points_map.get(self.level, 1)
    
    def get_options(self):
        """Returns all options as a dictionary"""
        return {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }
    
    def check_answer(self, selected_option):
        """Check if the selected option is correct"""
        return selected_option.upper() == self.correct_answer


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_random_questions(subject_code, level='easy', num_questions=10):
    """
    Returns random questions each refresh
    
    Args:
        subject_code (str): Subject code (e.g., 'CSW351-AI')
        level (str): Difficulty level ('easy', 'medium', 'hard')
        num_questions (int): Number of questions to return
    
    Returns:
        List of Question objects
    """
    try:
        subject = Subject.objects.get(code=subject_code)
        all_questions = list(Question.objects.filter(subject=subject, level=level))
        
        if not all_questions:
            return []
        
        # Shuffle and return random questions
        random.shuffle(all_questions)
        return all_questions[:num_questions]
    except Subject.DoesNotExist:
        return []


def get_all_subjects():
    """Get all available subjects"""
    return Subject.objects.all()


def get_subject_levels(subject_code):
    """Get available difficulty levels for a subject"""
    try:
        subject = Subject.objects.get(code=subject_code)
        levels = Question.objects.filter(subject=subject).values_list('level', flat=True).distinct()
        return list(levels)
    except Subject.DoesNotExist:
        return []
