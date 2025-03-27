from django.urls import path
from .views import BookListView, BookDetailView, ReviewUpdateView, ReviewDeleteView

app_name = "books"

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]