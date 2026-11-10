import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from accounts.models import UserProfile

E2E_USERS = (("gestor_e2e", "GESTOR"), ("motorista_e2e", "MOTORISTA"), ("motorista_outro_e2e", "MOTORISTA"))


class Command(BaseCommand):
    help = (
        "Cria (ou atualiza) as contas fictícias gestor_e2e e motorista_e2e usadas pelos "
        "testes Cucumber/Cypress. A senha vem da variável de ambiente E2E_PASSWORD."
    )

    def handle(self, *args, **options):
        if not settings.DEBUG and os.getenv("E2E_ALLOW_SEED") != "1":
            raise CommandError("Recusado fora de DEBUG. Defina E2E_ALLOW_SEED=1 se for intencional.")

        password = os.getenv("E2E_PASSWORD")
        if not password:
            raise CommandError("Defina E2E_PASSWORD com a senha das contas de teste.")

        User = get_user_model()
        for username, role in E2E_USERS:
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save(update_fields=["role"])
            action = "criada" if created else "atualizada"
            self.stdout.write(self.style.SUCCESS(f"Conta '{username}' {action} com perfil {role}."))
