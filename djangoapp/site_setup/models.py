from django.db import models

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

    # definindo o retorno do método como str legível
    def __str__(self):
        return self.text