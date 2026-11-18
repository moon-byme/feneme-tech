from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class DeliveryStatusMigrationTests(TransactionTestCase):
    """Exercita a migração em banco de teste com entrega anterior à US-11."""

    migrate_from = [("deliveries", "0002_route_alternative")]
    migrate_to = [("deliveries", "0003_alter_delivery_status_deliverystatushistory")]

    def test_existing_delivery_is_preserved_without_invented_history(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(self.migrate_to))
        old_apps = executor.loader.project_state(self.migrate_from).apps
        user = old_apps.get_model("auth", "User").objects.create(username="gestor_migracao")
        old_delivery = old_apps.get_model("deliveries", "Delivery")
        delivery = old_delivery.objects.create(
            origin="Origem existente", destination="Destino existente",
            cargo_description="Carga existente", created_by_id=user.pk,
        )
        snapshot = old_delivery.objects.values().get(pk=delivery.pk)
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        new_apps = executor.loader.project_state(self.migrate_to).apps
        self.assertEqual(new_apps.get_model("deliveries", "Delivery").objects.values().get(pk=delivery.pk), snapshot)
        self.assertFalse(new_apps.get_model("deliveries", "DeliveryStatusHistory").objects.exists())
