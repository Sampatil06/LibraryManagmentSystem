from rest_framework import serializers
from .models import User, Book, BorrowRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_librarian']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'user', 'book', 'start_date', 'end_date', 'status']
