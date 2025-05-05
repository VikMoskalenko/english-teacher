from django.contrib.auth.models import User
from django.db import models

class LessonCategory(models.Model):
    name = models.CharField(max_length=100)

class Lesson(models.Model):
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField(null=True, blank=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_surname = models.CharField(max_length=255, null=True )  # Cardholder's name
    card_number = models.CharField(max_length=16, null=True, blank=True)  # Store card number (in real case, don’t store it for security)
    exp_date = models.CharField(max_length=5, null=True)  # Expiration date (MM/YY)
    ccv = models.CharField(max_length=3, null=True)  # CCV code
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    lessons = models.ManyToManyField('Lesson')