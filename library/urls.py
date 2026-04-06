from django.urls import path
from .views import book_create, book_delete, book_edit, book_list

urlpatterns = [
    path('', book_list, name='book_list'),
    path('books/create/', book_create, name='book_create'),
    path('books/<int:pk>/edit/', book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', book_delete, name='book_delete'),
]
