from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('minify/', include('minify.urls')),
    path('<short_code>', include('redirection.urls'))
]
