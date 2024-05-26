from minify import views
from django.urls import path

urlpatterns = [
    path('', views.MinifyView.as_view(), name='minify'),
    path('doc/', views.PdfView.as_view(), name='view_pdf'),
]
