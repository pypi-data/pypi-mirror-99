import os

from piccolo.conf.apps import AppConfig

from .tables import Manager, Band, Venue, Concert, Ticket, Poster


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="example_app",
    table_classes=[Manager, Band, Venue, Concert, Ticket, Poster],
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY, "piccolo_migrations"
    ),
    commands=[],
)
