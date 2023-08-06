from django.forms.widgets import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe

try:
    from ..cms.internal_tags.fields import TaggedRelationWidget
    from ..cms.widgets import APIChoiceWidget
except ValueError:
    from cms.internal_tags.fields import TaggedRelationWidget
    from cms.widgets import APIChoiceWidget


class AssetsFileWidget(TaggedRelationWidget):
    crop_link = "crops/{0}/edit/"

    def get_qs(self):
        qs = super().get_qs()
        if self.asset_type:
            qs["ftype"] = self.asset_type
        return qs

    def get_add_qs(self):
        qs = self.get_qs()
        if "ftype" in qs:
            qs["type"] = qs.pop("ftype")
        return qs

    def get_crop_sizes(self):
        from . import get_image_cropper

        sizes = []
        if self.sizes:
            for x in self.sizes:
                crop = get_image_cropper().get_crop_config(x)
                if crop and crop.editable:
                    sizes.append(
                        {
                            "name": crop.name,
                            "width": crop.width,
                            "height": crop.height,
                            "post_link": self.crop_link.format(x),
                        }
                    )
        return sizes

    def render(self, name, value, attrs=None, renderer=None):
        obj = self.obj_for_value(value)
        # Go directly to parent of APIChoiceWidget to get input
        hidden_input = super(APIChoiceWidget, self).render(name, value, attrs=attrs, renderer=None)

        context = {
            "hidden_input": hidden_input,
            "object": obj,
            "asset_type": self.asset_type,
            "asset_tags": self.tags,
            "link": self.get_api_link(),
            "add_link": self.get_add_link(),
            "base_api_link": self._api_link,
            "sizes": self.get_crop_sizes(),
            "required_tags": self.required_tags,
        }
        html = render_to_string("assets/asset_widget.html", context)
        return mark_safe(html)


class RawImageWidget(ClearableFileInput):
    template_with_initial = (
        "%(initial_text)s: %(initial)s %(clear_template)s<br />%(input)s"
    )

    def render(self, name, value, attrs=None, renderer=None):
        thumbnail = None
        data = super().render(name, value, attrs, renderer=None)

        if value and hasattr(value, "admin_url"):
            thumbnail = value.admin_url()
        if thumbnail:
            data = mark_safe(
                '<p class="widget-asset-simple"><span class="widget-asset-simple-preview" style="background-image:url({0})"></span>{1}</p>'.format(
                    escape(thumbnail), data
                )
            )

        return data
