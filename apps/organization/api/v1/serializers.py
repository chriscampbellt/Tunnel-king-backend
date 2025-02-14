from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.organization.models import Department, Document, Organization, Role


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
        data["user"], data["user_created"] = CustomUser.objects.get_or_create(email=email)

        return data


class OrganizationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_role = serializers.CharField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "owner", "user_role"]  # Include your model fields here
        read_only_fields = ["owner"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "organization", "file", "name", "uploaded_at", "uploaded_by"]
        read_only_fields = ["id", "uploaded_at", "uploaded_by", "organization"]

    def create(self, validated_data):
        # Set the uploaded_by field to the current user
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)
