from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = (
    ('N', 'Not specified'),
    ('M', 'Male'),
    ('F', 'Female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/%m/%Y", blank=True)
    phone_number = PhoneNumberField(region='UA', blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='N')
    verified = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
