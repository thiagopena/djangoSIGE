""" Definições da URLs """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
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
