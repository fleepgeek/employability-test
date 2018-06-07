import os
import pickle
import numpy as np
import pandas as pd

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TestQuestion, TestChoice, PersonalityType, PersonalityQuestion
from personality.utils import clear_test_session


classifer_base = os.path.join(settings.BASE_DIR, 'personality', 'classifiers')

class AptitudeTest(LoginRequiredMixin, View):
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
        for uc in user_choices:
            if(uc.id in correct_ids):
                score += 10
        # print(score)
        return redirect('aptitude_finished')
        

class PersonalityTest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        qs = PersonalityType.objects.all()
        type_o = PersonalityType.objects.get(id=1)
        type_c = PersonalityType.objects.get(id=2)
        type_e = PersonalityType.objects.get(id=3)
        type_a = PersonalityType.objects.get(id=4)
        type_n = PersonalityType.objects.get(id=5)

        context = {
            'type_o': type_o,
            'type_c': type_c,
            'type_e': type_e,
            'type_a': type_a,
            'type_n': type_n,
        }
        return render(request, 'personality/personality_test.html', context)

    def post(self, request, *args, **kwargs):
        request_count = len(request.POST)-2
        # print(request.POST, request_count)
        choices = [int(request.POST.get('choice'+str(q+1))) for q in range(request_count)]
        print(choices)
        average = sum(choices)/len(choices) if len(choices) > 0 else 0
        
        print(average)
        test_type = request.POST.get('test_type')
        
        if test_type == '1':
            print('Openness Test')
            request.session['avg_o'] = sum(choices)/len(choices)
            pickle_in = open(os.path.join(classifer_base, 'openness.pkl'), 'rb')
            clf_opn = pickle.load(pickle_in)
            answers = pd.DataFrame([choices])
            result = clf_opn.predict(answers)
            print('Openness', result)
            request.session['done_o'] = True
        elif test_type == '2':
            print('Consientious Test')
            request.session['avg_c'] = sum(choices)/len(choices)
            pickle_in = open(os.path.join(classifer_base, 'conscientious.pkl'), 'rb')
            clf_con = pickle.load(pickle_in)
            answers = pd.DataFrame([choices])
            result = clf_con.predict(answers)
            print('Conscientious', result)
            request.session['done_c'] = True
        elif test_type == '3':
            print('Extroversion Test')
            request.session['avg_e'] = sum(choices)/len(choices)
            pickle_in = open(os.path.join(classifer_base, 'extroversion.pkl'), 'rb')
            clf_ext = pickle.load(pickle_in)
            answers = pd.DataFrame([choices])
            result = clf_ext.predict(answers)
            print('Extroversion', result)
            request.session['done_e'] = True
        elif test_type == '4':
            print('Agreeable Test')
            request.session['avg_a'] = sum(choices)/len(choices)
            pickle_in = open(os.path.join(classifer_base, 'agreeable.pkl'), 'rb')
            clf_agb = pickle.load(pickle_in)
            answers = pd.DataFrame([choices])
            result = clf_agb.predict(answers)
            print('Agreeable', result)
            request.session['done_a'] = True
        elif test_type == '5':
            print('Neurotism Test') 
            request.session['avg_n'] = sum(choices)/len(choices)
            pickle_in = open(os.path.join(classifer_base, 'neurotism.pkl'), 'rb')
            clf_neu = pickle.load(pickle_in)
            answers = pd.DataFrame([choices])
            result = clf_neu.predict(answers)
            print('Neurotism', result)
            request.session['done_n'] = True
            
            return redirect('personality_completed')
        
        return redirect('personality_test')


class PersonalityCompleted(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pickle_in = open(os.path.join(classifer_base, 'employability.pkl'), 'rb')
        clf_emp = pickle.load(pickle_in)
        avg_o = request.session.get('avg_o', None) 
        avg_c = request.session.get('avg_c', None) 
        avg_e = request.session.get('avg_e', None) 
        avg_a = request.session.get('avg_a', None) 
        avg_n = request.session.get('avg_n', None)
        averages = [avg_o, avg_c, avg_e, avg_a, avg_n]
        # averages = [3.1, 3.1, 3.2, 3.2, 1.9]
        print(averages)
        if len(averages) != 5 or None in averages:
            completed = False
        else: 
            personality_avgs = pd.DataFrame([averages])
            result = clf_emp.predict(personality_avgs)
            print('Employable', result)
            possible_results = [1,0]
            completed = clear_test_session(request) if result in possible_results else False
        context = {
            'completed': completed
        }
        return render(request, 'personality/personality_completed.html', context)



