# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserLoginView, UserRegisterView 



# Create your views here.


def login_view (request):
    next = request.GET.get('next')
    title = "Submit"
    form = UserLoginView(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')
    context ={
        "title":title,
        "form":form,
    }
    return render(request,"form.html",context)

def register_view (request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterView(request.POST or None)
   
    if form.is_valid():
        instance = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        instance.set_password(password)
        instance.save()
        user = authenticate(username=username,password=password)
        login(request,user)
        # if you are in login due to a next function then after login it will continue your action
        if next:
            return redirect(next)
        return redirect('/')
    context ={
        "title":title,
        "form":form,
    }
    return render(request,"form.html",context)

def logout_view (request):
    logout(request)
    return redirect('/')

