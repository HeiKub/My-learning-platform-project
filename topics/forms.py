# topics/forms.py
from django import forms
from .models import Material, Quiz, Question, UserAnswer

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'material_type', 'content_file', 'video_url', 'link_url']


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['topic', 'name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['selected_answer']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')  
        super().__init__(*args, **kwargs)
        
        self.fields['selected_answer'] = forms.ChoiceField(
            choices=[(option, option) for option in question.get_answer_options()],
            widget=forms.RadioSelect, 
            label=question.question_text
        )