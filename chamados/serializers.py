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


class ChamadoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = ["status"]
        extra_kwargs = {"status": {"required": True}}

    def validate_status(self, value):
        if self.instance is None:
            raise serializers.ValidationError(
                "É necessário informar um chamado existente"
            )
        if (
            (
                self.instance.status == "aberto"
                and (value == "resolvido" or value == "aberto")
            )
            or (self.instance.status == "em_andamento" and value == "aberto")
            or (self.instance.status == "resolvido")
        ):
            raise serializers.ValidationError("Transição não permitida.")
        return value
