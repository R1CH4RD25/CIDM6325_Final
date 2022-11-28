from django.urls import path
from . import views


from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView, 
    SearchResultsView
)

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", ArticleCreateView.as_view(), name="article_new"),  # new
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='articles_detail'),
    path('', views.ArticleList.as_view(), name='home'),
]
