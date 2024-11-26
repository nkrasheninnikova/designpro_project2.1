from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def index(request):
    done_requests = Request.objects.filter(status='В')[:4]
    accepted_request_counter = Request.objects.filter(status='П').count()
    return render(request, 'index.html', {
        'done_requests': done_requests, 'accepted_request_counter': accepted_request_counter}
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.fio = form.cleaned_data['fio']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
               login(request, user)
               return HttpResponseRedirect('/')
            else:
                form = SignUpForm()
                return render(request, 'signup.html', {'form': form})