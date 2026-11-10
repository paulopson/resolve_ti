from django.urls import path

from . import views

urlpatterns = [
    path("", views.chamados, name="chamados"),
    path("<int:id>/", views.buscar_chamado, name="buscar_chamado"),

    ]
