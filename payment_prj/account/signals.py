from django.db.models.signals import post_save
from userauths.models import User
from account.models import Account


def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


def save_account(sender, instance, **kwargs):
    instance.account.save()


post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)