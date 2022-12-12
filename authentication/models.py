from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = (
    (0, 'Not specified'),
    (1, 'Male'),
    (2, 'Female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/%m/%Y")
    phone_number = PhoneNumberField(region='UA')
    birthday = models.DateField()
    sex = models.CharField(max_length=15, choices=GENDER_CHOICES, default=0)
    verified = models.BooleanField(default=False)
