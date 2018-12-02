from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def index(request):
    """
    Función vista para la página de inicio.
    :param request:
    :return:
    """
    # Genera Contadores de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Libros disponibles ( status = 'a' )
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # El 'all()' esta implicito por defecto
    num_genre = Genre.objects.count()
    num_book_with_p = Book.objects.all().count()
    #Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session["num_visits"]= num_visits+1
    # Renderiza la plantilla HTML index.html con los datos en la variable contexo
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genre': num_genre, "num_book_with_P": num_book_with_p, "num_visits": num_visits},
        )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
class BookDetailView(generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author
class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    Función de vista para renovar una BookInstance específica por bibliotecario.
    :param request:
    :param pk:
    :return:
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    #  Si se trata de una solicitud POST, entonces procese los datos del formulario
    if request.method == 'POST':
        #  Cree una instancia de formulario y rellénela con datos de la solicitud (enlace)
        form = RenewBookForm(request.POST)

        #  Compruebe si el formulario es válido:
        if form.is_valid():
            #  procese los datos en form.cleaned_data según sea necesario (aquí solo escribimos en el campo due_back del modelo)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            #  redirigir a una nueva URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    #  Si se trata de un GET (o cualquier otro método), cree el formulario predeterminado.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death': '05/01/2018', }

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
