# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

# Create your views here.

def home(request):
    return render(request, 'lr_templates/index.html')

def register(request):
    results = User.objects.register_validation(request.POST)

    if results[0]:

        request.session['user_id'] = results[1].id
        print "***********Registered**************"
        print User.objects.all()
        return redirect("/second_app/success")
    else:
        for err in results[1]:
            messages.error(request,err)
        return redirect('/lr_app')

def login(request):
    results = User.objects.login_validation(request.POST)

    if results[0]:
        request.session['user_id'] = results[1].id
        print "************Logged****************"
        print User.objects.all()
        return redirect("/second_app/success")
    else:
        for err in results[1]:
            messages.error(request, err)
        return redirect('/lr_app')


def logout(request):
    request.session.flush()
    print "*************Logged OUT****************"
    return redirect('/lr_app')