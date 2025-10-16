from django.contrib import admin
from .models import Category, Quiz, Question, Answer, QuizResult, UserAnswer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['answer_text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['quiz', 'question_type']
    search_fields = ['question_text']
    inlines = [AnswerInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ['question_text', 'code_snippet', 'question_type', 'points', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    fields = ['question', 'selected_answer', 'is_correct', 'points_earned']
    readonly_fields = ['is_correct', 'points_earned']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'passed', 'completed', 'started_at']
    list_filter = ['passed', 'completed', 'quiz']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['score', 'percentage', 'passed']
    inlines = [UserAnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer_text', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['answer_text', 'question__question_text']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_result', 'question', 'selected_answer', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'quiz_result__quiz']
    search_fields = ['quiz_result__user__username', 'question__question_text']
