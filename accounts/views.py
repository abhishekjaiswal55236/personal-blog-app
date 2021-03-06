from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
from .forms import SignUpForm

def signup(request):
    if request=='GET':
        form = UserCreationForm()
    else:


        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    return render(request,'signup.html',{'form':form})

