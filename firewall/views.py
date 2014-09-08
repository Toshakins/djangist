from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

@login_required(login_url = '/')
def welcome(req):
	return render(req, 'firewall/welcome.html', dictionary = {'name': req.user.username})

def index(req):
	if req.method == 'POST':
		name = req.POST.get('name', False)
		password = req.POST.get('password', False)
		user = authenticate(username = name, password = password)
		print name, password	
		if user is not None:
			login(req, user)
			return redirect('welcome')
		else:
			return redirect('fault')
	else:
		c = {}
		c.update(csrf(req))
		return render(req, 'firewall/index.html', c)

def fault(req):
	return render(req, 'firewall/fault.html')