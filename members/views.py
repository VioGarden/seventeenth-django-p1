from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']  #in login.html, form, name="username"
        password = request.POST['password']  #in login.html, form, name="password"
        user = authenticate(request, username=username, password=password) #if variables are correct
        if user is not None:
            login(request, user)
            return redirect('home') #return a success page
        else:
            messages.success(request, ("Error Logging In, Try Again"))
            return redirect('login-user') #return invalid login 
    else:
        return render(request, 'authentication/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)  #if user fills out form, pass
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authentication/register_user.html', {
        "form": form
    })


