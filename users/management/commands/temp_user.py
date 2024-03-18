from django.core.management import BaseCommand
from django.contrib.auth.models import Permission

from users.models import User
from fcm_django.models import FCMDevice


class Command(BaseCommand):

    def handle(self, *args, **options):
        perms = Permission.objects.all()
        for perm in perms:
            print(perm.codename)
