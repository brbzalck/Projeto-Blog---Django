from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

PER_PAGE = 9

# views, urls, post, models

def index(request):
    # pegando no banco com objects as publicações public True em ordem decrescente
    posts = Post.objects.get_published()

    # mandando para a view post 9 posts.
    paginator = Paginator(posts, PER_PAGE)
    # pegando o número de páginas
    page_number = request.GET.get("page")
    # pegando a pagina atual
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

# view que exibe quem criou
def created_by(request, author_pk):
    # pegando no banco com objects as publicações public True E que tenham a pk de quem criou = pk que vem da URL
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    # mandando para a view post 9 posts.
    paginator = Paginator(posts, PER_PAGE)
    # pegando o número de páginas
    page_number = request.GET.get("page")
    # pegando a pagina atual
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

# view que mostra os post com determinadas categorias
def category(request, slug):
    # pegando no banco com objects as publicações public True E que tenha a slug da categoria = slug qu vem da URL
    posts = Post.objects.get_published().filter(category__slug=slug)

    # mandando para a view post 9 posts.
    paginator = Paginator(posts, PER_PAGE)
    # pegando o número de páginas
    page_number = request.GET.get("page")
    # pegando a pagina atual
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )

def post(request, slug):
    # pegando do banco se estiver publicado onde a slug é igual a slug recebida da URL
    post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )