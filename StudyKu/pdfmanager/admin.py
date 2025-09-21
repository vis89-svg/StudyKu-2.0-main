from django.contrib import admin
from .models import PDFDocument

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')  # Customize what fields to display in the list view
    search_fields = ('name',)        # Enable search by name

# Optionally, you can add filters or other customizations if needed.
