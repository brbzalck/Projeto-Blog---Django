from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

PER_PAGE = 9

# sobrescrevendo list view
class PostListView(ListView):
    # definindo qual model(banco)
    model = Post
    # definindo qual template utilizar na renderização
    template_name = 'blog/pages/index.html'
    # definindo como que vou acessar os dados no template(html)
    context_object_name = 'posts'
    # colocando em ordem de criação(mais novo primeiro)
    ordering = '-pk',
    # definindo quantas páginas por vez
    paginate_by = PER_PAGE
    # query set padrão começa verificando se está publicada
    queryset = Post.objects.get_published()
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
        
    # sobrescrevendo o método de ListView que pega o contexto que vai para o template
    def get_context_data(self, **kwargs):
        # salvando o contexto numa variável para edição
        context = super().get_context_data(**kwargs)

        # atualizando determinado contexto com novos dados
        context.update({
            'page_title': 'Home - ',
        })

        # retorna contexto atualizado
        return context

# def index(request):
#     # pegando no banco com objects as publicações public True em ordem decrescente
#     posts = Post.objects.get_published()

#     # mandando para a view post 9 posts.
#     paginator = Paginator(posts, PER_PAGE)
#     # pegando o número de páginas
#     page_number = request.GET.get("page")
#     # pegando a pagina atual
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )

# view que exibe quem criou
def created_by(request, author_pk):
    # pegando o usuário do banco onde a pk da table é igual a pk do autor que vem da URL
    user = User.objects.filter(pk=author_pk).first()

    # se não existir usuário levanta um erro
    if user is None:
        raise Http404()

    # pegando no banco com objects as publicações public True E que tenham a pk de quem criou = pk que vem da URL
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    # criando um full name a partir do dado da column username
    user_full_name = user.username

    # se tiver first name, dale robertin
    if user.first_name:
        # concatenando primeiro e sobrenome na variável(editando ela)
        user_full_name = f'{user.first_name} {user.last_name}'
    # Concatenando a título da página com nome de usuário
    page_title = 'Posts de ' + user_full_name + ' - '

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
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
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

    # se não existir categoria levanta erro
    if len(page_obj) == 0:
        raise Http404()    

    # título da página é pego pelo peimeiro post página onde a categoria associada a ele tem determinado nome
    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
        }
    )
# view que mostra os post com determinadas tags
def tag(request, slug):
    # pegando no banco com objects as publicações public True E que tenha a slug da tag = slug qu vem da URL
    posts = Post.objects.get_published().filter(tags__slug=slug)

    # mandando para a view post 9 posts.
    paginator = Paginator(posts, PER_PAGE)
    # pegando o número de páginas
    page_number = request.GET.get("page")
    # pegando a pagina atual
    page_obj = paginator.get_page(page_number)

    # se não existir tags levanta erro
    if len(page_obj) == 0:
        raise Http404()   
     
    # título da página é pego pelo peimeiro post da página onde a tag associada a ele tem determinado nome
    page_title = f'{page_obj[0].tags.first().name} - Tags - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
        }
    )
# view que mostra o resultado do search
def search(request):
    # o valor de pesquisa será pego na requisição do get de name 'search', com exclusão dos espaços em branco
    search_value = request.GET.get('search', '').strip()

    # pegando no banco com objects as publicações public True E que contenha título, excerpt, e conteúdo = valor da pesquisa
    posts = (
        Post.objects.get_published()
            .filter(
                Q(title__icontains=search_value) |
                Q(excerpt__icontains=search_value) |
                Q(content__icontains=search_value)
            )[:PER_PAGE]
            # exibi somente 9
        )
    # título da página é o serach_value com o máximo de 30 caracteres
    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            # mandando o resultado da query para a render
            'page_obj': posts,
            # mandando o valor de pesquisa
            'search_value': search_value,
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
        }
    )

# view page que pega página publicada E vê qual slug do site é = slug da URL
def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    # se não existir página levanta erro
    if page_obj is None:
        raise Http404()    

    # pegando o título assiciado a página criada na admin
    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            # joga pro contexto o resultado da query
            'page': page_obj,
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
        }
    )

def post(request, slug):
    # pegando do banco se estiver publicado onde a slug é igual a slug recebida da URL
    post_obj = Post.objects.get_published().filter(slug=slug).first()
    
    # se não existir post levanta erro
    if post_obj is None:
        raise Http404()    

    # título da aba é igual ao título associado ao post no momento de sua criação
    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            # passando no contexto que vai para o renderização o nome da página
            'page_title': page_title,
        }
    )