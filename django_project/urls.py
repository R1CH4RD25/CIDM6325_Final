from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import ArticleSitemap

sitemaps = {
    "posts": ArticleSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("articles/", include("articles.urls")),
    path("", include("articles.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
