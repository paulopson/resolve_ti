# RESOLVE_TI

## Sobre o projeto
ResolveTI foi desenvolvido para organizar e acompanhar solicitações de suporte dentro de uma empresa. A API REST permiti cadastrar chamados, consultar solicitações, atualizar informações e acompanhar o andamento dos atendimentos.

## Tecnologias Utilizadas
- **Python:** Linguagem utilizada para desenvolver a lógica da aplicação.

- **Django:** Framework que fornece a estrutura principal do backend.

- **Django REST Framework:** Ferramenta utilizada para desenvolver os endpoints da API REST.

- **SQLite:** Banco de dados utilizado para armazenar os chamados.

- **Poetry:** Gerencia dependências e o ambiente virtual do projeto.

- **pytest:** Executa os testes automatizados que verificam o comportamento da API.

- **Git:** Controla as versões e o historico do código.

- **GitHub:** Hospeda o repositório e permite compartilhar e revisar alterações.

## Funcionalidades
- Cadastrar chamados no sistema.
- Consultar os chamados cadastrados.
- Atualizar informações de um chamado cadastrado no sistema.
- Filtrar chamados por status.
- Acompanhar o andamento dos atendimentos.
- Validação de dados, impedindo o cadastro de informações inválidas.
- Regas de negócio, um chamado resolvido não pode ser reaberto nem modificado.

## Instalação e execução
- Python: executa a aplicação.
- Poetry: instala e gerencia as dependências.
- Git: permite clonar o projeto do GitHub.

### Clonagem e instalação
Clone o repositório do GitHub:
```bash
git clone https://github.com/paulopson/resolve_ti.git
```
Acesse a pasta do projeto:
```bash
cd resolve_ti
```

Instale as dependências utilizando o Poetry:
```bash
poetry install
```

### Configurações de variaveis de ambiente
Na raiz do projeto, crie um arquivo chamado `.env` e adicione:
```dotenv
DJANGO_SECRET_KEY="SUA_CHAVE_SECRETA"
```

Para gerar uma chave segura::
```bash
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Substitua `SUA_CHAVE_SECRETA` pela chave gerada.

**Importante:** o arquivo `.env` contém informações sensíveis e não deve ser enviado ao GitHub.

### Executando o projeto
Primeiro, aplique as migrações para preparar o banco de dados:
```bash
poetry run python manage.py migrate
```

Depois, inicie o servidor de desenvolvimento do Django:
```bash
poetry run python manage.py runserver
```

A API estará disponível em:
`http://127.0.0.1:8000/api/chamados/`

### Testes automatizados
O ResolveTI possui testes automatizados desenvolvidos com pytest para verificar o funcionamento da API e suas regras de negócio.
Para executar os testes:
```bash
poetry run pytest
```

## Objetivo de aprendizado
Este projeto tem como objetivo desenvolver minhas habilidades em programação backend, utilizando Python e Django para construir uma API REST.
Durante o desenvolvimento, pretendo praticar organização de código, gerenciamento de dependências, versionamento com Git e testes automatizados.


## Status do Projeto
Em desenvolvimento -- MVP backend implementado.

A primeira versão da API REST está funcional, com cadastro, consulta, atualização e gerenciamento de status dos chamados, além de testes automatizados.
O projeto continuará em evolução com novas funcionalidades como autenticação de controle de permissões e uma interface frontend.