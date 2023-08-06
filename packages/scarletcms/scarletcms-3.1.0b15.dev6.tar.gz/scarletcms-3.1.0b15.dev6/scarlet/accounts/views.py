from django.contrib import messages
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import logout as Signout
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView, View
from django.views.generic.list import ListView, MultipleObjectMixin

from . import settings as accounts_settings
from . import signals as accounts_signals
from .decorators import secure_required
from .forms import (
    AuthenticationForm,
    ChangeEmailForm,
    EditProfileForm,
    SignupForm
)
from .models import AccountsSignup
from .utils import get_profile_model, get_user_model, signin_redirect


class ExtraContextTemplateView(TemplateView):
    """ Add extra context to a simple template view """

    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            *args, **kwargs
        )
        if self.extra_context:
            context.update(self.extra_context)
        return context

    # this view is used in POST requests,
    # e.g. signup when the form is not valid
    post = TemplateView.get


@secure_required
def activate(
    request,
    activation_key,
    template_name="accounts/activate_fail.html",
    success_url=None,
    extra_context=None,
):
    """
    Activate a user with an activation key.

    The key is a SHA1 string. When the SHA1 is found with an
    :class:`AccountsSignup`, the :class:`User` of that account will be
    activated.  After a successful activation the view will redirect to
    ``success_url``.  If the SHA1 is not found, the user will be shown the
    ``template_name`` template displaying a fail message.

    :param activation_key:
        String of a SHA1 string of 40 characters long. A SHA1 is always 160bit
        long, with 4 bits per character this makes it --160/4-- 40 characters
        long.

    :param template_name:
        String containing the template name that is used when the
        ``activation_key`` is invalid and the activation fails. Defaults to
        ``accounts/activation_fail.html``.

    :param success_url:
        String containing the URL where the user should be redirected to after
        a successful activation. Will replace ``%(username)s`` with string
        formatting if supplied. If ``success_url`` is left empty, will direct
        to ``accounts_profile_detail`` view.

    :param extra_context:
        Dictionary containing variables which could be added to the template
        context. Default to an empty dictionary.

    """
    user = AccountsSignup.objects.activate_user(activation_key)
    if user:
        # Sign the user in.
        auth_user = authenticate(identification=user.email, check_password=False)
        login(request, auth_user)

        if accounts_settings.ACCOUNTS_USE_MESSAGES:
            messages.success(
                request,
                _("Your account has been activated and you have been signed in."),
                fail_silently=True,
            )

        if success_url:
            redirect_to = success_url % {"username": user.username}
        else:
            redirect_to = reverse(
                "accounts_profile_detail", kwargs={"username": user.username}
            )
        return redirect(redirect_to)
    else:
        if not extra_context:
            extra_context = dict()
        return ExtraContextTemplateView.as_view(
            template_name=template_name, extra_context=extra_context
        )(request)


@secure_required
def email_confirm(
    request,
    confirmation_key,
    template_name="accounts/email_confirm_fail.html",
    success_url=None,
    extra_context=None,
):
    """
    Confirms an email address with a confirmation key.

    Confirms a new email address by running :func:`User.objects.confirm_email`
    method. If the method returns an :class:`User` the user will have his new
    e-mail address set and redirected to ``success_url``. If no ``User`` is
    returned the user will be represented with a fail message from
    ``template_name``.

    :param confirmation_key:
        String with a SHA1 representing the confirmation key used to verify a
        new email address.

    :param template_name:
        String containing the template name which should be rendered when
        confirmation fails. When confirmation is successful, no template is
        needed because the user will be redirected to ``success_url``.

    :param success_url:
        String containing the URL which is redirected to after a successful
        confirmation.  Supplied argument must be able to be rendered by
        ``reverse`` function.

    :param extra_context:
        Dictionary of variables that are passed on to the template supplied by
        ``template_name``.

    """
    user = AccountsSignup.objects.confirm_email(confirmation_key)
    if user:
        if accounts_settings.ACCOUNTS_USE_MESSAGES:
            messages.success(
                request, _("Your email address has been changed."), fail_silently=True
            )

        if success_url:
            redirect_to = success_url
        else:
            redirect_to = reverse(
                "accounts_email_confirm_complete", kwargs={"username": user.username}
            )
        return redirect(redirect_to)
    else:
        if not extra_context:
            extra_context = dict()
        return ExtraContextTemplateView.as_view(
            template_name=template_name, extra_context=extra_context
        )(request)


