from minify import views
from django.urls import path

urlpatterns = [
    path('', views.MinifyView.as_view, name='minify'),
]
