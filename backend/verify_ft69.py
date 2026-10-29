"""Execute os testes existentes e registre evidências por CT da Sprint 1."""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from zoneinfo import ZoneInfo

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
from django.db import connection
from django.test.runner import DiscoverRunner

ROOT = Path(__file__).resolve().parent.parent
LABELS = ["accounts.tests", "deliveries.tests", "deliveries.test_ft58"]
FLOW = "deliveries.tests.FenemeDeliveryFlowTests."
AUTH = "accounts.tests.MotoristaLoginTests."
CASES = [
    ("CT-01", "Login válido do Gestor", "HTTP 200, tokens, perfil GESTOR e consulta autenticada.",
     [FLOW + "test_login_returns_role"]),
    ("CT-02", "Senha incorreta do Gestor", "HTTP 401, mensagem genérica e ausência de tokens.",
     [AUTH + "test_invalid_credentials_are_rejected_without_tokens"]),
    ("CT-03", "Cadastrar entrega válida", "HTTP 201, dados persistidos, autor e status PENDENTE.",
     [FLOW + "test_gestor_can_create_and_list_delivery"]),
    ("CT-04", "Cadastrar sem campos obrigatórios", "HTTP 400, erros por campo ausente/em branco e nenhuma gravação.",
     [FLOW + "test_missing_required_fields_are_rejected"]),
    ("CT-05", "Atribuir Motorista", "HTTP 200, atribuição persistida e lista/detalhe acessíveis ao responsável.",
     [FLOW + "test_gestor_can_assign_existing_driver"]),
    ("CT-13", "Login válido do Motorista", "HTTP 200, tokens e perfil MOTORISTA no usuário e no JWT.",
     [AUTH + "test_motorista_valid_login_returns_tokens_and_role"]),
    ("CT-14", "Credenciais inválidas do Motorista", "HTTP 401, mensagem genérica e ausência de tokens.",
     [AUTH + "test_invalid_credentials_are_rejected_without_tokens"]),
    ("CT-15", "Consultar entregas cadastradas", "HTTP 200, dados completos e todas as entregas visíveis ao Gestor.",
     [FLOW + "test_gestor_can_create_and_list_delivery",
      "deliveries.test_ft58.DriverDeliveryListTests.test_gestor_still_sees_all_deliveries"]),
    ("CT-16", "Consultar lista vazia como Gestor", "HTTP 200 e lista [] em base sem entregas.",
     [FLOW + "test_gestor_sees_empty_delivery_list"]),
    ("CT-17", "Atribuir usuário que não é Motorista", "HTTP 400, erro em driver_id e atribuição anterior preservada.",
     [FLOW + "test_cannot_assign_user_with_manager_profile"]),
]


class EvidenceResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = {}

    def startTest(self, test):
        super().startTest(test)
        self.outcomes[test.id()] = "iniciado"

    def addSuccess(self, test):
        super().addSuccess(test)
        self.outcomes[test.id()] = "aprovado"

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.outcomes[test.id()] = "reprovado"

    def addError(self, test, err):
        super().addError(test, err)
        self.outcomes[test.id()] = "erro"

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.outcomes[test.id()] = "ignorado"

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.outcomes[test.id()] = (
                "reprovado" if issubclass(err[0], test.failureException) else "erro"
            )


class EvidenceRunner(DiscoverRunner):
    def get_resultclass(self):
        return EvidenceResult

    def run_suite(self, suite, **kwargs):
        self.test_database = connection.settings_dict["NAME"]
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            self.database_version = cursor.fetchone()[0]
        self.result = super().run_suite(suite, **kwargs)
        return self.result


class Tee:
    def __init__(self, console, file):
        self.console, self.file = console, file

    def write(self, value):
        self.console.write(value)
        self.file.write(value)

    def flush(self):
        self.console.flush()
        self.file.flush()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def metric(cases):
    executed = sum(case["resultado"] in {"aprovado", "reprovado"} for case in cases)
    return {"executados": executed, "planejados": len(cases),
            "percentual": round(executed / len(cases) * 100, 2)}


