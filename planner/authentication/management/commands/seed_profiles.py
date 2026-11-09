import secrets

from django.core.management.base import BaseCommand
from django.db import transaction

from authentication.models import Profile, RoleChoices, TechChoices


PROFILES = (
    ("Avery", "Bennett", RoleChoices.PROJECT_COORDINATOR, None),
    ("Jordan", "Ellis", RoleChoices.PROJECT_COORDINATOR, None),
    ("Morgan", "Chen", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Riley", "Patel", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Casey", "Brooks", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Taylor", "Nguyen", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Cameron", "Reyes", RoleChoices.DEVELOPER, TechChoices.TESTER),
    ("Quinn", "Foster", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Drew", "Kim", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Skyler", "Turner", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Rowan", "Shah", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Emerson", "Price", RoleChoices.DEVELOPER, TechChoices.TESTER),
    ("Parker", "Diaz", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Reese", "Morgan", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Finley", "Ross", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Hayden", "Cruz", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Dakota", "Ward", RoleChoices.DEVELOPER, TechChoices.TESTER),
)


class Command(BaseCommand):
    help = "Create two project coordinators and fifteen developers for demo use."

    def handle(self, *args, **options):
        created_profiles = []
        skipped_profiles = []

        with transaction.atomic():
            for index, (first_name, last_name, role, tech) in enumerate(PROFILES, start=1):
                username = (
                    f"{first_name}.{last_name}{1000 + index}@mailinator.com".lower()
                )
                if Profile.objects.filter(username=username).exists():
                    skipped_profiles.append(username)
                    continue

                password = secrets.token_urlsafe(18)
                profile = Profile.objects.create_user(
                    username=username,
                    email=username,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    tech=tech,
                    password=password,
                )
                created_profiles.append((profile, password))

        if created_profiles:
            self.stdout.write("Created profiles (save these generated passwords now):")
            for profile, password in created_profiles:
                self.stdout.write(
                    f"{profile.role}: {profile.get_full_name()} | "
                    f"username/email: {profile.username} | password: {password}"
                )
        else:
            self.stdout.write("No profiles were created.")

        if skipped_profiles:
            self.stdout.write(
                f"Skipped {len(skipped_profiles)} existing profile(s); "
                "their passwords were not changed or displayed."
            )
