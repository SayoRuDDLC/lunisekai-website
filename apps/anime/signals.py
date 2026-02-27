from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Still

# Сигналы не срабатывают для bulk операций (filter() и update())
@receiver(post_delete, sender=Still, dispatch_uid="delete_still_delete")
def delete_still_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=Still, dispatch_uid="delete_old_still_file")
def delete_old_still_file(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_image = Still.objects.get(pk=instance.pk).image
    except Still.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        old_image.delete(save=False)

