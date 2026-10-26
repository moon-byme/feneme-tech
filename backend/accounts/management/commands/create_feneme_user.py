from getpass import getpass
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from accounts.models import UserProfile

class Command(BaseCommand):
    help = "Cria uma conta Feneme com perfil Gestor ou Motorista."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--role", required=True, choices=["GESTOR", "MOTORISTA"])

    def handle(self, *args, **options):
        username = options["username"]
        role = options["role"]
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            raise CommandError(f"O usuário '{username}' já existe.")

        password = getpass("Senha: ")
        confirm = getpass("Confirme a senha: ")
        if not password or password != confirm:
            raise CommandError("As senhas estão vazias ou não conferem.")

        user = User.objects.create_user(username=username, password=password)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save(update_fields=["role"])
        self.stdout.write(self.style.SUCCESS(
            f"Conta '{username}' criada com perfil {role}."
        ))
