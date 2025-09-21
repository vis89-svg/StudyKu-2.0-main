from django.urls import path, include
from . import views


urlpatterns = [
    # Public routes
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('', views.search_pdfs, name='search_pdfs'),
    
    # OAuth routes (django-allauth)
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_view, name='logout'),
    
    # User-specific routes
    path('my-notes/', views.my_notes, name='my_notes'),
    path('my-notes/edit/<int:pdf_id>/', views.edit_pdf, name='edit_pdf'),
    path('my-notes/delete/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    
    # PDF viewing (tracks history)
    path('view-pdf/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
    
    # History and bookmarks
    path('search-history/', views.search_history, name='search_history'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmark/add/<int:pdf_id>/', views.add_bookmark, name='add_bookmark'),
    path('bookmark/remove/<int:pdf_id>/', views.remove_bookmark, name='remove_bookmark'),
]
