# topics/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Material, Quiz, Question, UserResult, UserAnswer
from .forms import MaterialForm, QuizForm, QuestionForm, UserAnswerForm

@login_required
def topic_list(request):
    topics = Topic.objects.order_by('name')
    return render(request, 'topics/topic_list.html', {'topics': topics})

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quizzes = topic.quizzes.all()
    materials = Material.objects.filter(topic=topic, is_approved = True)
    
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.topic = topic
            material.is_approved = False
            material.uploaded_by = request.user
            material.save()
            return redirect('topic-detail', topic_id=topic.id)
    else:
        form = MaterialForm()

    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'materials': materials,
        'form': form,
        'quizzes': quizzes
    
    })


def quizzes_for_topic(request, topic_id):
    topic = get_object_or_404(Topic, id= topic_id)

    quizzes = topic.quizzes.all()
    return render(request, 'topics/quizzes_for_topic.html', {'topic': topic,'quizzes':quizzes})



def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question.all()  # Fetch all questions related to this quiz

    if request.method == 'POST':
        forms = []
        for question in questions:
            form = UserAnswerForm(request.POST, question=question)
            if form.is_valid():
                # Create the UserAnswer object for this user and question
                user_answer = form.save(commit=False)
                user_answer.user = request.user
                user_answer.question = question
                user_answer.save()
            forms.append(form)

        # Once all answers are submitted, calculate the user's score
        user_result, created = UserResult.objects.get_or_create(user=request.user, topic=quiz.topic)
        user_result.calculate_score()  # Update the score
        user_result.save()

        # Redirect to the quiz result view
        return redirect('quiz_result', quiz_id=quiz.id)

    else:
        # If it's a GET request, we generate the form for each question
        forms = [UserAnswerForm(question=question) for question in questions]

    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'forms': forms})








def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__quiz=quiz)
    
    # Collect the correct answers for each question
    questions = Question.objects.filter(quiz=quiz)
    correct_answers = {question.id: question.correct_answer for question in questions}
    
    # Calculate score
    score = user_answers.filter(is_correct=True).count()
    
    # Prepare context data
    result = {
        'score': score,
        'correct_answers': correct_answers,
        'user_answers': {answer.question.id: answer.selected_answer for answer in user_answers},
    }

    return render(request, 'quizzes/quiz_result.html', {
        'quiz': quiz,
        'result': result,
    })