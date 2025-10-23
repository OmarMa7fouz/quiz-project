from django.contrib import admin
from .models import Subject, Question


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin interface for Subject model"""
    list_display = ['code', 'name', 'total_questions', 'created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']
    
    def total_questions(self, obj):
        return obj.total_questions()
    total_questions.short_description = 'Total Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model"""
    list_display = ['subject', 'question_preview', 'level', 'correct_answer', 'created_at']
    list_filter = ['subject', 'level', 'correct_answer']
    search_fields = ['question_text', 'subject__code', 'subject__name']
    ordering = ['subject', 'level', '-created_at']
    
    fieldsets = (
        ('Question Information', {
            'fields': ('subject', 'question_text', 'level')
        }),
        ('Answer Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')
        }),
        ('Additional Information', {
            'fields': ('explanation',),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        """Show first 80 characters of question"""
        return obj.question_text[:80] + '...' if len(obj.question_text) > 80 else obj.question_text
    question_preview.short_description = 'Question'
    
    def save_model(self, request, obj, form, change):
        """Validate correct answer before saving"""
        if obj.correct_answer not in ['A', 'B', 'C', 'D']:
            obj.correct_answer = obj.correct_answer.upper()
        super().save_model(request, obj, form, change)


# Customize admin site header
admin.site.site_header = 'Quiz System Administration'
admin.site.site_title = 'Quiz Admin'
admin.site.index_title = 'Manage Subjects and Questions'
