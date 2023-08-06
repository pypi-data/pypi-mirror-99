import os
import uuid
import urllib.parse

from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.forms.forms import pretty_name

from . import get_image_cropper, settings, signals, tasks, utils
from .fields import AssetRealFileField
from .managers import AssetManager

try:
    from ..versioning import manager
except ValueError:
    from versioning import manager

try:
    from ..cms.internal_tags.models import AutoTagModel
except ValueError:
    from cms.internal_tags.models import AutoTagModel


class AssetBase(AutoTagModel):
    UNKNOWN = "unknown"
    IMAGE = "image"
    SVG_IMAGE = "svg_image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"

    TYPES = (
        settings.ASSET_TYPES
        and settings.ASSET_TYPES
        or (
            (UNKNOWN, "Unknown"),
            (IMAGE, "Image"),
            (SVG_IMAGE, "SVG Image"),
            (DOCUMENT, "Document"),
            (AUDIO, "Audio"),
            (VIDEO, "Video"),
        )
    )

    __original_file = None

    title = models.CharField(max_length=255)
    file = AssetRealFileField(upload_to=utils.assets_dir)
    type = models.CharField(max_length=255, choices=TYPES, db_index=True)
    slug = models.SlugField(unique=True, max_length=255)
    user_filename = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cbversion = models.PositiveIntegerField(editable=False)

    objects = AssetManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_file = self.file

    def rename_file(self):
        if self.type == self.DOCUMENT:
            return False
        return settings.HASH_FILENAME

    def url(self):
        """
        This is a wrapper of file.url
        """
        return self.file.url

    def generate_slug(self):
        return str(uuid.uuid1())

    def assign_tag(self):
        pass

    def delete_real_file(self, file_obj):
        file_obj.storage.delete(file_obj.name)
        signals.file_removed.send(file_obj.name)

    def _can_crop(self):
        return self.type == self.IMAGE

    def reset_crops(self):
        """
        Reset all known crops to the default crop.

        If settings.ASSET_CELERY is specified then
        the task will be run async
        """

        if self._can_crop():
            if settings.CELERY or settings.USE_CELERY_DECORATOR:
                # this means that we are using celery
                tasks.reset_crops.apply_async(args=[self.pk], countdown=5)
            else:
                tasks.reset_crops(None, asset=self)

    def ensure_crops(self, *required_crops):
        """
        Make sure a crop exists for each crop in required_crops.
        Existing crops will not be changed.

        If settings.ASSET_CELERY is specified then
        the task will be run async
        """
        if self._can_crop():
            if settings.CELERY or settings.USE_CELERY_DECORATOR:
                # this means that we are using celery
                args = [self.pk] + list(required_crops)
                tasks.ensure_crops.apply_async(args=args, countdown=5)
            else:
                tasks.ensure_crops(None, *required_crops, asset=self)

    def create_urls_json(self, crops):
        """
        Create JSON with base and all cropped image's urls.
        """
        urls = {"base": self.file.url}

        _, extension = os.path.splitext(self.file.name)
        if extension == "svg" or extension == ".svg":
            urls["svg"] = self.file.read().decode("utf-8")
            return urls

        if not self._can_crop():
            return urls

        crops.extend(get_image_cropper().required_crops())
        for size in crops:
            url_parts = list(urllib.parse.urlsplit(self.file.url))
            url_parts[2] = utils.get_size_filename(url_parts[2], size)
            urls[size] = urllib.parse.urlunsplit(url_parts)

        return urls

    def create_crop(self, name, x, x2, y, y2):
        """
        Create a crop for this asset.
        """
        if self._can_crop():
            spec = get_image_cropper().create_crop(
                name, self.file, x=x, x2=x2, y=y, y2=y2
            )
            ImageDetail.save_crop_spec(self, spec)

    def save(self, *args, **kwargs):
        """
        For new assets, creates a new slug.
        For updates, deletes the old file from storage.

        Calls super to actually save the object.
        """
        if not self.pk and not self.slug:
            self.slug = self.generate_slug()

        if self.__original_file and self.file != self.__original_file:
            self.delete_real_file(self.__original_file)

        file_changed = True
        if self.pk:
            new_value = getattr(self, "file")
            if hasattr(new_value, "file"):
                file_changed = isinstance(new_value.file, UploadedFile)
        else:
            self.cbversion = 0

        if file_changed:
            self.user_filename = os.path.basename(self.file.name)
            self.cbversion = self.cbversion + 1

        if not self.title:
            self.title = self.user_filename

        super().save(*args, **kwargs)

        if file_changed:
            signals.file_saved.send(self.file.name)
            utils.update_cache_bust_version(self.file.url, self.cbversion)
            self.reset_crops()

        if self.__original_file and self.file.name != self.__original_file.name:
            with manager.SwitchSchemaManager(None):
                for related in self.__class__._meta.get_fields(include_hidden=True):
                    field = related.field if hasattr(related, 'field') else None
                    if getattr(field, "denormalize", None):
                        cname = field.get_denormalized_field_name(field.name)
                        if getattr(field, "denormalize"):
                            related_objs = related.related_model.objects.filter(
                                **{field.name: self.pk}
                            )
                            for obj in related_objs:
                                getattr(obj, cname)["base"] = self.file.name

                            related_objs.bulk_update(related_objs, [cname,])

    def delete(self, *args, **kwargs):
        """
        Deletes the actual file from storage after the object is deleted.

        Calls super to actually delete the object.
        """
        file_obj = self.file
        super().delete(*args, **kwargs)
        self.delete_real_file(file_obj)

    def __str__(self):
        return self.user_filename


class ImageDetailBase(models.Model):
    image = models.ForeignKey(settings.ASSET_MODEL, on_delete=models.CASCADE)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    name = models.CharField(max_length=255)
    editable = models.BooleanField(editable=False, default=False)

    x = models.PositiveIntegerField(null=True)
    x2 = models.PositiveIntegerField(null=True)
    y = models.PositiveIntegerField(null=True)
    y2 = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return pretty_name(self.name)

    def get_crop_config(self):
        return get_image_cropper().get_crop_config(self.name)

    @classmethod
    def save_crop_spec(cls, asset, spec, update_version=True):
        if spec:
            cdict = spec.to_dict()
            updated = cls.objects.filter(image=asset, name=cdict["name"]).update(
                **cdict
            )
            if not updated:
                cls(image=asset, **cdict).save()

            if update_version:
                asset.__class__.objects.filter(pk=asset.pk).update(
                    cbversion=models.F("cbversion") + 1
                )


class Asset(AssetBase):
    class Meta:
        abstract = False


class ImageDetail(ImageDetailBase):
    class Meta:
        abstract = False
