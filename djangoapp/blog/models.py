from django.db import models
from utils.rands import slugify_new

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