import pytest
from rest_framework.test import APIClient

from chamados.models import Chamado


@pytest.mark.django_db
def test_listar_chamados():
    client = APIClient()

    response = client.get("/api/chamados/")

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_listar_chamados_com_registro():
    client = APIClient()
    data = Chamado.objects.create(
        titulo="Computador não liga",
        descricao="O equipamento não inica.",
        prioridade="alta",
    )

    response = client.get("/api/chamados/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["titulo"] == data.titulo
    assert response.data[0]["descricao"] == data.descricao
    assert response.data[0]["prioridade"] == data.prioridade
    assert response.data[0]["status"] == "aberto"


@pytest.mark.django_db
def test_criar_chamado():
    client = APIClient()
    dados = {
        "titulo": "Impressora com defeito",
        "descricao": "A impressora não está funcionando.",
        "prioridade": "alta",
    }
    response = client.post("/api/chamados/", data=dados, format="json")

    chamado_salvo = Chamado.objects.get()

    assert response.status_code == 201  # verifica se foi criado
    assert Chamado.objects.count() == 1  # verifica se foi salvo
    assert chamado_salvo.titulo == dados["titulo"]
    assert chamado_salvo.descricao == dados["descricao"]
    assert chamado_salvo.prioridade == dados["prioridade"]
    assert (
        chamado_salvo.status == "aberto"
    )  # verificando se o status inicial esta aberto


@pytest.mark.django_db
def test_criar_chamado_falha():
    client = APIClient()

    dados = {
        "descricao": "O computador não liga.",
        "prioridade": "alta",
    }

    response = client.post("/api/chamados/", data=dados, format="json")

    assert response.status_code == 400
    assert Chamado.objects.count() == 0
    assert "titulo" in response.data


@pytest.mark.django_db
def test_atualizar_titulo_chamado():
    client = APIClient()

    chamado = Chamado.objects.create(
        titulo="Computador com defeito",
        descricao="Equipamento não funciona.",
        prioridade="media",
    )

    dados = {"titulo": "Computador reiniciando sozinho"}

    response = client.patch(f"/api/chamados/{chamado.id}/", data=dados, format="json")

    assert response.status_code == 200

    chamado.refresh_from_db()

    assert chamado.titulo == dados["titulo"]  # Confirma que titulo foi alterado
    assert chamado.descricao == "Equipamento não funciona."  # Confirma que descricao nao foi alterada.
    assert chamado.prioridade == "media"  # Confirma que prioridade nao foi alterada.
    assert chamado.status == "aberto"  # Confirma que status nao foi alterado.


@pytest.mark.django_db
def test_impedir_edicao_chamado_resolvido():
    client = APIClient()

    chamado = Chamado.objects.create(
        titulo="Computador com defeito",
        descricao="Equipamento não funciona.",
        prioridade="media",
        status="resolvido",
    )

    dados = {
        "titulo": "computador não liga",
    }

    response = client.patch(f"/api/chamados/{chamado.id}/", data=dados, format="json")

    assert response.status_code == 409  # Confirma que a edição foi rejeitada
    chamado.refresh_from_db()
    assert chamado.titulo == "Computador com defeito"


@pytest.mark.django_db
def test_impedir_reabertura_chamado_resolvido():
    client = APIClient()

    chamado = Chamado.objects.create(
        titulo="Computador com defeito",
        descricao="Equipamento não funciona.",
        prioridade="media",
        status="resolvido",
    )
    dados = {"status": "aberto"}
    response = client.patch(f"/api/chamados/{chamado.id}/status/", data=dados, format="json")

    assert response.status_code == 400
    chamado.refresh_from_db()
    assert chamado.status == "resolvido"


@pytest.mark.django_db
def test_alterar_status_para_em_andamento():
    client = APIClient()

    chamado = Chamado.objects.create(
        titulo="Computador com defeito",
        descricao="Equipamento não funciona.",
        prioridade="media",
        status="aberto",
    )
    dados = {"status": "em_andamento"}
    response = client.patch(f"/api/chamados/{chamado.id}/status/", data=dados, format="json")

    assert response.status_code == 200
    chamado.refresh_from_db()
    assert chamado.status == "em_andamento"


@pytest.mark.django_db
def test_finalizar_chamado():
    client = APIClient()

    chamado = Chamado.objects.create(
        titulo="Computador com defeito",
        descricao="Equipamento não funciona",
        prioridade="media",
        status="em_andamento",
    )
    dados = {"status": "resolvido"}
    response = client.patch(f"/api/chamados/{chamado.id}/status/", data=dados, format="json")

    assert response.status_code == 200
    chamado.refresh_from_db()
    assert chamado.status == "resolvido"
    assert chamado.titulo == "Computador com defeito"
    assert chamado.descricao == "Equipamento não funciona"
    assert chamado.prioridade == "media"


@pytest.mark.django_db
def test_atualizar_chamado_inexistente():
    client = APIClient()

    dados = {"titulo": "Fonte queimada"}
    response = client.patch("/api/chamados/999/", data=dados, format="json")

    assert response.status_code == 404
    assert Chamado.objects.count() == 0


@pytest.mark.django_db()
def test_atualizar_prioridade_invalida():
    client = APIClient()
    chamado = Chamado.objects.create(
        titulo="Computador nao liga",
        descricao="Fonte queimada",
        prioridade="media",
        status="aberto"
    )

    dados = {"prioridade": "Urgente"}
    response = client.patch(f"/api/chamados/{chamado.id}/", data=dados, format="json")

    assert response.status_code == 400
    chamado.refresh_from_db()
    assert "prioridade" in response.data  # Verifica se a resposta contém um erro no campo prioridade.
    assert chamado.prioridade == "media"


@pytest.mark.django_db()
def test_filtrar_chamados_por_status():
    client = APIClient()
    chamado = Chamado.objects.create(
        titulo="Computador nao liga",
        descricao="Fonte queimada",
        prioridade="media",
        status="aberto"
    )
    chamado1 = Chamado.objects.create(
            titulo="Impressora nao imprime",
            descricao="Cabo frouxo",
            prioridade="baixa",
            status="em_andamento"
    )
    chamado2 = Chamado.objects.create(
            titulo="Problemas com internet",
            descricao="Cabo rompido",
            prioridade="alta",
            status="aberto"
    )

    response = client.get("/api/chamados/?status=aberto")

    assert response.status_code == 200
    assert len(response.data) == 2
    for chamado_retornado in response.data:
        assert chamado_retornado["status"] == "aberto"


@pytest.mark.django_db()
def test_filtrar_status_invalido():
    client = APIClient()
    response = client.get("/api/chamados/?status=cancelado")

    assert response.status_code == 400
    assert "detail" in response.data
