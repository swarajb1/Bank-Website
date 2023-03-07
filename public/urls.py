from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

app_name = "public"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),


    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]