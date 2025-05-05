from django.urls import path
from blog.views import index, post, page, created_by, category

# colocando nome no app para puxar as view mais fácil
app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    # caminho da url se o usuário clicar em algum post, + slug recebida pelo href post.slug, requisita view post
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('created_by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),
]