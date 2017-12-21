from __future__ import unicode_literals
from .models import User, Compliment
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum

def index(request):
	context={
		'users': User.objects.all()
	}
	return render(request, "login_reg/index.html", context)

def registration(request):
	result = User.objects.validate_registration(request.POST)	
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Registration Successful!")
	return redirect('/success')

def login(request):
	result = User.objects.validate_login(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Login Successful!")
	return redirect('/success')

def success(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	context = {
		'current_user': User.objects.get(id=request.session['user_id']),
		'compliments': Compliment.objects.all()
	}
	return render(request, 'login_reg/success.html', context)

def listofcomps(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	context = {
		'current_user': User.objects.get(id=request.session['user_id']),
		'compliments': Compliment.objects.all()
	}
	return render(request, 'login_reg/listofcomps.html', context)

def compliment(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	print 'hello'
	user1 = User.objects.get(id=request.session['user_id'])
	Compliment.objects.create_compliment(request.POST)	

	return redirect('/success')

def favorite(request, comp_id):
	user1 = User.objects.get(id=request.session['user_id']).id
	compliment = Compliment.objects.get(id = comp_id)
	compliment.favorite.add(user1)

	return redirect('/success')

def logout(request, user_id):
	del request.session
	return redirect('/')
