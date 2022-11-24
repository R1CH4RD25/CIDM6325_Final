from django.urls import path

from .views import HomePageView
from django.urls import path, include


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
        path('', include('articles.urls')),
]
