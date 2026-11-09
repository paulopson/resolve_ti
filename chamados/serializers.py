from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "id",
            "titulo",
            "descricao",
            "prioridade",
            "status",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "status", "criado_em", "atualizado_em"]
