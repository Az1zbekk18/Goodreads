from django.urls import path
from api.views import BookReviewsListApiView, BookReviewDetailAPIView

urlpatterns = [
    path('reviews/', BookReviewsListApiView.as_view(), name='reviews-list'),
    path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review-detail'),
]
