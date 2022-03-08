import os
from shutil import copy

from django.apps import AppConfig

from pathlib import Path

from car_inventory.settings import BASE_DIR


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'


class CarInventoryConfig(AppConfig):
    name = "inventory"

    def ready(self):
        db_source = os.path.join(BASE_DIR, 'db.sqlite3')
        destination_dir = str(Path.home()) + '\\Documents\\Backup\\'
        try:
            os.mkdir(destination_dir)
        except FileExistsError:
            try:
                os.remove(destination_dir + "db.sqlite3")
            except FileNotFoundError:
                copy(db_source, destination_dir)
            else:
                copy(db_source, destination_dir)
        else:
            copy(db_source, destination_dir)

