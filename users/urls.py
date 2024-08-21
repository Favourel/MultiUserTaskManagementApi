from django.urls import path
from . import views as user_view

urlpatterns = [
    path('register/', user_view.RegisterView.as_view(), name='register'),
    path('login/', user_view.LoginView.as_view(), name='login'),
]
