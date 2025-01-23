from django.core.management import BaseCommand

from apps.organization.constants import DEPARTMENTS, ROLES
from apps.organization.models import Department, Role


class Command(BaseCommand):
    help = "Create templates with their questions"

    def handle(self, *args, **kwargs):

        departments_to_create = [
            name
            for name in DEPARTMENTS
            if not Department.objects.filter(name=name).exists()
        ]
        departments_to_create = [
            Department(name=name) for name in departments_to_create
        ]
        Department.objects.bulk_create(departments_to_create)

        roles_to_create = [
            name for name in ROLES if not Role.objects.filter(name=name).exists()
        ]
        roles_to_create = [Role(name=role_name) for role_name in roles_to_create]
        Role.objects.bulk_create(roles_to_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully created departments, roles, permission")
        )
