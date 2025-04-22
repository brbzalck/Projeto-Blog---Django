from django.db import models
import os
from django.conf import settings

# Create your models here.
from django.db import models
 
 
class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    # criando colunas que recebe dados para serem guardadas no banco de dados
    # texto
    text = models.CharField(max_length=50)
    # url
    url_or_path = models.CharField(max_length=2048)
    # abriu em nova aba
    new_tab = models.BooleanField(default=False)

    # Adicionando a model MenuLink como ForeignKey de SiteSetup
    # ela pertence a site setup (um site tem vários links)
    site_setup = models.ForeignKey(
        # Selecionando qual Model se trata, modo cascata para deleção, podendo ser vazio, nulo e default
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None,
    )

    # definindo o retorno do método como str legível
    def __str__(self):
        return self.text

# criando model SiteSetup
class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    # Definindo coluna título e descrição
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    # Exibindo campos de header, search, menu, description, pagination e footer
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/',
        blank=True, default=''
    )
 
    def save(self, *args, **kwargs):
        # Se está atualizando e tem um favicon existente
        if self.pk and self.favicon:
            old_instance = SiteSetup.objects.get(pk=self.pk)
            if old_instance.favicon and old_instance.favicon != self.favicon:
                # Remove o arquivo antigo
                old_instance.favicon.delete(save=False)
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove o arquivo quando o objeto é deletado
        if self.favicon:
            self.favicon.delete(save=False)
        super().delete(*args, **kwargs)

    # definindo o retorno do método como str legível
    def __str__(self):
        return self.title