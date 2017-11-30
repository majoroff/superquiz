from django.contrib import admin

from .models import Test, Question, Answer, Result


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline,]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]


class ResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'user', 'right', 'wrong')
    list_filter = ('user',)


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
