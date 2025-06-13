from django.db import models
from datetime import datetime,timedelta
from user.models import User
from book.models import Book

# Create your models here.
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = datetime.now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"{self.book.title}-{self.user.username}"

    
    @property
    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return datetime.now().date() > self.due_date

class add_to_cart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Keep both foreign keys temporarily
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.user.username} requests {self.book.title}"
