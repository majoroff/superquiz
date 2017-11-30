# coding: utf-8
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Test, Question, Answer, Result


def home_view(request):
    """
    Базовый view показывает ничего неаутентифицированному пользователю
    или список доступных тестов аутентифицированному
    """
    context = {}
    if request.user.is_authenticated():
        test_passed = Result.objects.values('test_id').filter(user=request.user)
        tests = Test.objects.exclude(id__in=test_passed)
        context['tests'] = tests
    return render(request, 'home.html', context)


def quiz_view(request, test_id=0):

    if request.method == 'POST':
        # тест выполнен в виде формы, передается методом POST
        
        # копируем ответы в отдельный словарь, попутно убирая
        # лишние элементы
        ans = dict(request.POST)
        ans.pop('csrfmiddlewaretoken')
        test_id = int(ans.pop('test_id')[0])
        test = get_object_or_404(Test, pk=test_id)

        if len(ans) != test.question_set.count():
            # полученное количество ответов должно совпадать
            # c количеством вопросов теста, иначе ошибка
            ## в будущем нужно реализовать сохранение указанных
            ## ответов теста в этом месте, сейчас всё сбрасывается
            messages.error(request, 'Нужно ответить на все вопросы')

        user_right = 0
        user_wrong = 0
        # если получены ответы на все вопросы - начинаем их проверку
        # в POST ключ представляет собой id вопроса, значение - список (id) указанных пользователем ответов
        for k, v in ans.items():
            # берем вопрос и айдишки правильных ответов на него из базы
            question = get_object_or_404(Question, pk=int(k))
            right_answers = [ a.id for a in Answer.objects.filter(question=question, right=True)]

            # составляем список указанных пользователем ответов с проверкой на существование id
            answers = []
            for a in v:
                temp = get_object_or_404(Answer, pk=int(a))
                answers.append(temp.id)

            # если два полученных списка ответов равны, то пользователь ответил правильно
            # увеличиваем соответствующие счетчики
            if answers == right_answers:
                user_right += 1
            else:
                user_wrong += 1
        # и создаем объект результата
        Result.objects.create(user=request.user, test=test, right=user_right, wrong=user_wrong)
        return redirect('/')

    else:
        if test_id:
            test = get_object_or_404(Test, pk=int(test_id))
            questions = Question.objects.filter(test=test)
            return render(request, 'quiz.html', {'questions': questions, "test_id": test.id})
        else:
            raise Http404


def signup(request):
    """
    Стандартный view создания пользователя
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
