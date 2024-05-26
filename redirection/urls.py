from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectionView.as_view(), name='redirection'),
]
