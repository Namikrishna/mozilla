from django.urls import path
from . import views
from .views import (
    AuthorListView, AuthorDetailView, AllLoanedBooksListView,
    BookListView, LoanedBooksByUserListView
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BookListView.as_view(), name='books-list'),
    path('book/<int:pk>/', views.book_detail_view, name='book-detail'),
    path('my-url/<str:fish>/', views.my_view, name='aurl'),
    path('authors/', AuthorListView.as_view(), name='authors-list'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allborrowed/', permission_required('catalog.can_mark_returned')(AllLoanedBooksListView.as_view()), name='all-borrowed'),
    path('book/<int:pk>/renew/', permission_required('catalog.can_mark_returned')(views.renew_book_librarian), name='renew-book-librarian'),
]
