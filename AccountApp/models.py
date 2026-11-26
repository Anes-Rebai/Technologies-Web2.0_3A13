from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass
number_validator = RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits')
def birth_date_validator(d):
    if d >= timezone.localdate():
        raise ValidationError('Birth date must be in the past.')

class Doctor(User):
    license_number = models.CharField(max_length=5, unique=True, validators=[MinLengthValidator(5),MaxLengthValidator(5)])
    phone = models.CharField(max_length=8, validators=[number_validator])
    specialities = models.ForeignKey("AccountApp.Specialty", related_name="doctors", on_delete=models.PROTECT)


class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[number_validator])
    phone = models.CharField(max_length=8, validators=[number_validator])
    birth_date = models.DateField(birth_date_validator)

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
