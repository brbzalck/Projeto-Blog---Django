from django.urls import path
from blog.views import index, post, page, created_by, category, tag

# colocando nome no app para puxar as view mais fácil
app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    # caminho da url se o usuário clicar em algum post, + slug recebida pelo href post.slug, requisita view post
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    # url created_by/id do criador/ , que puxa a view created_by de nome created_by
    path('created_by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),
    # url da tag/slug, que puxa a view tag de nome tag
    path('tag/<slug:slug>/', tag, name='tag'),
]