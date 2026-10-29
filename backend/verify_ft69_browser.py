"""Conferência automatizada no Chrome, com servidor e PostgreSQL de teste isolados.

Uso: python backend/verify_ft69_browser.py evidencias/FT69/<execucao>
Requer Node.js 22+ e Chrome instalado (ou variável CHROME_PATH).
"""

import os
from pathlib import Path
import subprocess
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.runner import DiscoverRunner

from accounts.models import UserProfile
from deliveries.models import Delivery

ROOT = Path(__file__).resolve().parent.parent


class BrowserChecks(StaticLiveServerTestCase):
    def test_sprint1_browser_flow(self):
        password = "SenhaSomenteTesteFT69!"
        for username, role in [("gestor_ft69", UserProfile.Role.GESTOR),
                               ("motorista_ft69", UserProfile.Role.MOTORISTA)]:
            user = User.objects.create_user(username=username, password=password)
            user.profile.role = role
            user.profile.save(update_fields=["role"])
        completed = subprocess.run(
            ["node", str(ROOT / "scripts" / "ft69_browser.mjs"),
             self.live_server_url, os.environ["FT69_BROWSER_OUTPUT"]],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        output = completed.stdout + completed.stderr
        print(output)
        (Path(os.environ["FT69_BROWSER_OUTPUT"]) / "FT69_browser_resultado.txt").write_text(
            output, encoding="utf-8"
        )
        self.assertEqual(completed.returncode, 0, output)
        delivery = Delivery.objects.get()
        self.assertEqual(delivery.assigned_driver.username, "motorista_ft69")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Informe a pasta de evidências de uma execução FT-69.")
    output = (ROOT / sys.argv[1]).resolve()
    if not output.is_relative_to(ROOT / "evidencias" / "FT69") or not output.is_dir():
        raise SystemExit("A pasta deve existir dentro de evidencias/FT69.")
    os.environ["FT69_BROWSER_OUTPUT"] = str(output)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    runner = DiscoverRunner(verbosity=2, interactive=False)
    sys.exit(bool(runner.run_tests(["verify_ft69_browser.BrowserChecks"])))
