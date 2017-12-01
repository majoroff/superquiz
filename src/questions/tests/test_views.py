import random

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from questions.models import Test, Result

User = get_user_model()


class HomePageTest(TestCase):

    def test_root_url_renders_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')



class AuthTest(TestCase):
    
    # стандартные проверки механизмов создания аккаунта и входа
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'

    def test_signup_renders_form(self):
        response = self.client.get('/signup/')
        self.assertTemplateUsed(response, 'signup.html')

    def test_POST_signup(self):
        response = self.client.post('/signup/', {'username': self.username, 'password1': self.password, 'password2': self.password}, follow=True)
        newby = User.objects.last()
        self.assertEqual(newby.username, self.username)
        self.assertTrue(response.context['user'].is_authenticated())

    def test_login_renders_form(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_POST_login(self):
        User.objects.create_user(username=self.username, password=self.password)        
        response = self.client.post('/login/', {'username': self.username, 'password': self.password}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated())

    def test_login_required_for_quiz(self):
        quiz_url = reverse('quiz', kwargs={'test_id': 0})
        response = self.client.get(quiz_url)
        self.assertRedirects(response, '/login/?next=%s' % quiz_url)


class QuizTest(TestCase):

    fixtures = ['quizes.json']

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'

        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)


    def test_user_gets_available_quizes(self):
        # так как это свежий пользователь, ему доступны все тесты
        tests = Test.objects.all()
        response = self.client.get('/')

        for t in tests:
            self.assertContains(response, t.title)


    def test_user_could_take_a_quiz(self):
        # выбираем случайный тест
        quiz = Test.objects.order_by('?')[0]
        # проверяем, можно ли его начать
        quiz_url = reverse('quiz', kwargs={'test_id': quiz.id})
        response = self.client.get(quiz_url)
        self.assertTemplateUsed(response, 'quiz.html')

        # эмулируем выполнение
        ## на реально существующие id вопросов отображаем случайные ответы
        answers = {}
        for question in quiz.question_set.all():
            answers[question.id] = random.randint(1, 10)

        ## добавляем необходимые в настоящем POST запросе данные
        answers.update({'csrfmiddlewaretoken': 'keep-it-super-secret', 'test_id': quiz.id})
        response = self.client.post(quiz_url, answers)
        ## должна появиться запись с результатом выполнения
        res = Result.objects.last()
        self.assertEqual(res.user.username, self.username)
        self.assertEqual(res.test.id, quiz.id)

        # тест пройден, значит больше недоступен на главной
        response = self.client.get('/')
        self.assertNotContains(response, quiz.title)

