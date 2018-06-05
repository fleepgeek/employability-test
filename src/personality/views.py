from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .models import TestQuestion, TestChoice


class AptitudeTest(View):
    def get(self, request, *args, **kwargs):
        qs = TestQuestion.objects.all()[:10]
        context = {
            'questions': qs
        }
        return render(request, 'personality/aptitude_test.html', context)
    
    def post(self, request, *args, **kwargs):
        choices = [request.POST.get(str(q+1)) for q in range(10)]
        score = 0
        user_choices = TestChoice.objects.filter(pk__in=choices)
        correct_answers = TestChoice.objects.filter(is_answer=True)
        correct_ids = [x.id for x in correct_answers]
        for cid in correct_ids:
            for uc in user_choices:
                if(uc.id == cid):
                    score += 10
        return redirect('aptitude_finished')
        