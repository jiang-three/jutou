from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

from django.db.models.signals import post_migrate

def create_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'jiang44811957')

class YourAppConfig(AppConfig):
    def ready(self):
        post_migrate.connect(create_superuser, sender=self)