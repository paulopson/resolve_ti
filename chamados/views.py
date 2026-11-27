from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Chamado
from .serializers import ChamadoSerializer, ChamadoStatusSerializer


@api_view(["GET", "POST"])
def chamados(request):
    if request.method == "GET":
        status_filtro = request.query_params.get("status")
        prioridade_filtro = request.query_params.get("prioridade")
        status_validos = ["aberto", "em_andamento", "resolvido"]
        prioridades_validas = ["alta", "media", "baixa"]

        listar = Chamado.objects.all()

        if status_filtro is not None:
            if status_filtro not in status_validos:
                return Response(
                    {"detail": "Status invalido."}, status=status.HTTP_400_BAD_REQUEST
                )
            listar = listar.filter(status=status_filtro)

        if prioridade_filtro is not None:
            if prioridade_filtro not in prioridades_validas:
                return Response(
                    {"detail": "Prioridade invalida."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            listar = listar.filter(prioridade=prioridade_filtro)

        serializer = ChamadoSerializer(listar, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ChamadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH"])
def buscar_chamado(request, id):
    chamado_por_id = get_object_or_404(Chamado, pk=id)
    if request.method == "GET":
        serializer = ChamadoSerializer(chamado_por_id)
        return Response(serializer.data)

    elif request.method == "PATCH":
        if chamado_por_id.status == "resolvido":
            return Response(
                {"detail": "Chamados resolvidos não podem ser alterados."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = ChamadoSerializer(chamado_por_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def alterar_status(request, id):
    chamado_por_id = get_object_or_404(Chamado, pk=id)
    serializer = ChamadoStatusSerializer(chamado_por_id, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
