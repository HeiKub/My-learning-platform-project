from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=250,unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name
    
class Material(models.Model):  
    MATERIAL_TYPES = [
        ('file', 'File'),
        ('video', 'Video'),
        ('link', 'Link'),
    ]

    topic = models.ForeignKey(Topic, on_delete= models.CASCADE)
    title = models.CharField(max_length=50)
    material_type = models.CharField(max_length=20, choices = MATERIAL_TYPES)
    content_file = models.FileField(
    upload_to = 'materials/', blank= True, null = True)
    video_url = models.URLField(blank = True, null = True)
    link_url = models.URLField(blank = True, null = True)
    is_approved = models.BooleanField(default = False) 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name ='quizzes')
    name = models.CharField(max_length=20)    

    def __str__(self):
        return self.name
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE, related_name ='question')
    question_text = models.CharField(max_length=300) 
    correct_answer = models.CharField(max_length=255, default="No option")
  # Assume correct answer is stored here

    # Example of multiple answer options (you need to add this or something similar)
    option_1 = models.CharField(max_length=255,default="No option")
    option_2 = models.CharField(max_length=255,default="No option")
    option_3 = models.CharField(max_length=255,default="No option")
    option_4 = models.CharField(max_length=255,default="No option")

    def get_answer_options(self):
        # Return a list of all the answer options
        return [self.option_1, self.option_2, self.option_3, self.option_4]

    def __str__(self):
        return self.question_text 
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    selected_answer = models.CharField(max_length=255)  
    is_correct = models.BooleanField()  #True or False 

    def save(self, *args, **kwargs):
        
        self.is_correct = (self.selected_answer == self.question.correct_answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text} - Correct: {self.is_correct}"



class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_results')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_results')
    score = models.IntegerField(default=0) 

    def calculate_score(self):
        # Calculate the score based on correct answers
        correct_answers = UserAnswer.objects.filter(user=self.user, question__quiz__topic=self.topic, is_correct=True).count()
        total_questions = Question.objects.filter(quiz__topic=self.topic).count()
        self.score = correct_answers
        return self.score

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - Score: {self.score}"
    