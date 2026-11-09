from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_chamados, name="listar_chamados"),
    path("<int:id>/", views.buscar_chamado, name="buscar_chamado"),

    ]
