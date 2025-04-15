from django.http import HttpResponse
from django.shortcuts import render
import requests

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def lessons(request):
    return render(request, 'lessons.html')

