from django.db import models
from django.contrib.auth.models import User

class PDFDocument(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"

    class Meta:
        ordering = ['-searched_at']

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pdf_document')
        ordering = ['-bookmarked_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.pdf_document.name}"