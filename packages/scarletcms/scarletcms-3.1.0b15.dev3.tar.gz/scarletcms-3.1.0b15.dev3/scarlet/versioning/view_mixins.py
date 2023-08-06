from django import http
from django.views.generic.detail import SingleObjectMixin

from . import manager


class PreviewableObject(SingleObjectMixin):
    """
    View that can get an unpublished version of an
    object
    """

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        Copied from SingleObjectMixin except that this allows
        us to lookup preview objects.
        """

        schema = manager.get_schema()
        vid = None
        if (
            self.request.GET.get("vid")
            and self.request.user.is_staff
            and self.request.user.is_active
        ):
            try:
                schema = "public"
                vid = int(self.request.GET.get("vid"))
                queryset = self.model.normal.filter(vid=vid)
            except ValueError:
                pass

        with manager.SwitchSchema(schema):
            # Use a custom queryset if provided
            if queryset is None:
                queryset = self.get_queryset()

            # Next, try looking up by primary key.
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            slug = self.kwargs.get(self.slug_url_kwarg, None)
            if pk is not None:
                if vid:
                    queryset = queryset.filter(vid=vid)
                else:
                    queryset = queryset.filter(object_id=pk)

            # Next, try looking up by slug.
            elif slug is not None:
                slug_field = self.get_slug_field()
                queryset = queryset.filter(**{slug_field: slug})

            # If none of those are defined, it's an error.
            else:
                raise AttributeError(
                    f"View {self.__class__.__name__} must be called "
                    "with either an object pk or a slug."
                )

            try:
                obj = queryset.get()
            except queryset.model.DoesNotExist:
                raise http.Http404(
                    f"No {queryset.model._meta.verbose_name} found matching the query"
                )

        return obj
