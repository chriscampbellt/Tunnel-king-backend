from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Case, CharField, F, Q, Value, When
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_extensions.db.models import ActivatorModel
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.organization.api.v1.serializers import (AddTeamMemberSerializer,
                                                  DepartmentSerializer,
                                                  DocumentSerializer,
                                                  OrganizationSerializer,
                                                  RoleSerializer)
from apps.organization.models import (Department, Document, Organization, Role,
                                      TeamMember)

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
            {
                "detail": f"User {user_created} added to organization and invitation sent."
            },
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


@extend_schema(tags=["Organization"])
class ListOrganizationAPIView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return organizations where the user is the owner or a team member,
        and annotate the user's role as 'Owner' or the role name (if a team member).
        """
        user = self.request.user

        return (
            Organization.objects.filter(Q(owner=user) | Q(team_members__user=user))
            .annotate(
                # Annotate the role: 'Owner' if the user owns the organization, else role from TeamMember
                user_role=Case(
                    When(owner=user, then=Value("Owner")),
                    When(team_members__user=user, then=F("team_members__role__name")),
                    default=Value("Unknown"),
                    output_field=CharField(),
                )
            )
            .distinct()
        )


@extend_schema(tags=["Document"])
class DocumentCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_organization(self):
        organization_id = self.kwargs["organization_id"]
        return Organization.objects.get(id=organization_id)

    def get_queryset(self):
        """
        Restrict documents to the ones owned by the user's organization.
        """
        organization_id = self.kwargs.get("organization_id")
        return Document.objects.filter(
            organization__owner=self.request.user, organization_id=organization_id
        )

    def perform_create(self, serializer):
        organization = self.get_organization()
        serializer.save(organization=organization)


@extend_schema(tags=["Document"])
class DocumentListCreateAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        """
        Restrict documents to the ones owned by the user's organization.
        """
        organization_id = self.kwargs.get("organization_id")
        return Document.objects.filter(
            organization__owner=self.request.user, organization_id=organization_id
        )


@extend_schema(tags=["Document"])
class DocumentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_queryset(self):
        """
        Restrict access to the documents of the user's organization.
        """
        return super().get_queryset().filter(organization__owner=self.request.user)

    def perform_destroy(self, instance):
        instance.status = ActivatorModel.ACTIVE_STATUS
        instance.save()
