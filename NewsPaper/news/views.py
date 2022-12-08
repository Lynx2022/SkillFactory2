from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory
from .forms import NewForm, ArticleForm
from .filters import NewsFilter
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import login_required
from datetime import timezone, timedelta, datetime


class PostList(ListView):
    model = Post
    ordering ='-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        limit = 3
        today = datetime.now()
        prev_day = today - timedelta(days=1)
        posts_day_count = Post.objects.filter(dateCreation__gte=prev_day, author__authorUser=user).count()
        context['posts_limit'] = limit <= posts_day_count
        return context




class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_new',)
    raise_exception = True
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_variety = 'ne'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_variety = 'ar'
        return super().form_valid(form)


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_new',)
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_article',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


class NewDelete(DeleteView):
    permission_required = ('simpleapp.delete_new',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(DeleteView):
    permission_required = ('simpleapp.delete_article',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)


class PostSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей данной категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})