from django.contrib import admin

# Register your models here.
from apps.organization.models import (Department, Document, Organization, Role,
                                      TeamMember)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "name",
    )
    list_filter = ("created", "modified", "activate_date", "deactivate_date")
    search_fields = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "name",
    )
    list_filter = ("created", "modified", "activate_date", "deactivate_date")
    # raw_id_fields = ('permissions',)
    search_fields = ("name",)


class TeamMemberInline(admin.TabularInline):  # or admin.StackedInline
    model = TeamMember
    extra = 0  # Do not display extra blank forms
    fields = ["user", "role", "department"]  # Fields to display in the inline
    readonly_fields = ["user"]  # Make user field read-only (optional)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "name",
        "email",
    )
    list_filter = ("created", "modified", "activate_date", "deactivate_date")
    raw_id_fields = ("permissions",)
    search_fields = ("name",)
    actions = ["resend_email"]
    inlines = [TeamMemberInline]

    @admin.action(description="Resend password reset email")
    def resend_email(self, request, queryset):
        for organization in queryset:
            organization.resend_admin_email()
        self.message_user(request, "Password reset emails resent successfully.")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "user", "role", "department")
    list_filter = ("organization", "user", "role", "department")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "status",
        "activate_date",
        "deactivate_date",
        "organization",
        "file",
        "name",
        "uploaded_at",
        "uploaded_by",
    )
    list_filter = (
        "created",
        "modified",
        "activate_date",
        "deactivate_date",
        "organization",
        "uploaded_at",
        "uploaded_by",
    )
    search_fields = ("name",)
