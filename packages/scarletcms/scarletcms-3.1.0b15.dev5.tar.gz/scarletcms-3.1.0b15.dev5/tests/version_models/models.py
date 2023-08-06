from django.db import models

from scarlet.assets.fields import AssetsFileField
from scarlet.assets.models import Asset
from scarlet.versioning import fields
from scarlet.versioning.models import (
    VersionView,
    Cloneable,
    BaseModel,
    BaseVersionedModel,
)


class Harmless:
    is_harmless = True


class ConcreteModel(models.Model):
    name = models.CharField(max_length=255)


class NameModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Abstract(BaseVersionedModel, NameModel):
    associates = fields.M2MFromVersion("self", blank=True)

    class Meta:
        abstract = True


class Author(VersionView, Abstract):
    def __str__(self):
        return self.name


class Cartoon(VersionView, NameModel):
    author = models.ForeignKey(
        Author, related_name="works", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class AbstractM2MBook(models.Model):
    books = fields.M2MFromVersion("Book", blank=True)
    cartoon = fields.FKToVersion(
        Cartoon, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class Gallery(Cloneable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(VersionView, NameModel, Harmless):
    _clone_related = ["review", "galleries"]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    galleries = fields.M2MFromVersion(Gallery)

    def __str__(self):
        return self.name


class BookNoRelated(VersionView, NameModel, Harmless):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    galleries = fields.M2MFromVersion(Gallery)

    def __str__(self):
        return self.name


class Review(Cloneable):
    book = fields.FKToVersion(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Store(VersionView, NameModel, AbstractM2MBook):
    pass


class NoReverse(VersionView, NameModel):
    _clone_related = ("rm2m",)


class RM2M(Cloneable):
    no = models.ManyToManyField(NoReverse)


class Image(Cloneable):
    name = models.CharField(max_length=255)
    image = AssetsFileField(type=Asset.IMAGE, blank=True, null=True)
    cartoons = models.ManyToManyField(Cartoon)

    def __str__(self):
        return self.name


class CustomModel(BaseModel):
    reg_number = models.CharField(max_length=20)


class Gun(VersionView):
    name = models.CharField(max_length=20)

    class Meta:
        _base_model = CustomModel
