# importando o model SiteSetup para importação para todos templates
from site_setup.models import SiteSetup

def context_processor_example(request):
    return {
        'example': 'Veio do context processor (example)'
    }

# função que pega a última configuração do site e retorna num dict para manipulação
def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup,
    }