from django.urls import path
from blog.views import index, post, page

# colocando nome no app para puxar as view mais fácil
app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    # caminho da url se o usuário clicar em algum post, + slug recebida pelo href post.slug, requisita view post
    path('post/<slug:slug>', post, name='post'),
    path('page/', page, name='page'),
]