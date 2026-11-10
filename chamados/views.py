from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Chamado
from .serializers import ChamadoSerializer


@api_view(["GET", "POST"])
def chamados(request):
    if request.method == "GET":
        listar = Chamado.objects.all()
        serializer = ChamadoSerializer(listar, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ChamadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def buscar_chamado(request, id):
    chamado_por_id = get_object_or_404(Chamado, pk=id)
    serializer = ChamadoSerializer(chamado_por_id)
    return Response(serializer.data)
