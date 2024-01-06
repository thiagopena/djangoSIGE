"""URL configuration for DjangoSIGE project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangosige.base.urls")),
    path("login/", include("djangosige.login.urls")),
    path("cadastro/", include("djangosige.cadastro.urls")),
    path("fiscal/", include("djangosige.fiscal.urls")),
    path("vendas/", include("djangosige.vendas.urls")),
    path("compras/", include("djangosige.compras.urls")),
    path("financeiro/", include("djangosige.financeiro.urls")),
    path("estoque/", include("djangosige.estoque.urls")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
