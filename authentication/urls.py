from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexPage),
    path("uservalidation", views.userValidation),
    path("login", views.loginPage),
    path("logout", views.logoutUser),
    path("testing", views.testing)
]