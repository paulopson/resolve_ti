from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Chamado
from .serializers import ChamadoSerializer


@api_view(["GET"])
def listar_chamados(request):
    listar = Chamado.objects.all()
    serializer = ChamadoSerializer(listar, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def buscar_chamado(request, id):
    chamado_por_id = get_object_or_404(Chamado, pk=id)
    serializer = ChamadoSerializer(chamado_por_id)
    return Response(serializer.data)
