from django.contrib import admin
from blog.models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

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
class PageAdmin(SummernoteModelAdmin):
    # colocando os campos de summernote no content atribuido pelo models
    summernote_fields = ('content',)
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

# Registrando na admin do django o Post
@admin.register(Post)
# Definindo como o campo será exibido
class PostAdmin(SummernoteModelAdmin):
    # colocando os campos de summernote no content atribuido pelo models
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',  'created_by',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'category', 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by', 'link',
    prepopulated_fields = {
        "slug": ('title',),
    }
    autocomplete_fields = 'tags', 'category',

    # link recebe objeto
    def link(self, obj):
        # se não existir pk exibi -
        if not obj.pk:
            return '-'
        # se no link existir pk vai ser igual ao método get_absolute_url da nossa models
        url_do_post = obj.get_absolute_url()
        # usando método do django utils para o django confiar no link
        safe_link = mark_safe(f'<a href="{url_do_post}">Ver post</a>')

        # método retorna um link safe
        return safe_link

    # o metodo save_model tem acesso ao obj
    def save_model(self, request, obj, form, change):
        # change = mudar
        # se foi feita alterções, vai para o campo updated_by de obj
        if change:
            obj.updated_by = request.user
        # ao salvar se não tiver mudança é porque criou
        else:
            obj.created_by = request.user
        obj.save()