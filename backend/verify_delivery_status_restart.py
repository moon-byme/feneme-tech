"""Evidência reproduzível de persistência após reinício real do servidor.

Use somente um banco descartável já migrado:
python verify_delivery_status_restart.py --database feneme_status_e2e_20261118_001
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True)
    args = parser.parse_args()
    if not args.database.startswith("feneme_status_e2e_"):
        parser.error("Use um banco descartável com prefixo feneme_status_e2e_.")
    os.environ["DB_NAME"] = args.database
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    from django.db import connection
    from deliveries.models import DeliveryStatusHistory

    suffix, password = secrets.token_hex(5), secrets.token_urlsafe(24)
    users = {}
    for role in ["GESTOR", "MOTORISTA"]:
        user = get_user_model().objects.create_user(
            username=f"restart_{role.lower()}_{suffix}", password=password,
        )
        user.profile.role = role
        user.profile.save(update_fields=["role"])
        users[role] = user

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"

    def request(path, data=None, token=None):
        req = Request(base + path, data=json.dumps(data).encode() if data is not None else None,
                      headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {token}"} if token else {})})
        with urlopen(req, timeout=10) as response:
            return json.load(response)

    def stop_server(process):
        if process.poll() is None:
            if os.name == "nt":
                # O launcher do venv no Windows pode manter um processo filho.
                # Encerra somente a árvore do PID criado por este script.
                subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            else:
                process.terminate()
            process.wait(timeout=10)
        for _ in range(50):
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                    time.sleep(0.1)
            except OSError:
                return
        raise RuntimeError("A porta do servidor continua aberta após o encerramento.")

    def start_server():
        process = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload"],
            cwd=Path(__file__).resolve().parent, env=os.environ.copy(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("O servidor encerrou durante a inicialização.")
            try:
                with urlopen(base + "/", timeout=1):
                    return process
            except OSError:
                time.sleep(0.1)
        stop_server(process)
        raise RuntimeError("Timeout iniciando servidor de teste.")

    def login(role):
        return request("/api/auth/login/", {"username": users[role].username, "password": password})["access"]

    process = start_server()
    try:
        manager = login("GESTOR")
        delivery = request("/api/deliveries/", {
            "origin": "Origem reinicio FT-48", "destination": "Destino reinicio FT-48",
            "cargo_description": "Carga ficticia de verificacao",
        }, manager)
        delivery_id = delivery["id"]
        request(f"/api/deliveries/{delivery_id}/assign-driver/", {"driver_id": users["MOTORISTA"].pk}, manager)
        result = request(f"/api/deliveries/{delivery_id}/update-status/", {"status": "EM_TRANSPORTE"}, login("MOTORISTA"))
        assert result["status"] == "EM_TRANSPORTE"
        first_pid = process.pid
        stop_server(process)
        connection.close()
        process = start_server()
        assert process.pid != first_pid
        for role in ["GESTOR", "MOTORISTA"]:
            result = request(f"/api/deliveries/{delivery_id}/", token=login(role))
            assert result["status"] == "EM_TRANSPORTE"
        event = DeliveryStatusHistory.objects.get(delivery_id=delivery_id)
        assert (event.previous_status, event.new_status) == ("PENDENTE", "EM_TRANSPORTE")
        assert event.changed_by_id == users["MOTORISTA"].pk
        assert event.changed_at is not None
        print(json.dumps({
            "verification": "FT-48: reinicio real do processo Django",
            "server_restarted": True, "fresh_authentication": ["GESTOR", "MOTORISTA"],
            "port_closed_between_processes": True,
            "recovered_status": result["status"], "recovered_history_events": 1,
            "history_fields_verified": ["delivery", "previous_status", "new_status", "changed_by", "changed_at"],
            "result": "PASS",
        }, ensure_ascii=False, indent=2))
    finally:
        stop_server(process)
        connection.close()


if __name__ == "__main__":
    main()
