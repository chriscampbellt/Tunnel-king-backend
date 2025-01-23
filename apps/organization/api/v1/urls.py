from django.urls import path

from .views import (AddTeamMemberAPIView, CreateOrganizationAPIView,
                    DepartmentListAPIView, RoleListAPIView)

app_name = "accounts"

urlpatterns = [
    path("create/", CreateOrganizationAPIView.as_view(), name="create_organization"),
    path("add/team-member/", AddTeamMemberAPIView.as_view(), name="add_team_member"),
    path("departments/", DepartmentListAPIView.as_view(), name="department_list"),
    path("roles/", RoleListAPIView.as_view(), name="role_list"),
]
