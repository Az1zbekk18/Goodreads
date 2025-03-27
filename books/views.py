from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Book, BookReview
from .forms import ReviewForm

class BookListView(ListView):
    model = Book
    template_name = "books/list.html"
    context_object_name = "books"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(title__icontains=query)
        return super().get_queryset()

class BookDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = BookReview.objects.filter(book=self.object)
        context["form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        existing_review = BookReview.objects.filter(book=book, user=request.user).first()

        if existing_review:
            messages.error(request, "Siz allaqachon ushbu kitob uchun review qoldirgansiz!")
            return redirect('books:detail', book.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Sizning review qo'shildi!")
            return redirect('books:detail', book.id)

        context = self.get_context_data(**kwargs)
        context["form"] = form
        return self.render_to_response(context)


class ReviewUpdateView(UpdateView):
    model = BookReview
    fields = ['comment', 'stars_given']
    template_name = 'reviews/review_form.html'

    def get_success_url(self):
        return reverse_lazy('books:detail', kwargs={'pk': self.object.book.pk})

class ReviewDeleteView(DeleteView):
    model = BookReview
    template_name = 'reviews/review_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('books:detail', kwargs={'pk': self.object.book.id})


def home(request):
    book_reviews = BookReview.objects.select_related("book", "user").all()
    context = {"book_reviews": book_reviews}
    return render(request, "home.html", context)
