from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm
import datetime


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {'form': form, 'book_instance': book_instance}
    return render(request, 'book_renew_librarian.html', context)


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


def index(request):
    """View function for the home page of the site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})


def my_view(request, fish):
    return render(request, 'my_template.html', {'fish': fish})


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'author_list.html'
    paginate_by = 1


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """List books on loan to the current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """List all books borrowed, visible to librarians only."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'bookinstance_list_borrowed_all.html'
    paginate_by = 10
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').select_related('borrower').order_by('due_back')
