from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, CustomLoginView, ProfileView, ProfileUpdateView, UserLogout
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', UserLogout, name='logout'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
