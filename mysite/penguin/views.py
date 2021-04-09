from django.shortcuts import render
<<<<<<< HEAD
from django.http import HttpResponse
from .models import Player

=======
from django.http import HttpResponse, HttpRequest
from .login import UserRegisterForm
>>>>>>> Sign-up
# Create your views here.

def index(request):
    return render(request, 'penguin/index.html')
    
def login(request):
    return render(request, 'penguin/login.html')

def home(request):
    return render(request, 'penguin/home.html')

<<<<<<< HEAD
def game(request):
    players = Player.objects.all() 
    return render(request, 'penguin/World.html', {'players':players})


=======
def login(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Sucess')
    else:
        form = UserRegisterForm
        
    return render(request, 'penguin/login.html')
>>>>>>> Sign-up