def main():
    django.setup()
    started = datetime.now(ZoneInfo("America/Sao_Paulo"))
    output = ROOT / "evidencias" / "FT69" / started.strftime("%Y%m%d-%H%M%S-%f")
    output.mkdir(parents=True, exist_ok=False)
    sources = sorted(
        path for path in (ROOT / "backend").rglob("*.py")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    )
    metadata = {
        "inicio": started.isoformat(), "timezone": "America/Sao_Paulo",
        "commit_base": git("rev-parse", "HEAD"),
        "alteracoes_locais": git("status", "--porcelain"),
        "python": platform.python_version(), "django": django.get_version(),
        "sistema": platform.platform(), "database_engine": connection.settings_dict["ENGINE"],
        "comando": "./backend/.venv/Scripts/python.exe backend/verify_ft69.py",
        "labels": LABELS,
        "sha256_fontes": {str(p.relative_to(ROOT)).replace("\\", "/"):
                          hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    }
    runner = EvidenceRunner(verbosity=2, interactive=False)
    error = None
    with (output / "FT69_resultado.txt").open("w", encoding="utf-8") as log:
        with redirect_stdout(Tee(sys.stdout, log)), redirect_stderr(Tee(sys.stderr, log)):
            print(f"FT-69 / Q-01 — início: {started.isoformat()}")
            try:
                failures = runner.run_tests(LABELS)
            except Exception as exc:
                import traceback
                traceback.print_exc()
                error = f"{type(exc).__name__}: {exc}"
                failures = 1
    result = getattr(runner, "result", None)
    outcomes = result.outcomes if result else {}
    cases = []
    for ct, title, expected, methods in CASES:
        states = [outcomes.get(method, "não executado") for method in methods]
        state = ("aprovado" if all(s == "aprovado" for s in states)
                 else "reprovado" if all(s in {"aprovado", "reprovado"} for s in states)
                 else "incompleto")
        cases.append({"ct": ct, "cenario": title, "resultado": state,
                      "verificacoes": expected,
                      "metodos": {method: outcomes.get(method, "não executado") for method in methods}})
    metadata.update({
        "fim": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
        "database_teste": getattr(runner, "test_database", None),
        "postgresql": getattr(runner, "database_version", None),
        "erro_infraestrutura": error,
        "metodos_executados": result.testsRun if result else 0,
        "suite_aprovada": bool(result and result.wasSuccessful() and not failures),
        "q01_original_r1": metric(cases[:5]),
        "controle_ampliado_r1_provisorio": metric(cases),
        "aprovados": sum(c["resultado"] == "aprovado" for c in cases),
        "reprovados": sum(c["resultado"] == "reprovado" for c in cases),
        "incompletos": sum(c["resultado"] == "incompleto" for c in cases),
        "casos": cases, "resultados_metodos": outcomes,
        "conferencia_manual_navegador": "pendente",
        "aprovacao_universo_po_qa": "pendente",
        "sha256_log": hashlib.sha256((output / "FT69_resultado.txt").read_bytes()).hexdigest(),
    })
    (output / "FT69_resultado.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    original, expanded = metadata["q01_original_r1"], metadata["controle_ampliado_r1_provisorio"]
    lines = [
        "# FT-69 — execução funcional Q-01 da Sprint 1", "",
        f"Execução: {metadata['inicio']} a {metadata['fim']} (America/Sao_Paulo).", "",
        "Referências: [FT-69](https://feneme.atlassian.net/browse/FT-69) e "
        "[Plano de Testes FT-10](https://feneme.atlassian.net/browse/FT-10). "
        "Cenários e divergência documental conforme instruções fornecidas pelo solicitante; "
        "sem aprovação formal do universo ampliado registrada nesta execução.", "",
        f"Ambiente: Python {metadata['python']}, Django {metadata['django']}; "
        f"PostgreSQL em banco temporário `{metadata['database_teste']}`.", "",
        f"Commit base: `{metadata['commit_base']}`. As alterações locais executadas "
        "estão identificadas pelos hashes SHA-256 dos fontes no JSON.", "",
        f"Métodos automatizados executados: **{metadata['metodos_executados']}**. "
        f"CT aprovados: **{metadata['aprovados']}**; reprovados: **{metadata['reprovados']}**; "
        f"incompletos/não executados: **{metadata['incompletos']}**.", "",
        f"Q-01 original R1 (CT-01 a CT-05): "
        f"**{original['executados']}/{original['planejados']} = {original['percentual']}%**.", "",
        f"Controle ampliado R1 (CT-01 a CT-05 e CT-13 a CT-17): "
        f"**{expanded['executados']}/{expanded['planejados']} = {expanded['percentual']}%**, "
        "provisório até PO e QA aprovarem o universo. Não utilizar denominador 26.", "",
        "Execução conta CT aprovados e reprovados; erros/ausência de execução ficam incompletos. "
        "Um método pode evidenciar mais de um CT. Os demais métodos são regressões de apoio.", "",
        "| Grupo | CT | Cenário | Resultado na API | Verificações |",
        "|---|---|---|---|---|",
    ]
    for case in cases:
        group = "Original R1" if case in cases[:5] else "Acrescentado R1"
        lines.append(f"| {group} | {case['ct']} | {case['cenario']} | "
                     f"{case['resultado']} | {case['verificacoes']} |")
    lines += ["", "## Rastreabilidade", "",
              "Evidências: [log integral](FT69_resultado.txt) e [dados e hashes](FT69_resultado.json).", ""]
    for case in cases:
        lines.append(f"- **{case['ct']}**: " + "; ".join(
            f"`{method}` ({state})" for method, state in case["metodos"].items()))
    lines += ["", "## Pendências para fechamento", "",
              "- Conferência manual no navegador: pendente. A suíte acima executa fluxos reais "
              "da API com persistência em PostgreSQL, sem comprovar mensagens ou layout na interface.",
              "- PO/QA: confirmar se o universo oficial da Q-01 possui 5 ou 10 CT.",
              "- Registro no Jira: relatório local preparado para anexar/comentar na FT-69 e vincular à FT-10.", ""]
    if error:
        lines += [f"Erro de infraestrutura: `{error}`.", ""]
    (output / "FT69_relatorio.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Evidências: {output}")
    print(f"CT: {metadata['aprovados']} aprovados, {metadata['reprovados']} reprovados, "
          f"{metadata['incompletos']} incompletos.")
    return 1 if failures or metadata["incompletos"] or metadata["reprovados"] else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    sys.exit(main())
