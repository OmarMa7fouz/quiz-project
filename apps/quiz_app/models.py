from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Category for organizing quizzes"""
    name = models.CharField(max_length=100, verbose_name='اسم الفئة')
    slug = models.SlugField(unique=True, verbose_name='الرابط')
    description = models.TextField(blank=True, verbose_name='الوصف')
    icon = models.CharField(max_length=50, blank=True, verbose_name='الأيقونة')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Quiz(models.Model):
    """Quiz model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'سهل'),
        ('medium', 'متوسط'),
        ('hard', 'صعب'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان الاختبار')
    slug = models.SlugField(unique=True, verbose_name='الرابط')
    description = models.TextField(verbose_name='الوصف')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes', verbose_name='الفئة')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name='مستوى الصعوبة')
    duration = models.IntegerField(default=30, verbose_name='المدة (بالدقائق)')
    pass_percentage = models.IntegerField(default=60, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='النسبة المطلوبة للنجاح')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes', verbose_name='أنشأه')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'اختبار'
        verbose_name_plural = 'الاختبارات'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def questions_count(self):
        return self.questions.count()
    
    @property
    def completion_rate(self):
        total_attempts = self.results.count()
        if total_attempts == 0:
            return 0
        completed = self.results.filter(completed=True).count()
        return int((completed / total_attempts) * 100)


class Question(models.Model):
    """Question model"""
    QUESTION_TYPES = [
        ('single', 'اختيار واحد'),
        ('multiple', 'اختيار متعدد'),
        ('true_false', 'صح أو خطأ'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name='الاختبار')
    question_text = models.TextField(verbose_name='نص السؤال')
    code_snippet = models.TextField(blank=True, null=True, verbose_name='مقتطف الكود')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single', verbose_name='نوع السؤال')
    points = models.IntegerField(default=1, verbose_name='النقاط')
    explanation = models.TextField(blank=True, verbose_name='الشرح')
    order = models.IntegerField(default=0, verbose_name='الترتيب')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'سؤال'
        verbose_name_plural = 'الأسئلة'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}"


class Answer(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='السؤال')
    answer_text = models.CharField(max_length=500, verbose_name='نص الإجابة')
    is_correct = models.BooleanField(default=False, verbose_name='إجابة صحيحة')
    order = models.IntegerField(default=0, verbose_name='الترتيب')
    
    class Meta:
        verbose_name = 'إجابة'
        verbose_name_plural = 'الإجابات'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.answer_text[:30]}"


class QuizResult(models.Model):
    """Quiz result for a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results', verbose_name='المستخدم')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results', verbose_name='الاختبار')
    score = models.IntegerField(default=0, verbose_name='النتيجة')
    total_points = models.IntegerField(default=0, verbose_name='مجموع النقاط')
    percentage = models.FloatField(default=0, verbose_name='النسبة المئوية')
    passed = models.BooleanField(default=False, verbose_name='نجح')
    time_taken = models.IntegerField(default=0, verbose_name='الوقت المستغرق (بالثواني)')
    completed = models.BooleanField(default=False, verbose_name='مكتمل')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'نتيجة اختبار'
        verbose_name_plural = 'نتائج الاختبارات'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.percentage}%"
    
    @property
    def correct_answers(self):
        return self.user_answers.filter(is_correct=True).count()
    
    @property
    def wrong_answers(self):
        return self.user_answers.filter(is_correct=False).count()


class UserAnswer(models.Model):
    """User's answer to a specific question"""
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='user_answers', verbose_name='نتيجة الاختبار')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='السؤال')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الإجابة المختارة')
    is_correct = models.BooleanField(default=False, verbose_name='صحيحة')
    points_earned = models.IntegerField(default=0, verbose_name='النقاط المكتسبة')
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'إجابة المستخدم'
        verbose_name_plural = 'إجابات المستخدمين'
        unique_together = ['quiz_result', 'question']
    
    def __str__(self):
        return f"{self.quiz_result.user.username} - {self.question.question_text[:30]}"
