from django.contrib import admin
from site_setup.models import MenuLink

# Register your models here.
# decorator para registrar o model MenuLink na admin
@admin.register(MenuLink)
# usando MenuLinkAdmin para customizar a exibição do model MenuLink com um form pronto
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = 'id', 'text', 'url_or_path',
    list_display_links = 'id', 'text', 'url_or_path',
    search_fields = 'id', 'text', 'url_or_path',