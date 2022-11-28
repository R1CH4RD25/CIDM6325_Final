from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView  
from django.views.generic.detail import SingleObjectMixin  
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse  

from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL

from .forms import CommentForm
from .models import Article
from django.views import generic
from django.db.models import Q


  
class ArticleList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
  
class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'articles_detail.html'
    
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
  
class ArticleListView(LoginRequiredMixin, ListView):  
    model = Article
    template_name = "article_list.html"     


class CommentGet(DetailView):  
    model = Article
    template_name = "articles_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):  
    model = Article
    form_class = CommentForm
    template_name = "articles_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("articles_detail", kwargs={"slug": article.slug})


class ArticleDetailView(LoginRequiredMixin, View):  
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  
    model = Article
    fields = (
        "title",
        "category",
        "image",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):  
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):  
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):  
    model = Article
    template_name = "article_new.html"    
    fields = ("title","category", "image", "body")      
    prepopulated_fields = {"slug": ("title",)}

    def form_valid(self, form):  
        form.instance.author = self.request.user
        return super().form_valid(form)



class SearchResultsView(ListView):
    model = Article
    template_name = 'search_results.html'
    
    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list