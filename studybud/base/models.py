from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    """Model to represent a friendship between two users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')

    class Meta:
        unique_together = ('user', 'friend')  # Prevents duplicate friendships

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

class Group(models.Model):
    """Model to represent a group of users who share expenses."""
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='user_groups')  # Changed related_name to avoid conflict

    def __str__(self):
        return self.name

    def add_member(self, user):
        """Adds a user to the group."""
        self.members.add(user)

class Expense(models.Model):
    """Model to represent an expense within a group."""
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    participants = models.ManyToManyField(User, related_name='expenses_participated')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def split_amount(self):
        """Calculates the amount each participant owes."""
        if self.participants.count() > 0:
            return self.amount / self.participants.count()
        return 0
