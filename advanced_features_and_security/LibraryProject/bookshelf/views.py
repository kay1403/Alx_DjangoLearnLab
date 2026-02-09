from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from .forms import ExampleForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def form_example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Exemple de traitement sécurisé des données
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            # Ici tu pourrais enregistrer dans la base de données
            return render(request, 'bookshelf/form_example.html', {'form': form, 'success': True})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("Create book")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return HttpResponse("Edit book")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return HttpResponse("Delete book")
