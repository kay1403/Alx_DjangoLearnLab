from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.generic import DetailView
from .models import Book
from .models import Library
from .models import UserProfile


# --- FUNCTION-BASED VIEW ---
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# --- CLASS-BASED VIEW ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- CUSTOM PERMISSIONS ---
@permission_required('relationship_app.can_add_book')
def add_book(request):
    pass

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    pass

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    pass

# --- ROLE-BASED VIEWS ---
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
