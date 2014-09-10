from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.views.generic.base import TemplateView
from django.views.generic import View
from django import forms
from celery import Celery
import random
import django.conf
from celery.registry import tasks

class Welcome(View):
	def get(self, req):
		return render(req, 'firewall/welcome.html', dictionary = {'name': req.user.username})
		
class Index(View):
	def post(self, req):
		name = req.POST.get('name', False)
		password = req.POST.get('password', False)
		user = authenticate(username = name, password = password)
		print name, password	
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

	celery = Celery('firewall.views.square_random', backend = 'redis', broker='redis://')
	celery.config_from_object('django.conf:settings')
	celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


	@celery.task
	def square_random(x):
		return x ** 2

	tasks.register(square_random)

	def get(self, req):
		task = self.square_random.delay(random.random())
		print task.state
		self.task_list.append(task)
		return render(req, 'firewall/celery.html', dictionary = {'total_tasks': len(self.task_list)})

class LoginForm(forms.Form):
	name = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

