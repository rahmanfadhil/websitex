from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a new app with a custom template"

    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)

    def handle(self, *args, **options):
        # Get app name
        name = options["name"]

        # Create app directory
        app_dir = settings.BASE_DIR / "apps" / name
        app_dir.mkdir(exist_ok=True)

        # Create app from template
        template_dir = Path(__file__).parent / "templates"
        call_command(
            "startapp",
            name,
            template=str(template_dir),
            directory=str(app_dir),
        )

        # Show success message
        self.stdout.write(self.style.SUCCESS(f"Successfully created app {name}"))
