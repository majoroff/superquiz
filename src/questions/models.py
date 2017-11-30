# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings



class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название теста')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quiz', kwargs={'test_id': self.pk})


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    order = models.PositiveIntegerField(verbose_name='Порядок')
    test = models.ForeignKey(Test)

    class Meta:
        ordering = ['order', ]

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    right = models.BooleanField(verbose_name='Правильный ответ')
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь')
    test = models.ForeignKey(Test, verbose_name='Тест')
    right = models.PositiveIntegerField(verbose_name='Верные ответы')
    wrong = models.PositiveIntegerField(verbose_name='Неверные ответы')

    class Meta:
        verbose_name = 'Результаты теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return self.user.username + ' :: ' + self.test.title
