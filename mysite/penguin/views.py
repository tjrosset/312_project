from django.shortcuts import render
from django.http import HttpResponse
from .models import Player

# Create your views here.

def index(request):
    return render(request, 'penguin/index.html')
    
def login(request):
    return render(request, 'penguin/login.html')

def home(request):
    return render(request, 'penguin/home.html')

def game(request):
    players = Player.objects.all() 
    return render(request, 'penguin/World.html', {'players':players})


