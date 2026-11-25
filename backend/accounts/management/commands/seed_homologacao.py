"""Contas de demonstração do ambiente de homologação (FT-110).

As senhas vêm de variáveis de ambiente configuradas só no provedor; nada fica no
repositório. Sem as variáveis, o comando não cria nada e o deploy continua.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserProfile

DEMO_ACCOUNTS = (
    ("gestor_demo", UserProfile.Role.GESTOR, "HOMOLOG_GESTOR_PASSWORD"),
    ("motorista_demo", UserProfile.Role.MOTORISTA, "HOMOLOG_MOTORISTA_PASSWORD"),
)


class Command(BaseCommand):
    help = "Cria ou atualiza as contas de demonstração da homologação a partir de variáveis de ambiente."

    def handle(self, *args, **options):
        User = get_user_model()
        for username, role, variable in DEMO_ACCOUNTS:
            password = os.getenv(variable, "")
            if not password:
                self.stdout.write(self.style.WARNING(f"{variable} não definida; conta '{username}' ignorada."))
                continue
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save(update_fields=["role"])
            action = "criada" if created else "atualizada"
            self.stdout.write(self.style.SUCCESS(f"Conta '{username}' {action} com perfil {role}."))
