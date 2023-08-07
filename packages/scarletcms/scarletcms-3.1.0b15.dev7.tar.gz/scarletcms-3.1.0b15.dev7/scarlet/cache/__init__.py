from .manager import cache_manager

default_app_config = "scarlet.cache.apps.AppConfig"


def autodiscover():
    """
    Copied from django source

    Auto-discover INSTALLED_APPS cache_groups.py modules and fail silently if
    not present. This forces an import on them to register any admin bits they
    may want.
    """

    import copy

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(cache_manager._registry)
            import_module(f"{app}.cache_manager")
        except Exception:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            cache_manager._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, "cache_manager"):
                raise

default_app_config = "scarlet.cache.apps.AppConfig"
