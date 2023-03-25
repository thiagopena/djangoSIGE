""" Definições da URLs """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

from djangosige.contrib.swagger.views import schema_view

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^", include("djangosige.apps.base.urls")),
    re_path(r"^login/", include("djangosige.apps.login.urls")),
    re_path(r"^cadastro/", include("djangosige.apps.cadastro.urls")),
    re_path(r"^fiscal/", include("djangosige.apps.fiscal.urls")),
    re_path(r"^vendas/", include("djangosige.apps.vendas.urls")),
    re_path(r"^compras/", include("djangosige.apps.compras.urls")),
    re_path(r"^financeiro/", include("djangosige.apps.financeiro.urls")),
    re_path(r"^estoque/", include("djangosige.apps.estoque.urls")),
]

if settings.DEBUG:
    urlpatterns = (
        urlpatterns
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    )
