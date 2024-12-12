from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuserCommand
from django.core.management import CommandError
from django.utils.translation import gettext_lazy as _
from home.models import Landlord, Student
import uuid

class Command(CreateSuperuserCommand):
    help = "Creates a superuser and automatically generates a Landlord profile."

    def handle(self, *args, **options):
        super().handle(*args, **options)
        
        email = options.get('email')
        if not email:
            raise CommandError(_("Superuser creation failed: Missing email."))

        try:
            user = Landlord.objects.get(email=email)
            if Landlord.objects.filter(user=user).exists():
                self.stdout.write(
                    self.style.WARNING(f"Landlord profile already exists for {user.email}.")
                )
                return
            landlord = Landlord.objects.create(
                user=user,
                id=uuid.uuid4(),
                accommodation_name="",
                address="",
                company_email=email,
                description="",
                price=0.00,
                offered_amenities="",
                accommodated_universities="Default University",
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Landlord profile created for {user.email} with UUID {landlord.id}"
                )
            )
        except Student.DoesNotExist:
            raise CommandError(f"Failed to create Landlord profile: No Student found with email '{email}'.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")
