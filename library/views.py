from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, BorrowRequest
from django.db.models import Q




def home(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')


def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_librarian = request.POST.get('is_librarian') == 'on'

        # Validation
        if not username or not email or not password:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=400)

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_librarian  # Mark librarian role
        user.save()

        # Auto-login after registration
        login(request, user)
        return redirect('/')

    return render(request, 'register.html')


@login_required
def books(request):
    """
    List all books and borrowing options.
    """
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


@login_required
def borrow(request):
    """
    Handle book borrowing.
    """
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Validate inputs
        if not book_id or not start_date or not end_date:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            # Validate book availability and overlapping requests
            book = Book.objects.get(id=book_id)
            overlapping_requests = BorrowRequest.objects.filter(
                Q(book=book) & (
                    (Q(start_date__lte=end_date) & Q(end_date__gte=start_date))
                )
            )

            if overlapping_requests.exists():
                return JsonResponse({'error': 'Book not available during the requested period.'}, status=400)

            # Create borrow request
            BorrowRequest.objects.create(
                user=request.user,
                book=book,
                start_date=start_date,
                end_date=end_date
            )
            return redirect('/api/books/')

        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request.'}, status=400)
