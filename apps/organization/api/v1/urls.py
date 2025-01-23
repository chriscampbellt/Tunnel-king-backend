from django.urls import path

from .views import (AddTeamMemberAPIView, CreateOrganizationAPIView,
                    DepartmentListAPIView, DocumentCreateAPIView,
                    DocumentUpdateDeleteAPIView, ListOrganizationAPIView,
                    RoleListAPIView)

app_name = "user_accounts"

urlpatterns = [
    path("create/", CreateOrganizationAPIView.as_view(), name="create_organization"),
    path("add/team-member/", AddTeamMemberAPIView.as_view(), name="add_team_member"),
    path("departments/", DepartmentListAPIView.as_view(), name="department_list"),
    path("roles/", RoleListAPIView.as_view(), name="role_list"),
    path(
        "",
        ListOrganizationAPIView.as_view(),
        name="list_organization",
    ),
    path(
        "<int:organization_id>/documents/",
        DocumentCreateAPIView.as_view(),
        name="upload_document",
    ),
    path(
        "documents/<int:pk>/",
        DocumentUpdateDeleteAPIView.as_view(),
        name="document_update_delete",
    ),
]
