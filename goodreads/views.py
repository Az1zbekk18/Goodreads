from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview


def landing_page(request):
    return render(request, "landing.html")


def home_page(request):
    reviews = BookReview.objects.all().order_by("-id")
    paginator = Paginator(reviews, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})

