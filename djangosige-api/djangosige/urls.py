from django.urls import include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from .configs.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('djangosige.apps.base.urls')),
    re_path(r'^login/', include('djangosige.apps.login.urls')),
    re_path(r'^cadastro/', include('djangosige.apps.cadastro.urls')),
    re_path(r'^fiscal/', include('djangosige.apps.fiscal.urls')),
    re_path(r'^vendas/', include('djangosige.apps.vendas.urls')),
    re_path(r'^compras/', include('djangosige.apps.compras.urls')),
    re_path(r'^financeiro/', include('djangosige.apps.financeiro.urls')),
    re_path(r'^estoque/', include('djangosige.apps.estoque.urls')),
]

if DEBUG is True:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
