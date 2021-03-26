from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'penguin/index.html')
    
def login(request):
    return render(request, 'penguin/login.html')

def home(request):
    return render(request, 'penguin/home.html')

