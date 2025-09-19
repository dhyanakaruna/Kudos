from django.db import models
from datetime import datetime, timedelta


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.organization.name})"

    def get_remaining_kudos(self):
        """Calculate how many kudos this user has left for the current week"""
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        # Count kudos given this week
        kudos_given_this_week = Kudo.objects.filter(
            sender=self,
            created_at__date__gte=start_of_week
        ).count()
        
        return max(0, 3 - kudos_given_this_week)

    def get_kudos_received(self):
        """Get all kudos received by this user"""
        return Kudo.objects.filter(receiver=self).select_related('sender').order_by('-created_at')


class Kudo(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kudos_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kudos_received')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Kudo from {self.sender.username} to {self.receiver.username}"

    def clean(self):
        """Validate that user cannot give kudos to themselves"""
        from django.core.exceptions import ValidationError
        if self.sender == self.receiver:
            raise ValidationError("Users cannot give kudos to themselves.")
