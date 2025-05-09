from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

PER_PAGE = 9

# sobrescrevendo list view
class PostListView(ListView):
    # definindo qual template utilizar na renderização
    template_name = 'blog/pages/index.html'
    # definindo como que vou acessar os dados no template(html)
    context_object_name = 'posts'
    # definindo quantas páginas por vez
    paginate_by = PER_PAGE
    # query set padrão começa verificando se está publicada(também define o model)
    queryset = Post.objects.get_published()
        
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


# aproveitando minha Classe List View para configurar o CreatedBy View
class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        # garantindo que a construção básica de ListView seja feita
        super().__init__(**kwargs)
        # criando dicionário temporário para armazenar dados relacionados ao USER
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        # jogando o contexto atual para uma variável
        ctx = super().get_context_data(**kwargs)

        # pegando meu USER armazenado no _temp_context
        user = self._temp_context['user']
        # configura o nome do usuário com os dados do usuário armazenado no _temp_context
        user_full_name = user.username

        # se tiver first name, dale robertin
        if user.first_name:
            # concatenando primeiro e sobrenome na variável(editando ela)
            user_full_name = f'{user.first_name} {user.last_name}'
        # Concatenando a título da página com nome de usuário
        page_title = 'Posts de ' + user_full_name + ' - '

        # aproveitando e jogando o títilo da página para dentro do contexto
        ctx.update({
            'page_title': page_title,
        })

        # enfim retorna o contexto
        return ctx
    
    # definindo queryset da view (já herdada com as configs da classe pai)
    def get_queryset(self):
        # salvando numa variável para edição
        qs = super().get_queryset()
        # filtrando os posts que forem a pk de created_by do banco = pk do user armazenado no _temp_context
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        # retorna query set
        return qs

    # sobrescrevendo get de ListView
    def get(self, request, *args, **kwargs):
        # pegando com get o ID de author_pk passado pela url
        author_pk = self.kwargs.get('author_pk')
        # pegando da table User a pk = que bate com a author_pk vinda da URL
        user = User.objects.filter(pk=author_pk).first()

        # se não existir usuário levanta um erro
        if user is None:
            # se não existir o User redireciona para o index
            return redirect('blog:index')
        
        # atualizando o contexo temporário o author_pk e user
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        # processando requisição com ID e Usuário configurados para renderização
        return super().get(request, *args, **kwargs)


# herda a lógica de listagem do PostListView, paginação, template, queryset base
class CategoryListView(PostListView):
    # "permitir_vazio", quando false não deixe a página carregar se não tiver conteúdo mandando para 404
    allow_empty = False

    # adicionando um filtro para a query de PostListView, onde a slug da categoria do banco = slug recuperada pelos kwargs q ListView armazena
    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    # mudando o contexto da categoria
    def get_context_data(self, **kwargs):
        # recuperando contexto para edição
        ctx = super().get_context_data(**kwargs)

        # salvando o títilo da aba pelo primeiro post contido em object_list que armazena o nome da categoria
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        # atualizando o título da aba
        ctx.update({
            'page_title': page_title,
        })
        # retorna contexto atualizado
        return ctx


class TagListView(PostListView):
    # "permitir_vazio", quando false não deixe a página carregar se não tiver conteúdo mandando para 404
    allow_empty = False

    # adicionando um filtro para a query de PostListView, onde a slug da tag no banco = slug recuperada pelos kwargs q ListView armazena
    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    # jogando o contexto da tag para ctx
    def get_context_data(self, **kwargs):
        # recuperando contexto para edição
        ctx = super().get_context_data(**kwargs)

        # salvando o títilo da aba pelo primeiro post contido em object_list que armazena a tag associada, pegando o nome da primeira
        page_title = f'{self.object_list[0].tags.first().name} - Tag - '
        # atualizando o título da aba
        ctx.update({
            'page_title': page_title,
        })
        # retorna contexto atualizado
        return ctx


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # iniciando search_value vazio para guardar o valor que o usuário digitar
        self._search_value = ''

    # método inicial que inicia bem no início da requisição
    def setup(self, request, *args, **kwargs):
        # pegando o valor do parâmetro search que vem na url e atribuindo para self._search_value
        self._search_value = request.GET.get('search', '').strip()

        return super().setup(request, *args, **kwargs)

    # modificando a query
    def get_queryset(self):
        # colocando meu search_value numa variável para manipulação
        search_value = self._search_value
        # o filtro será a pesquisa do search_value nos títulos, excerpt e content feito pelo icontains
        return super().get_queryset().filter(
                Q(title__icontains=search_value) |
                Q(excerpt__icontains=search_value) |
                Q(content__icontains=search_value)
            )[:PER_PAGE]
    
    # modificando o contexto da serach
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            # o título da página vai ser search value com máximo de 30 caracteres
            'page_title': f'{search_value[:30]} - Search - ',
            # valor de pesquisa para manipulação no header
            'search_value': search_value,
        })
        return ctx
    
    # get para utilizar request no final da requisição
    def get(self, request, *args, **kwargs):
        # se não houver valor de pesquisa, redireciona para home do site
        if self._search_value == '':
            return redirect('blog:index')

        return super().get(request, *args, **kwargs)


# detail view para exibir uma única página nesse caso
class PageDetailView(DetailView):
    # selecionando qual banco(table) a minha View vai trabalhar
    model = Page
    # selecionando qual template vai renderizar
    template_name = 'blog/pages/page.html'
    # selecionando a column da slug para o django procurar a página
    slug_field = 'slug'
    # em vez de acessar o 'objeto' por object acessa por 'page'
    context_object_name = 'page'

    # modificando contexto de PageDetail
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # separando qual página será exibida numa variável
        page = self.get_object()
        # pegando pela página o titulo dela para colocar como titulo de aba da mesma
        page_title = f'{page.title} - Página - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
    def get_queryset(self):
        # nossa query padrão verifica se está publicado apenas como filtro.
        return super().get_queryset().filter(is_published=True)


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