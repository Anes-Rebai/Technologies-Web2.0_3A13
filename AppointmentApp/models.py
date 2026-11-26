from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# Create your models here.
class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    doctor = models.ForeignKey("AccountApp.Doctor", related_name="appointments", on_delete=models.CASCADE)
    patient = models.ForeignKey("AccountApp.Patient", related_name="appointments", on_delete=models.CASCADE)


    reason = models.TextField(max_length=200)
    prescription = models.FileField(upload_to='prescriptions/', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])


    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField(blank=False)

    def clean(self):
        super().clean()
        if self.appointment_date and self.appointment_date <= timezone.now():
            date_unchanged = not self._state.adding and Appointment.objects.filter(
                pk=self.pk, appointment_date=self.appointment_date
            ).exists()
            if not date_unchanged:
                raise ValidationError({'appointment_date': 'Appointment date must be in the future.'})

    class Meta:
        ordering = ['-appointment_date']
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'appointment_date'], name='unique_doctor_appointment')
        ]
