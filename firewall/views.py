from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.views.generic.base import TemplateView
from django.views.generic import View
from django import forms
import random
from tasks import square_random, rand_sleep
from celery import app


class Welcome(View):
    def get(self, req):
        return render(req, 'firewall/welcome.html', dictionary = {'name': req.user.username})
        
class Index(View):
    def post(self, req):
        name = req.POST.get('name', False)
        password = req.POST.get('password', False)
        user = authenticate(username = name, password = password)
        if user is not None:
            login(req, user)
            return redirect('welcome')
        else:
            return redirect('fault')

    def get(self, req):
        c = {}
        c.update(csrf(req))
        form = LoginForm()
        return render(req, 'firewall/index.html', dictionary = {'c' : c, 'form': form})

class Fault(TemplateView):
    template_name = 'firewall/fault.html'

class CeleryView(View):

    task_list = []

    def get(self, req):
        task = rand_sleep.delay()
        self.task_list.append(task)
        return render(req, 'firewall/celery.html', dictionary = {'total_tasks': len(self.task_list)})

class QueueInspector(View):

    def get(self, req):
        # print app.app_or_default().events.state.tasks_by_worker()
        stats = CeleryView.task_list
        stats = [{'task_id': t.task_id} for t in stats]
        # just send all tasks which were ever been runned
        return render(req, 'firewall/inspector.html', dictionary = {'stats': stats})


class LoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)