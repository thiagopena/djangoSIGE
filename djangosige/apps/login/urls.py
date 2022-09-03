from django.urls import re_path as url
from . import views

app_name = 'djangosige.apps.login'

urlpatterns = [
    # login/
    url(r'^$', views.UserFormView.as_view(), name='loginview'),

    # login/registrar/
    url(r'registrar/$', views.UserRegistrationFormView.as_view(),
        name='registrarview'),

    # login/esqueceu/:
    url(r'^esqueceu/$', views.ForgotPasswordView.as_view(), name='esqueceuview'),

    # login/trocarsenha/:
    url(r'^trocarsenha/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$',
        views.PasswordResetConfirmView.as_view(), name='trocarsenhaview'),

    # logout
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logoutview'),

    # login/perfil/
    url(r'^perfil/$', views.MeuPerfilView.as_view(), name='perfilview'),

    # login/editarperfil/
    url(r'^editarperfil/$', views.EditarPerfilView.as_view(), name='editarperfilview'),

    # login/usuarios/
    url(r'^usuarios/$', views.UsuariosListView.as_view(), name='usuariosview'),

    # login/usuarios/(id_usuario)
    url(r'usuarios/(?P<pk>[0-9]+)/$',
        views.UsuarioDetailView.as_view(), name='usuariodetailview'),

    # deletar usuario
    url(r'deletaruser/(?P<pk>[0-9]+)/$',
        views.DeletarUsuarioView.as_view(), name='deletarusuarioview'),

    # permissoes usuario
    url(r'permissoesusuario/(?P<pk>[0-9]+)/$',
        views.EditarPermissoesUsuarioView.as_view(), name='permissoesusuarioview'),

    # selecionar empresa
    url(r'selecionarempresa/$', views.SelecionarMinhaEmpresaView.as_view(),
        name='selecionarempresaview'),
]
