from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.organization.api.v1.serializers import (AddTeamMemberSerializer,
                                                  DepartmentSerializer,
                                                  OrganizationSerializer,
                                                  RoleSerializer)
from apps.organization.models import Department, Organization, Role, TeamMember

User = get_user_model()


@extend_schema(tags=["Organization"])
class AddTeamMemberAPIView(CreateAPIView):
    serializer_class = AddTeamMemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = serializer.validated_data["organization"]
        user = serializer.validated_data["user"]
        user_created = serializer.validated_data["user_created"]
        role = serializer.validated_data.get("role")
        department = serializer.validated_data.get("department")

        # Add or update the team member
        TeamMember.objects.update_or_create(
            organization=organization,
            user=user,
            defaults={"role": role, "department": department},
        )

        # Send an invitation email if the user was newly created
        if user_created:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = request.get_host()
            # TODO: Update the url (frontend endpoint)
            reset_url = f"http://{current_site}/password-reset-confirm/{uid}/{token}/"

            send_mail(
                subject="You're Invited to Join the Organization",
                message=(
                    f"Hello,\n\nYou have been invited to join {organization.name}.\n\n"
                    f"Set your password and activate your account using the link below:\n\n"
                    f"{reset_url}\n\n"
                    f"If you did not request this, please ignore this email."
                ),
                from_email="no-reply@example.com",
                recipient_list=[user.email],
            )

        return Response(
            {"detail": "User added to organization and invitation sent."},
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Organization"])
class RoleListAPIView(generics.ListAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


@extend_schema(tags=["Organization"])
class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


@extend_schema(tags=["Organization"])
class CreateOrganizationAPIView(CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
