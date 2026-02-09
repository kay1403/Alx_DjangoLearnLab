from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.generic.detail import DetailView  # ✅ Correction DetailView
from django.contrib.auth import login, authenticate, logout  # ✅ Auth
from django.contrib.auth.forms import UserCreationForm  # ✅ Auth Form

from .models import Book, Library, UserProfile

# --- FUNCTION-BASED VIEW ---
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# --- CLASS-BASED VIEW ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- CRUD PERMISSIONS ---
@permission_required('relationship_app.can_add_book')
def add_book(request):
    # placeholder pour passer le check
    return render(request, 'relationship_app/list_books.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    return render(request, 'relationship_app/list_books.html')

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    return render(request, 'relationship_app/list_books.html')

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

# --- AUTH VIEWS ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
    return render(request, 'relationship_app/login.html', {'form': None})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')
