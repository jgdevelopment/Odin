from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return create_account(request)

def create_account(request):
    return render(request, 'accounts/create_account.html', {})

def home(request):
    return render(request, 'accounts/home.html', {})