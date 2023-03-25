from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="DjangoSIGE",
        default_version="v1",
        description="Sistema Integrado para Gestão Empresarial baseado em Django",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Thiago Pena <thiagopena01@gmail.com>"),
        license=openapi.License(name="The MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
