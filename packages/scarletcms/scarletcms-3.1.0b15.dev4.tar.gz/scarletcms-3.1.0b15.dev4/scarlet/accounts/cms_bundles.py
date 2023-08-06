from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm

try:
    from ..cms import bundles, views
    from ..cms.sites import site
except ValueError:
    from cms import bundles, views
    from cms.sites import site

from . import forms, groups


class AddView(views.FormView):
    force_add = True
    form_class = forms.SignupModelForm

    fieldsets = (
        (
            "User Information",
            {"fields": ("username", "first_name", "last_name", "email")},
        ),
        ("Password", {"fields": ("password1", "password2")}),
    )


class PasswordView(views.FormView):
    redirect_to_view = "edit"
    context_object_name = "object"

    def get_form_class(self):
        return AdminPasswordChangeForm

    def write_message(self, message=None):
        message = f"{self.object} password changed"
        super().write_message(message=message)

    def get_form_kwargs(self):
        # Since we aren't using a model form
        # strip instance and use user instead
        kwargs = super().get_form_kwargs()
        instance = kwargs.pop("instance")
        kwargs["user"] = instance
        return kwargs


class AccountBundle(bundles.Bundle):
    required_groups = (groups.ADMIN,)

    add = AddView()
    edit = views.FormView(
        form_class=forms.UserForm,
        fieldsets=(
            (
                "User Information",
                {
                    "fields": (
                        "username",
                        "first_name",
                        "last_name",
                        "email",
                        "password",
                    )
                },
            ),
            ("Status", {"fields": ("is_active", "is_superuser", "is_staff")}),
            ("Groups", {"fields": ("groups",)}),
        ),
        context_object_name="object",
    )
    password = PasswordView()
    main = views.ListView(
        paginate_by=100,
        display_fields=("username", "first_name", "last_name", "email", "groups"),
        action_links=(
            ("edit", "Edit", "e"),
            ("delete", "Delete", "d"),
            ("password", "Change Password", "k"),
        ),
    )

    class Meta:
        model = get_user_model()
        primary_model_bundle = True
        item_views = ("password", "edit", "delete")
        default_kwargs = {"object_header_tmpl": "cms/object_header_no_preview.html"}


site.register("users", AccountBundle(name="accounts_admin", title="Account"), 10)
