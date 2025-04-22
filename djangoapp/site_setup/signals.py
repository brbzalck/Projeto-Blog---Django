from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import SiteSetup

@receiver(pre_delete, sender=SiteSetup)
def delete_favicon_on_model_delete(sender, instance, **kwargs):
    if instance.favicon:
        instance.favicon.delete(save=False)