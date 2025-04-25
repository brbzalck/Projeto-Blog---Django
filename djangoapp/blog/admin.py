from django.contrib import admin
from blog.models import Tag, Category, Page

# Register your models here.
# Registrando no admin o campo Tag
@admin.register(Tag)
# Configurando como será exibido na admin do site
class TagAdmin(admin.ModelAdmin):
    # configurando como será exibido a tag
    list_display = 'id', 'name', 'slug',
    # em qual campo poderemos acessar ela
    list_display_links = 'name',
    # podemos pesquisar por tais campos
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    # colocando uma pré visualização de como a tag vai ficar
    prepopulated_fields = {
        "slug": ('name',),
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }
# Registrando Page no admin
@admin.register(Page)
# com as seguintes informações de exibição
class PageAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }