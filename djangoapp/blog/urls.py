from django.urls import path
from blog.views import PostListView, post, page, CreatedByListView, CategoryListView, TagListView, SearchListView

# colocando nome no app para puxar as view mais fácil
app_name = 'blog'

urlpatterns = [
    # usando o PostListView com a função as_view executada para o path entender
    path('', PostListView.as_view(), name='index'),
    # caminho da url se o usuário clicar em algum post, + slug recebida pelo href post.slug, requisita view post
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    # url created_by/id do criador/ , que puxa a view created_by de nome created_by
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    # url da tag/slug, que puxa a view tag de nome tag
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]