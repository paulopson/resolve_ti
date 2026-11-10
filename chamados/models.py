from django.db import models


class Chamado(models.Model):
    titulo = models.CharField(max_length=150, blank=False)
    descricao = models.TextField(blank=False)

    class Prioridade(models.TextChoices):
        BAIXA = "baixa", "Baixa"  # ! BAIXA = valor armazenada no python
        MEDIA = "media", "Média"  # ! "media" = valor que sera aramazenada no banco de dados
        ALTA = "alta", "Alta"     # ! "Alta" = Texto apresentado ao usuario

    prioridade = models.CharField(max_length=15, choices=Prioridade.choices, default=Prioridade.MEDIA)

    class Status(models.TextChoices):
        ABERTO = 'aberto', "Aberto"
        EM_ANDAMENTO = 'em_andamento', "Em andamento"
        RESOLVIDO = 'resolvido', 'Resolvido'

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)



""" Campo	Regra
id	Identificador único
titulo	Texto obrigatório
descricao	Texto obrigatório
prioridade	Baixa, média ou alta
status	Aberto, em andamento ou resolvido
criado_em	Data e hora automáticas na criação
atualizado_em	Data e hora da última atualização """
