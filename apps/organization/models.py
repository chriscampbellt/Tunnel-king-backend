from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_extensions.db.models import ActivatorModel, TimeStampedModel

User = get_user_model()


class Department(ActivatorModel, TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Role(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=50, unique=True)
    # permissions = models.ManyToManyField("auth.Permission", related_name="roles")

    def __str__(self):
        return self.name


class Organization(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(
        help_text="This is the email of the organization's admin.",
        null=True,
        blank=True,
    )
    # add key to user owner of this organization
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
        null=True,
        blank=True,
    )

    permissions = models.ManyToManyField(
        "auth.Permission", related_name="organizations", blank=True
    )
    email_sent = models.BooleanField(
        default=False
    )  # Track if the email was successfully sent

    def __str__(self):
        return f"{self.id} | {self.name} | {self.email}"

    def save(self, *args, **kwargs):
        # is_new = self._state.adding
        super().save(*args, **kwargs)

        # TODO: Handle for both (existing and not existing users)
        # if is_new:
        # Create the admin user
        # self.create_admin_user()

    def create_admin_user(self):
        """
        Creates an admin user for the organization and triggers a password reset email.
        """
        from .tasks import send_reset_email_task

        admin_user = User.objects.create_user(
            username=self.email,  # Use email as username
            email=self.email,
        )
        admin_user.set_unusable_password()
        admin_user.save()

        # Generate reset link and send email via Celery task
        reset_link = self.generate_reset_link(admin_user)
        send_reset_email_task.delay(self.id, self.name, self.email, reset_link)

    def generate_reset_link(self, user):
        """
        Generates a password reset link for the given user.
        """
        current_site = Site.objects.get_current()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse(
            "accounts:set_admin_password", kwargs={"uidb64": uid, "token": token}
        )
        return f"http://{current_site.domain}{reset_url}"

    def resend_admin_email(self):
        """
        Resends the admin password reset email with a new link.
        """
        from .tasks import send_reset_email_task

        admin_user = User.objects.get(email=self.email)
        reset_link = self.generate_reset_link(admin_user)
        send_reset_email_task.delay(self.id, self.name, self.email, reset_link)


class TeamMember(models.Model):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="team_members"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizations"
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members",
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members",
    )

    def __str__(self):
        return f"{self.user.email} in {self.organization.name}"


class Document(TimeStampedModel, ActivatorModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="organization_documents/")
    name = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_documents",
    )

    def __str__(self):
        return f"{self.name} for {self.organization.name}"
