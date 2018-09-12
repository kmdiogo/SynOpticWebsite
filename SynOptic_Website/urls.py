from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.AboutUs, name='about-us'),
    path('contact-us', views.ContactUs, name='contact-us')
]
