from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment

# Classe que configura nosso próprio Attachment para armazenar dados
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        # se não tiver nome, salva com o nome do próprio arquivo
        if not self.name:
            self.name = self.file.name

        # salvando numa variável str o nome do arquivo
        current_file_name = str(self.file.name)
        # salvando de fao
        super_save = super().save(*args, **kwargs)
        # arquivo não foi mudado ainda.
        file_changed = False

        # se o arquivo existir
        if self.file:
            # file changed = se o nome do arquivo for diferente do recebido
            file_changed = current_file_name != self.file.name
        # e se o arquivo for mudado
        if file_changed:
            # deixa ele menor para não ocupar muito espaço
            resize_image(self.file, 900, True, 70)
        # agora sim salva :)
        return super_save


# Create your models here.
# Criando a table Tag que guarda as tags do site
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    # Suas colunas serão name e slug
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null= True, blank=True , max_length=255
    )

    # ao salvar, executamos nosso método slugify_new
    def save(self, *args, **kwargs):
        if not self.slug:
            # Pega name que o usuário passou, transforma em slug + 6 random letras
            self.slug = slugify_new(self.name, 6)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
# table category para as Categorias
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    # Suas colunas serão name e slug
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, null= True, blank=True , max_length=255
    )

    # ao salvar, executamos nosso método slugify_new
    def save(self, *args, **kwargs):
        if not self.slug:
            # Pega name que o usuário passou, transforma em slug + 6 random letras
            self.slug = slugify_new(self.name, 6)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
        

# table para Page
class Page(models.Model):
    # titulo da página
    title = models.CharField(max_length=65,)
    # slug para salvar no BD
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )

    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField()

    # ao salvar, executamos nosso método slugify_new
    def save(self, *args, **kwargs):
        if not self.slug:
            # Pega name que o usuário passou, transforma em slug + 6 random letras
            self.slug = slugify_new(self.title, 6)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    # Resumod do post
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para o post ser exibido publicamente.'
        ),
    )
    # aqui fica o html
    content = models.TextField()
    # capa do post!!!
    cover = models.ImageField(upload_to='posts', blank=True, default='')

    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Se marcado, exibirá a capa dentro do post.',
    )
    # (adiciona data de criação)
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_created_by.all -> assm que irei acessar esse valor no html
    created_by = models.ForeignKey(
        # pegando o usuárioo que criou
        User,
        # se deletar deixa os post
        on_delete=models.SET_NULL,
        blank=True, null=True,
        # nome relacionado para acesso no html
        related_name='post_created_by'
    )
    # atualiza data de criação
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_updated_by.all -> assm que irei acessar esse valor no html
    updated_by = models.ForeignKey(
        # selecionando qual model se trata
        User,
        # não dependente
        on_delete=models.SET_NULL,
        blank=True, null=True,
        # nome para acesso fora do models
        related_name='post_updated_by'
    )
    # O Post tem relação com a Categoria(pk>Category -> post), mas não depende dela para viver
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    # relação de tags pode ter muitos post e vice versa
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save