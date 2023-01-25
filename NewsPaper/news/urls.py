from django.urls import path
from .views import PostList, PostDetail, NewCreate, ArticleCreate, NewUpdate,\
   ArticleUpdate, NewDelete, ArticleDelete, \
   multiply, PostSearch, CategoryListView, subscribe
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path('news/', PostList.as_view(), name='post_list'),
   # path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewCreate.as_view(), name='new_create'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   # path('search/', PostSearch.as_view(), name='news_search'),
   path('multiply/', multiply),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('<int:pk>/', cache_page(300)(PostDetail.as_view()), name='post_detail'),
   path('news/', cache_page(60)(PostList.as_view()), name='post_list'),
   path('search/', cache_page(60)(PostSearch.as_view()), name='news_search'),
]


