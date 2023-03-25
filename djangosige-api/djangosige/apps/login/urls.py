from django.urls import re_path

from . import views

app_name = "login"
urlpatterns = [
    # login/
    re_path(r"^$", views.UserFormView.as_view(), name="loginview"),
    # login/registrar/
    re_path(r"registrar/$", views.UserRegistrationFormView.as_view(), name="registrarview"),
    # login/esqueceu/:
    re_path(r"^esqueceu/$", views.ForgotPasswordView.as_view(), name="esqueceuview"),
    # login/trocarsenha/:
    re_path(
        r"^trocarsenha/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$",
        views.PasswordResetConfirmView.as_view(),
        name="trocarsenhaview",
    ),
    # logout
    re_path(r"^logout/$", views.UserLogoutView.as_view(), name="logoutview"),
    # login/perfil/
    re_path(r"^perfil/$", views.MeuPerfilView.as_view(), name="perfilview"),
    # login/editarperfil/
    re_path(r"^editarperfil/$", views.EditarPerfilView.as_view(), name="editarperfilview"),
    # login/usuarios/
    re_path(r"^usuarios/$", views.UsuariosListView.as_view(), name="usuariosview"),
    # login/usuarios/(id_usuario)
    re_path(
        r"usuarios/(?P<pk>[0-9]+)/$",
        views.UsuarioDetailView.as_view(),
        name="usuariodetailview",
    ),
    # deletar usuario
    re_path(
        r"deletaruser/(?P<pk>[0-9]+)/$",
        views.DeletarUsuarioView.as_view(),
        name="deletarusuarioview",
    ),
    # permissoes usuario
    re_path(
        r"permissoesusuario/(?P<pk>[0-9]+)/$",
        views.EditarPermissoesUsuarioView.as_view(),
        name="permissoesusuarioview",
    ),
    # selecionar empresa
    re_path(
        r"selecionarempresa/$",
        views.SelecionarMinhaEmpresaView.as_view(),
        name="selecionarempresaview",
    ),
]
