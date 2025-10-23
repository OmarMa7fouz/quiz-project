from rest_framework import serializers
from .models import Subject, Question


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    total_questions = serializers.SerializerMethodField()
    levels_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'description', 'total_questions', 'levels_available']
    
    def get_total_questions(self, obj):
        """Get total number of questions for this subject"""
        return obj.total_questions()
    
    def get_levels_available(self, obj):
        """Get available levels with question counts"""
        levels = []
        for level in ['easy', 'medium', 'hard']:
            count = obj.questions_by_level(level).count()
            if count > 0:
                levels.append({
                    'level': level,
                    'count': count,
                    'display': level.title()
                })
        return levels


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'subject_code', 'subject_name', 'question_text', 
            'option_a', 'option_b', 'option_c', 'option_d', 
            'correct_answer', 'level', 'explanation', 'created_at', 'options'
        ]
    
    def get_options(self, obj):
        """Get formatted options"""
        return {
            'A': obj.option_a,
            'B': obj.option_b,
            'C': obj.option_c,
            'D': obj.option_d
        }


class QuizRequestSerializer(serializers.Serializer):
    """Serializer for quiz request"""
    subject_code = serializers.CharField(max_length=50)
    level = serializers.ChoiceField(choices=['easy', 'medium', 'hard'])
    num_questions = serializers.IntegerField(default=10, min_value=1, max_value=30)


class QuizAnswerSerializer(serializers.Serializer):
    """Serializer for quiz answers"""
    question_id = serializers.IntegerField()
    selected_answer = serializers.CharField(max_length=1)


class QuizSubmissionSerializer(serializers.Serializer):
    """Serializer for quiz submission"""
    answers = serializers.ListField(
        child=QuizAnswerSerializer(),
        allow_empty=False
    )
    
    def validate_answers(self, value):
        """Validate that answers are unique"""
        question_ids = [answer['question_id'] for answer in value]
        if len(question_ids) != len(set(question_ids)):
            raise serializers.ValidationError("Duplicate question IDs found")
        return value


class QuizResultSerializer(serializers.Serializer):
    """Serializer for quiz results"""
    total_questions = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    incorrect_count = serializers.IntegerField()
    percentage = serializers.FloatField()
    results = serializers.ListField()
    time_taken = serializers.CharField(required=False)
