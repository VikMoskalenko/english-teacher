from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Booking
from .models import Lesson
import requests
from collections import Counter
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib import messages
from .models import Payment, Lesson
from django.core.mail import send_mail
from django.conf import settings

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
    lessons=Lesson.objects.all()
    return render(request, 'prices.html', {'lessons': lessons})

def pay_view(request):
    return render(request, 'pay.html')


def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')

        if len(card_number) == 16 and card_number.isdigit():
            request.session['cart'] = []  # Clear cart
            messages.success(request, 'Payment successful!')
            return redirect('lesson_list')
        else:
            messages.error(request, 'Invalid card number. Please enter a 16-digit number.')
            return redirect('cart')


def add_to_cart(request, lesson_id):
    cart = request.session.get('cart', [])
    if lesson_id not in cart:
        cart.append(lesson_id)
        request.session['cart'] = cart
    return redirect('prices')

def cart_view(request):
    cart = request.session.get('cart', [])
    cart_counter = Counter(cart)

    lessons = Lesson.objects.filter(id__in=cart)

    lesson_data = []
    for lesson in lessons:
        lesson_data.append({
            'lesson': lesson,
            'quantity': cart_counter[str(lesson.id)] if str(lesson.id) in cart_counter else cart_counter[lesson.id],
        })

    return render(request, 'cart.html', {'lesson_data': lesson_data})

def add_to_cart(request, lesson_id):
    cart = request.session.get('cart', [])
    if lesson_id not in cart:
        cart.append(lesson_id)
    request.session['cart'] = cart
    return redirect('prices')



@require_POST
def remove_from_cart(request, lesson_id):
    cart = request.session.get('cart', [])
    if lesson_id in cart:
        cart.remove(lesson_id)
    request.session['cart'] = cart
    return redirect('cart')


def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number').replace(' ', '')
        name_surname = request.POST.get('name_surname')
        exp_date = request.POST.get('exp_date')
        ccv = request.POST.get('ccv')
        cart = request.session.get('cart', [])

        if len(card_number) == 16 and card_number.isdigit() and cart:
            lessons = Lesson.objects.filter(id__in=cart)
            total = sum(lesson.price for lesson in lessons)

            payment = Payment.objects.create(
                user=request.user,
                name_surname=name_surname,
                card_number=card_number,
                exp_date=exp_date,
                ccv=ccv,
                total_amount=total,
            )
            payment.lessons.set(lessons)

            lesson_list = "\n".join(f"- {lesson.title} ({lesson.price} GBP)" for lesson in lessons)
            message = (
                f"Thank you for your payment!\n\nYou purchased the following lessons:\n\n"
                f"{lesson_list}\n\nTotal paid: {total} GBP"
            )

            send_mail(
                subject="Lesson Payment Confirmation",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            request.session['cart'] = []
            return redirect('payment_confirmation')

        messages.error(request, 'Invalid card number or empty cart.')
        return redirect('cart')