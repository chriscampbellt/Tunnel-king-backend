from rest_framework import serializers

from apps.accounts.models import User
from apps.organization.models import Department, Organization, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class AddTeamMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False
    )

    def validate(self, data):
        if self.context["request"].user != data["organization"].owner:
            raise serializers.ValidationError(
                {
                    "detail": "only owner of this organization can add team member to this organization."
                }
            )
        email = data.get("email")
        data["user"], data["user_created"] = User.objects.get_or_create(email=email)

        return data


class OrganizationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Organization
        fields = ["id", "name", "owner"]  # Include your model fields here
        read_only_fields = ["owner"]
