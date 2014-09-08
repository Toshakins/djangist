from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required(login_url = '/')
def welcome(req):
	return render(req, 'firewall/welcome.html')

def index(req):
	if req.method == 'POST':
		name = req.POST.get('name', False)
		password = req.POST.get('password', False)
		user = authenticate(username = name, password = password)
		print 'nameu des!', req.POST
		if user is not None:
			login(req, user)
			return render(req, 'firewall/welcome.html')
		else:
			raise PermissionDenied()
	else:
		c = {}
		c.update(csrf(req))
		return render_to_response('firewall/index.html', c)