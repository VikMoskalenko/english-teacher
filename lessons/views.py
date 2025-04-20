from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Booking
from .models import Lesson
import requests

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

def about(request):
    if request.method == "GET":
        return render(request, 'about.html')

def contact(request):
    if request.method == "GET":
        return render(request, 'contact.html')

def lessons(request):
    if request.method == "GET":
        return render(request, 'lessons.html')

def api_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')  # optional if not using yet

        if not name or not email:
            return render(request, 'book.html', {
                'success': False,
                'message': 'Please fill in all required fields.',
                 'today': date.today()
            })

        try:
            Booking.objects.create(name=name, email=email, date=date)
            return render(request, 'book.html', {
                'success': True,
                'message': 'Your request is confirmed!',
                'today': date.today()
            })
        except Exception as e:
            return render(request, 'book.html', {
                'success': False,
                'message': 'Something went wrong. Please try again.',
                'today': date.today()
            })

    return render(request, 'book.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # or wherever you want
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def price_view(request):
    return render(request, 'prices.html')

def pay_view(request):
    return render(request, 'pay.html')

def cart_view(request):
    # Example: get cart from session or db
    cart = request.session.get('cart', [])  # List of lesson IDs
    lessons = Lesson.objects.filter(id__in=cart)  # Assuming you have a Lesson model

    return render(request, 'cart.html', {'lessons': lessons})

def add_to_cart(request, lesson_id):
    cart = request.session.get('cart', [])
    if lesson_id not in cart:
        cart.append(lesson_id)
    request.session['cart'] = cart
    return redirect('prices')
