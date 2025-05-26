from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('lessons/', views.lessons, name='lessons'),
    path('book/', views.api_book, name='book'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('prices/', views.price_view, name='prices'),
    path('pay/', views.pay_view, name='pay'),
     path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:lesson_id>', views.add_to_cart, name='add_to_cart'),
path('remove-from-cart/<int:lesson_id>/', views.remove_from_cart, name='remove_from_cart'),
path('process-payment/', views.process_payment, name='process_payment'),
path('payment-confirmation/', views.payment_confirmation, name='payment_confirmation'),
    #api-pay
]