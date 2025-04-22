from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup
from django import forms

# Register your models here.
# decorator para registrar o model MenuLink na admin
# @admin.register(MenuLink)
# # usando MenuLinkAdmin para customizar a exibição do model na listagem
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path',
#     list_display_links = 'id', 'text', 'url_or_path',
#     search_fields = 'id', 'text', 'url_or_path',

# pegando o MenuLink como table imbutida(tabular embutido)
class MenuLinkInline(admin.TabularInline):
    # selecionando qual table vai ser embutida
    model = MenuLink
    # definindo quantos campos extras do model MenuLink vai ter para adição
    extra = 1

class SiteSetupForm(forms.ModelForm):
    class Meta:
        model = SiteSetup
        fields = '__all__'
        widgets = {
            'favicon': forms.ClearableFileInput(attrs={'multiple': False}),
        }

# decorator para registrar o model SiteSetup na admin
@admin.register(SiteSetup)
# usando SiteSetupAdmin para customizar a exibição do model na listagem
class SiteSetupAdmin(admin.ModelAdmin):
    form = SiteSetupForm  # Usa o form customizado
    list_display = 'title', 'description',
    # adicionando como table imbutida MenuLinkInline ao SiteSetup para modificações simuntâneas SiteSetup/MenuLink
    inlines = MenuLinkInline,

    class Media:
        css = {'all': ['admin/css/hide_cleared_file.css']}
        js = ('admin/js/fix_favicon_clear.js',)

    # Adiciona isso para permitir a remoção do favicon
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['favicon'].widget.can_delete_related = True
        return form

    # função de permissão de adicionar setup
    def has_add_permission(self, request):
        # retorna a permissão para não adicionar se algum objeto já existir
        return not SiteSetup.objects.exists()