from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import PDFDocument, SearchHistory, Bookmark
from .forms import PDFUploadForm

# Upload view - now handles private/public uploads
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            if request.user.is_authenticated:
                pdf.author = request.user
            form.save()
            messages.success(request, 'PDF uploaded successfully!')
            return redirect('upload_pdf')
    else:
        form = PDFUploadForm()
    return render(request, 'pdfmanager/upload_pdf.html', {'form': form})

# Updated search_pdfs view with PDF IDs for bookmarking
def search_pdfs(request):
    query = request.GET.get('q', '')
    results = []
    suggestions = []
    pdf_urls = {}
    pdf_ids = {}
    
    if query:
        results = PDFDocument.objects.filter(name__icontains=query)
        suggestions = PDFDocument.objects.filter(name__icontains=query).values_list('name', flat=True)
        
        # Save search history if user is authenticated (only for non-AJAX requests)
        if request.user.is_authenticated and not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            SearchHistory.objects.create(
                user=request.user,
                query=query
            )
        
        # Create mappings for suggestions
        for pdf in results:
            pdf_urls[pdf.name] = pdf.file.url
            pdf_ids[pdf.name] = pdf.id  # Add PDF IDs for bookmarking
            
        # If it's an AJAX request, return suggestions
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'suggestions': list(suggestions), 
                'pdfUrls': pdf_urls,
                'pdfIds': pdf_ids  # Include PDF IDs
            })
    
    # Get user's bookmarks to show bookmark status
    user_bookmarks = []
    if request.user.is_authenticated:
        user_bookmarks = list(Bookmark.objects.filter(user=request.user).values_list('pdf_document_id', flat=True))
            
    return render(request, 'pdfmanager/search_pdfs.html', {
        'results': results, 
        'query': query,
        'user_bookmarks': user_bookmarks
    })

# Add this new view to track PDF views/clicks
@login_required
def view_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    
    # Save to search history as "viewed"
    SearchHistory.objects.create(
        user=request.user,
        query=f"Viewed: {pdf.name}"
    )
    
    # Redirect to the actual PDF file
    return redirect(pdf.file.url)

# My Notes dashboard - shows user's uploaded PDFs
@login_required
def my_notes(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search in user's own notes (both private and public)
        my_pdfs = PDFDocument.objects.filter(
            author=request.user,
            name__icontains=query
        )
    else:
        my_pdfs = PDFDocument.objects.filter(author=request.user)
    
    return render(request, 'pdfmanager/my_notes.html', {
        'my_pdfs': my_pdfs,
        'query': query
    })

# Edit PDF
@login_required
def edit_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id, author=request.user)
    
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            messages.success(request, 'PDF updated successfully!')
            return redirect('my_notes')
    else:
        form = PDFUploadForm(instance=pdf)
    
    return render(request, 'pdfmanager/edit_pdf.html', {
        'form': form, 
        'pdf': pdf
    })

# Delete PDF
@login_required
def delete_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id, author=request.user)
    
    if request.method == 'POST':
        pdf.file.delete()  # Delete the actual file
        pdf.delete()
        messages.success(request, 'PDF deleted successfully!')
        return redirect('my_notes')
    
    return render(request, 'pdfmanager/delete_pdf.html', {'pdf': pdf})

# Search History view
@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-searched_at')[:20]  # Last 20 searches
    return render(request, 'pdfmanager/search_history.html', {'history': history})

# Bookmarks view
@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-bookmarked_at')
    return render(request, 'pdfmanager/bookmarks.html', {'bookmarks': bookmarks})

# Updated add bookmark with AJAX support
@login_required
def add_bookmark(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, pdf_document=pdf)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request - return JSON
        if created:
            return JsonResponse({'status': 'added', 'message': f'Added "{pdf.name}" to bookmarks!'})
        else:
            return JsonResponse({'status': 'exists', 'message': f'"{pdf.name}" is already bookmarked!'})
    
    # Regular request - redirect with message
    if created:
        messages.success(request, f'Added "{pdf.name}" to bookmarks!')
    else:
        messages.info(request, f'"{pdf.name}" is already bookmarked!')
    
    return redirect('search_pdfs')

# Updated remove bookmark with AJAX support
@login_required
def remove_bookmark(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    try:
        bookmark = Bookmark.objects.get(user=request.user, pdf_document=pdf)
        bookmark.delete()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAX request - return JSON
            return JsonResponse({'status': 'removed', 'message': f'Removed "{pdf.name}" from bookmarks!'})
        
        # Regular request - redirect with message
        messages.success(request, f'Removed "{pdf.name}" from bookmarks!')
    except Bookmark.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Bookmark not found!'})
        
        messages.error(request, 'Bookmark not found!')
    
    return redirect('bookmarks')

# Custom logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('search_pdfs')