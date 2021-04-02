from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .login import UserRegisterForm
# Create your views here.

def index(request):
    return render(request, 'penguin/index.html')
    
def login(request):
    return render(request, 'penguin/login.html')

def home(request):
    return render(request, 'penguin/home.html')

def login(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Sucess')
    else:
        form = UserRegisterForm
        
    return render(request, 'penguin/login.html')