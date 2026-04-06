from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book


def book_list(request):
    books = Book.objects.all()

    title = request.GET.get('title', '').strip()
    author = request.GET.get('author', '').strip()
    year = request.GET.get('year', '').strip()

    if title:
        books = books.filter(title__icontains=title)

    if author:
        books = books.filter(author__icontains=author)

    if year:
        books = books.filter(year=year)

    context = {
        'books': books,
        'title_query': title,
        'author_query': author,
        'year_query': year,
    }
    return render(request, 'library/book_list.html', context)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {
        'form': form,
        'page_title': 'Добавить книгу',
    })


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {
        'form': form,
        'page_title': 'Редактировать книгу',
    })


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()

    return redirect('book_list')

# Create your views here.
