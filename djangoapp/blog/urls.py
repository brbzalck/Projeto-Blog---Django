from django.urls import path
from blog.views import index

# colocando nome no app para puxar as view mais fácil
app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
]