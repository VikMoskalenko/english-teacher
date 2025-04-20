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
