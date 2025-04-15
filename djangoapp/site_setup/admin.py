from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup

# Register your models here.
# decorator para registrar o model MenuLink na admin
@admin.register(MenuLink)
# usando MenuLinkAdmin para customizar a exibição do model na listagem
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = 'id', 'text', 'url_or_path',
    list_display_links = 'id', 'text', 'url_or_path',
    search_fields = 'id', 'text', 'url_or_path',

# decorator para registrar o model SiteSetup na admin
@admin.register(SiteSetup)
# usando SiteSetupAdmin para customizar a exibição do model na listagem
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()