def direct_to_user_template(request, username, template_name, extra_context=None):
    """
    Simple wrapper for Django's :func:`direct_to_template` view.

    This view is used when you want to show a template to a specific user. A
    wrapper for :func:`direct_to_template` where the template also has access
    to the user that is found with ``username``. For ex. used after signup,
    activation and confirmation of a new e-mail.

    :param username:
        String defining the username of the user that made the action.

    :param template_name:
        String defining the name of the template to use. Defaults to
        ``accounts/signup_complete.html``.

    **Keyword arguments**

    ``extra_context``
        A dictionary containing extra variables that should be passed to the
        rendered template. The ``account`` key is always the ``User``
        that completed the action.

    **Extra context**

    ``viewed_user``
        The currently :class:`User` that is viewed.

    """
    user = get_object_or_404(get_user_model(), username__iexact=username)

    if not extra_context:
        extra_context = dict()
    extra_context["viewed_user"] = user
    extra_context["profile"] = user.get_profile()
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
def signin(
    request,
    auth_form=AuthenticationForm,
    template_name="accounts/signin_form.html",
    redirect_field_name=REDIRECT_FIELD_NAME,
    redirect_signin_function=signin_redirect,
    extra_context=None,
):
    """
    Signin using email or username with password.

    Signs a user in by combining email/username with password. If the
    combination is correct and the user :func:`is_active` the
    :func:`redirect_signin_function` is called with the arguments
    ``REDIRECT_FIELD_NAME`` and an instance of the :class:`User` who is is
    trying the login. The returned value of the function will be the URL that
    is redirected to.

    A user can also select to be remembered for ``ACCOUNTS_REMEMBER_DAYS``.

    :param auth_form:
        Form to use for signing the user in. Defaults to the
        :class:`AuthenticationForm` supplied by accounts.

    :param template_name:
        String defining the name of the template to use. Defaults to
        ``accounts/signin_form.html``.

    :param redirect_field_name:
        Form field name which contains the value for a redirect to the
        succeeding page. Defaults to ``next`` and is set in
        ``REDIRECT_FIELD_NAME`` setting.

    :param redirect_signin_function:
        Function which handles the redirect. This functions gets the value of
        ``REDIRECT_FIELD_NAME`` and the :class:`User` who has logged in. It
        must return a string which specifies the URI to redirect to.

    :param extra_context:
        A dictionary containing extra variables that should be passed to the
        rendered template. The ``form`` key is always the ``auth_form``.

    **Context**

    ``form``
        Form used for authentication supplied by ``auth_form``.

    """
    form = auth_form()

    if request.method == "POST":
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification = form.cleaned_data["identification"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data["remember_me"]

            user = authenticate(identification=identification, password=password)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(
                        accounts_settings.ACCOUNTS_REMEMBER_ME_DAYS[1] * 86400
                    )
                else:
                    request.session.set_expiry(0)

                if accounts_settings.ACCOUNTS_USE_MESSAGES:
                    messages.success(
                        request, _("You have been signed in."), fail_silently=True
                    )

                # Whereto now?
                redirect_to = redirect_signin_function(
                    request.GET.get(redirect_field_name), user
                )
                return redirect(redirect_to)
            else:
                return redirect(
                    reverse("accounts_disabled", kwargs={"username": user.username})
                )

    if not extra_context:
        extra_context = dict()
    extra_context.update(
        {"form": form, "next": request.GET.get(redirect_field_name),}
    )
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
def signout(
    request,
    next_page=accounts_settings.ACCOUNTS_REDIRECT_ON_SIGNOUT,
    template_name="accounts/signout.html",
    *args,
    **kwargs
):
    """
    Signs out the user and adds a success message ``You have been signed
    out.`` If next_page is defined you will be redirected to the URI. If
    not the template in template_name is used.

    :param next_page:
        A string which specifies the URI to redirect to.

    :param template_name:
        String defining the name of the template to use. Defaults to
        ``accounts/signout.html``.

    """
    if (
        request.user.is_authenticated() and accounts_settings.ACCOUNTS_USE_MESSAGES
    ):  # pragma: no cover
        messages.success(request, _("You have been signed out."), fail_silently=True)
    return Signout(request, next_page, template_name, *args, **kwargs)


@secure_required
def email_change(
    request,
    username,
    email_form=ChangeEmailForm,
    template_name="accounts/email_form.html",
    success_url=None,
    extra_context=None,
):
    """
    Change email address

    :param username:
        String of the username which specifies the current account.

    :param email_form:
        Form that will be used to change the email address. Defaults to
        :class:`ChangeEmailForm` supplied by accounts.

    :param template_name:
        String containing the template to be used to display the email form.
        Defaults to ``accounts/email_form.html``.

    :param success_url:
        Named URL where the user will get redirected to when successfully
        changing their email address.  When not supplied will redirect to
        ``accounts_email_complete`` URL.

    :param extra_context:
        Dictionary containing extra variables that can be used to render the
        template. The ``form`` key is always the form supplied by the keyword
        argument ``form`` and the ``user`` key by the user whose email address
        is being changed.

    **Context**

    ``form``
        Form that is used to change the email address supplied by ``form``.

    ``account``
        Instance of the ``Account`` whose email address is about to be changed.

    **Todo**

    Need to have per-object permissions, which enables users with the correct
    permissions to alter the email address of others.

    """
    user = get_object_or_404(get_user_model(), username__iexact=username)

    form = email_form(user)

    if request.method == "POST":
        form = email_form(user, request.POST, request.FILES)

        if form.is_valid():
            form.save()

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse(
                    "accounts_email_change_complete", kwargs={"username": user.username}
                )
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["profile"] = user.get_profile()
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
def password_change(
    request,
    username,
    template_name="accounts/password_form.html",
    pass_form=PasswordChangeForm,
    success_url=None,
    extra_context=None,
):
    """ Change password of user.

    This view is almost a mirror of the view supplied in
    :func:`contrib.auth.views.password_change`, with the minor change that in
    this view we also use the username to change the password. This was needed
    to keep our URLs logical (and REST) across the entire application. And
    that in a later stadium administrators can also change the users password
    through the web application itself.

    :param username:
        String supplying the username of the user who's password is about to be
        changed.

    :param template_name:
        String of the name of the template that is used to display the password
        change form. Defaults to ``accounts/password_form.html``.

    :param pass_form:
        Form used to change password. Default is the form supplied by Django
        itself named ``PasswordChangeForm``.

    :param success_url:
        Named URL that is passed onto a :func:`reverse` function with
        ``username`` of the active user. Defaults to the
        ``accounts_password_complete`` URL.

    :param extra_context:
        Dictionary of extra variables that are passed on to the template. The
        ``form`` key is always used by the form supplied by ``pass_form``.

    **Context**

    ``form``
        Form used to change the password.

    """
    user = get_object_or_404(get_user_model(), username__iexact=username)

    form = pass_form(user=user)

    if request.method == "POST":
        form = pass_form(user=user, data=request.POST)
        if form.is_valid():
            form.save()

            # Send a signal that the password has changed
            accounts_signals.password_complete.send(sender=None, user=user)

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse(
                    "accounts_password_change_complete",
                    kwargs={"username": user.username},
                )
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["profile"] = user.get_profile()
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
def profile_edit(
    request,
    username,
    edit_profile_form=EditProfileForm,
    template_name="accounts/profile_form.html",
    success_url=None,
    extra_context=None,
    **kwargs
):
    """
    Edit profile.

    Edits a profile selected by the supplied username. First checks
    permissions if the user is allowed to edit this profile, if denied will
    show a 404. When the profile is successfully edited will redirect to
    ``success_url``.

    :param username:
        Username of the user which profile should be edited.

    :param edit_profile_form:

        Form that is used to edit the profile. The :func:`EditProfileForm.save`
        method of this form will be called when the form
        :func:`EditProfileForm.is_valid`.  Defaults to :class:`EditProfileForm`
        from accounts.

    :param template_name:
        String of the template that is used to render this view. Defaults to
        ``accounts/edit_profile_form.html``.

    :param success_url:
        Named URL which will be passed on to a django ``reverse`` function
        after the form is successfully saved. Defaults to the
        ``accounts_detail`` url.

    :param extra_context:
        Dictionary containing variables that are passed on to the
        ``template_name`` template.  ``form`` key will always be the form used
        to edit the profile, and the ``profile`` key is always the edited
        profile.

    **Context**

    ``form``
        Form that is used to alter the profile.

    ``profile``
        Instance of the ``Profile`` that is edited.

    """
    user = get_object_or_404(get_user_model(), username__iexact=username)

    profile = user.get_profile()

    user_initial = {"first_name": user.first_name, "last_name": user.last_name}

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == "POST":
        form = edit_profile_form(
            request.POST, request.FILES, instance=profile, initial=user_initial
        )

        if form.is_valid():
            profile = form.save()

            if accounts_settings.ACCOUNTS_USE_MESSAGES:
                messages.success(
                    request, _("Your profile has been updated."), fail_silently=True
                )

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse(
                    "accounts_profile_detail", kwargs={"username": username}
                )
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["profile"] = profile
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


def profile_detail(
    request,
    username,
    template_name=accounts_settings.ACCOUNTS_PROFILE_DETAIL_TEMPLATE,
    extra_context=None,
    **kwargs
):
    """
    Detailed view of an user.

    :param username:
        String of the username of which the profile should be viewed.

    :param template_name:
        String representing the template name that should be used to display
        the profile.

    :param extra_context:
        Dictionary of variables which should be supplied to the template. The
        ``profile`` key is always the current profile.

    **Context**

    ``profile``
        Instance of the currently viewed ``Profile``.

    """
    user = get_object_or_404(get_user_model(), username__iexact=username)
    profile_model = get_profile_model()
    try:
        profile = user.get_profile()
    except profile_model.DoesNotExist:
        profile = profile_model(user=user)
        profile.save()
    if not profile.can_view_profile(request.user):
        return HttpResponseForbidden(
            _("You don't have permission to view this profile.")
        )
    if not extra_context:
        extra_context = dict()
    extra_context["profile"] = user.get_profile()
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


def account_delete(
    request,
    username,
    template_name=accounts_settings.ACCOUNTS_PROFILE_DETAIL_TEMPLATE,
    extra_context=None,
    **kwargs
):
    """
    Delete an account.
    """
    user = get_object_or_404(get_user_model(), username__iexact=username)
    user.is_active = False
    user.save()

    return redirect(reverse("accounts_admin"))


class ProfileListView(ListView):
    """
    Lists all profiles
    """

    context_object_name = "profile_list"
    page = 1
    paginate_by = 20
    template_name = "accounts/profile_list.html"
    extra_context = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get("page", None))
        except (TypeError, ValueError):
            page = self.page

        if not self.request.user.is_staff:
            raise Http404

        if not self.extra_context:
            self.extra_context = dict()

        context["page"] = page
        context["paginate_by"] = self.paginate_by
        context["extra_context"] = self.extra_context

        context["form"] = SignupForm()

        return context

    def get_queryset(self):
        profile_model = get_profile_model()
        queryset = profile_model.objects.get_visible_profiles(self.request.user)
        return queryset


class AccountsFormView(FormView, MultipleObjectMixin):
    template_name = "accounts/profile_list.html"
    form_class = SignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse("accounts_admin", kwargs=None)

    def form_valid(self, form):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()

        user = form.save()

        # Send the signup complete signal
        accounts_signals.signup_complete.send(sender=None, user=user)

        # record the interest using the message in form.cleaned_data
        return super().form_valid(form)


class AccountsListView(View):
    def get(self, request, *args, **kwargs):
        view = ProfileListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AccountsFormView.as_view()
        return view(request, *args, **kwargs)
