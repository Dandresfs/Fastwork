#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def emailLogin(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/ofertas/')
        else:
            # Return a 'disabled account' error message
            return None
    else:
        # Return an 'invalid login' error message.
        return render(request, 'home.html',{"error":"El usuario y la contraseña no coinciden"})