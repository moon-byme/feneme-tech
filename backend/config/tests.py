"""FT-110: configuração de homologação (health check, DATABASE_URL e contas de demonstração)."""
import os
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from accounts.models import UserProfile
from config.settings import database_from_url


class HealthCheckTests(TestCase):
    def test_health_is_public_and_reports_database_and_commit(self):
        with override_settings(APP_COMMIT="abc1234"):
            response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok", "commit": "abc1234"})

    def test_health_reports_database_failure_without_details(self):
        with mock.patch("config.views.connection.cursor", side_effect=RuntimeError("senha=segredo")):
            response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["database"], "indisponivel")
        self.assertNotIn("segredo", response.content.decode())

    def test_health_only_accepts_get(self):
        self.assertEqual(APIClient().post("/api/health/").status_code, 405)


class DatabaseUrlTests(TestCase):
    def test_parses_provider_connection_string(self):
        config = database_from_url("postgresql://feneme_user:p%40ss@db.exemplo.test:5433/feneme_db?sslmode=require")
        self.assertEqual(config["NAME"], "feneme_db")
        self.assertEqual(config["USER"], "feneme_user")
        self.assertEqual(config["PASSWORD"], "p@ss")
        self.assertEqual(config["HOST"], "db.exemplo.test")
        self.assertEqual(config["PORT"], "5433")
        self.assertEqual(config["OPTIONS"], {"sslmode": "require"})

    def test_rejects_other_schemes(self):
        with self.assertRaises(ValueError):
            database_from_url("mysql://u:p@h/db")


class SeedHomologacaoTests(TestCase):
    def test_creates_demo_accounts_from_environment(self):
        env = {"HOMOLOG_GESTOR_PASSWORD": "Gestor-Demo-123!", "HOMOLOG_MOTORISTA_PASSWORD": "Motorista-Demo-123!"}
        with mock.patch.dict(os.environ, env):
            call_command("seed_homologacao", stdout=StringIO())
            call_command("seed_homologacao", stdout=StringIO())  # idempotente
        User = get_user_model()
        gestor = User.objects.get(username="gestor_demo")
        motorista = User.objects.get(username="motorista_demo")
        self.assertTrue(gestor.check_password("Gestor-Demo-123!"))
        self.assertEqual(gestor.profile.role, UserProfile.Role.GESTOR)
        self.assertEqual(motorista.profile.role, UserProfile.Role.MOTORISTA)
        self.assertEqual(User.objects.filter(username__endswith="_demo").count(), 2)

    def test_without_passwords_creates_nothing(self):
        with mock.patch.dict(os.environ, {"HOMOLOG_GESTOR_PASSWORD": "", "HOMOLOG_MOTORISTA_PASSWORD": ""}):
            out = StringIO()
            call_command("seed_homologacao", stdout=out)
        self.assertFalse(get_user_model().objects.filter(username__endswith="_demo").exists())
        self.assertIn("ignorada", out.getvalue())
