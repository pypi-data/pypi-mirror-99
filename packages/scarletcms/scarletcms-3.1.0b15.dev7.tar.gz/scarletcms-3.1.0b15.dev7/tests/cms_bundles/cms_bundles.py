from django.forms.models import inlineformset_factory

from scarlet.cms import bundles, forms, options, views, renders, actions
from scarlet.cms.sites import site

from .models import Post, PostImage, Comment, Category, Tag, Author, DummyModel
from .views import PostsListView
from .forms import EditAuthorForm

postimages_formset = forms.LazyFormSetFactory(
    inlineformset_factory, Post, PostImage, can_order=True
)


class CloneAction(actions.ActionView):
    short_description = "Clone selected posts."

    def process_action(self, request, queryset):
        for obj in queryset:
            post = Post.objects.create(
                date=obj.date,
                title=obj.title,
                slug=obj.slug,
                body=obj.body,
                author=obj.author,
                category=obj.category,
                tag=obj.tags,
                keywords=obj.keywords,
                description=obj.description,
            )
        num = queryset.count()
        msg = f"{num} object{'s' if num == 1 else ''} have been cloned."
        self.write_message(message=msg)
        return self.render(request, redirect_url=self.get_done_url(), message=msg)


class CloneCommentAction(actions.ActionView):
    short_description = "Clone selected comments."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renders["object_header"] = renders.RenderString(
            template=self.object_header_tmpl
        )

    def process_action(self, request, queryset):
        for obj in queryset:
            comment = Comment.objects.create(
                post=obj.post, name=obj.name, text=obj.text
            )
        num = queryset.count()
        msg = f"{num} object{'' if num == 1 else 's'} have been cloned."
        self.write_message(message=msg)
        return self.render(request, redirect_url=self.get_done_url(), message=msg)


class DummyActionView(actions.ActionView):
    def process_action(self, request, queryset):
        queryset.update(title="Dummy")
        count = queryset.count()
        msg = (
            f'{count} object{"" if count == 1 else "s"} '
            'have been changed to "Dummy".'
        )
        self.write_message(message=msg)
        return self.render(request, redirect_url=self.get_done_url(), message=msg)


class SomethingAction(actions.ActionView):
    short_description = "It does something."
    confirmation_message = "Sure you want to do something to the following objects?"

    def process_action(self, request, queryset):
        queryset.update(name="Something")


class PostImageBundle(bundles.Bundle):
    navigation = bundles.PARENT

    class Meta(options.Orderable):
        model = PostImage


class CategoryBundle(bundles.Bundle):
    navigation = bundles.PARENT
    main = views.ListView(
        paginate_by=1, display_fields=("category",), change_fields=("category",)
    )

    class Meta:
        model = Category
        primary_model_bundle = True


class TagBundle(bundles.Bundle):
    navigation = bundles.PARENT
    main = views.ListView(
        paginate_by=1, display_fields=("tag",), change_fields=("tag",)
    )

    class Meta:
        model = Tag
        primary_model_bundle = True


class CommentBundle(bundles.ParentVersionedBundle, bundles.VersionMixin):
    navigation = bundles.PARENT
    object_view = bundles.PARENT
    clone = CloneCommentAction()
    main = views.ListView(display_fields=("name", "text"))
    something = SomethingAction()

    class Meta:
        model = Comment
        parent_field = "post"
        action_views = ["delete", "clone", "something", "publish", "unpublish"]


class AuthorBundle(bundles.Bundle):
    navigation = bundles.PARENT
    edit = views.FormView(form_class=EditAuthorForm)
    main = views.ListView(filter_form=forms.search_form("name", "bio",))

    class Meta:
        model = Author


class DummyAliasBundle(bundles.Bundle):
    dummy_edit = views.FormView()
    edit = bundles.URLAlias(alias_to="dummy_edit")

    class Meta:
        model = DummyModel
        item_views = ("dummy_edit", "delete")


class DummyRedirectorBundle(bundles.Bundle):
    edit = views.FormView(redirect_to_view="edit")

    class Meta:
        model = DummyModel
        item_views = ("edit", "delete")


DEFAULT_FIELDS = (
    ("Post", {"fields": ("date", "title", "body", "author", "category", "tags")}),
)


class PostDeleteView(actions.DeleteActionView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renders["object_header_bare"] = renders.RenderString(
            template="cms/object_header_bare.html"
        )


class BlogEditBundle(bundles.VersionedObjectOnlyBundle):
    navigation = (
        ("main", "Post Data"),
        ("comments", "Comments"),
        ("seo", "Page SEO"),
        ("delete", "Delete"),
        ("publish", "Publish"),
        ("unpublish", "Unpublish"),
    )

    main = views.FormView(
        redirect_to_view=None,
        formsets={"Images": postimages_formset},
        fieldsets=DEFAULT_FIELDS,
    )

    delete = PostDeleteView()
    edit = bundles.PARENT
    comments = CommentBundle.as_subbundle(name="comments", title="Comments",)
    seo = views.FormView(
        redirect_to_view=None,
        cancel_view=None,
        fieldsets=(("SEO", {"fields": ("keywords", "description",)}),),
    )

    class Meta:
        model = Post


class PostAddView(views.FormView):
    def get(self, request, *args, **kwargs):
        if not self.model.category.get_query_set():
            self.write_message(
                status=30,
                message="Warning! You need at least one Category to insert new Posts.",
            )
        if not self.model.author.get_query_set():
            self.write_message(
                status=30,
                message="Warning! You need at least one Author to insert new Posts.",
            )
        return super().get(request, *args, **kwargs)


class BlogBundle(bundles.DelegatedObjectBundle):
    dashboard = (
        ("main",),
        ("author",),
        ("dummy_alias",),
        ("dummy_redirector",),
        ("category",),
        ("tag",),
    )

    main = views.ListView(display_fields=("title", "author"))
    delete = actions.DeleteActionView()
    add = PostAddView(fieldsets=DEFAULT_FIELDS)
    edit = BlogEditBundle.as_subbundle(name="post", title="Post")
    author = AuthorBundle.as_subbundle(name="author", title="Author")
    dummy_alias = DummyAliasBundle.as_subbundle(name="dummy_alias", title="Dummy Alias")
    dummy_redirector = DummyRedirectorBundle.as_subbundle(
        name="dummy_redirector", title="Dummy Redirect"
    )
    category = CategoryBundle.as_subbundle(name="category", title="Category")
    tag = TagBundle.as_subbundle(name="tag", title="Tag")
    preview = views.PreviewWrapper(preview_view=PostsListView, pass_through_kwarg=None)
    change = DummyActionView(short_description="Change names to 'Dummy'")
    clone = CloneAction()

    class Meta:
        model = Post
        primary_model_bundle = True
        item_views = list(options.VersionMeta.item_views) + ["preview"]
        action_views = ["change", "delete", "clone"]


class BigAuthorBundle(bundles.DelegatedObjectBundle):
    dashboard = (("author",),)

    author = AuthorBundle.as_subbundle(name="author", title="Author")


class DummySingletonBundle(bundles.SingletonBundle):
    dashboard = (("main",),)
    edit = views.SingletonFormView()
    main = edit

    class Meta:
        model = DummyModel
        primary_model_bundle = False


site.register("dummy", BlogBundle(name="dummy"), order=10)
site.register("authoronly", BigAuthorBundle(name="authoronly"), order=10)
site.register("dummysingleton", DummySingletonBundle(name="dummysingleton"), order=10)
