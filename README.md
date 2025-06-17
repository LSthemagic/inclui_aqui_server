````markdown
# IncluiAqui Server

API backend **IncluiAqui** construída com FastAPI, SQLAlchemy (asyncio) e PostgreSQL, que expõe endpoints para busca e avaliação de estabelecimentos, autenticação via JWT, e registro de feedbacks de acessibilidade.

---

## 📦 Tecnologias

- **Python ≥3.13**  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [SQLAlchemy 2.x (asyncio)](https://docs.sqlalchemy.org/)  
- [Alembic](https://alembic.sqlalchemy.org/) para migrações  
- PostgreSQL (via `asyncpg` ou `psycopg2-binary`)  
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências  
- [python-jose](https://pypi.org/project/python-jose/) + Passlib/Bcrypt para auth JWT  

---

## 🚀 Começando

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/inclui-aqui-server.git
cd inclui-aqui-server
````

### 2. Instale as dependências

```bash
poetry install
```

> Se você não usar *in-project* venv, crie/ative um virtualenv:
>
> ```bash
> python -m venv .venv
> source .venv/bin/activate
> poetry install
> ```

### 3. Variáveis de ambiente

Copie o exemplo e ajuste seus valores (principalmente `DATABASE_URL` e chaves JWT):

```bash
cp env.example .env
# Edite .env com seu editor favorito:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/inclui_aqui
# SECRET_KEY=uma-chave-muito-secreta-e-complexa
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🏃 Executando a aplicação

```bash
poetry run uvicorn inclui_aqui_server.app:app --reload
```

* Acesse a **docs** interativa em:
  `http://localhost:8000/docs`
* Swagger UI alternativa:
  `http://localhost:8000/redoc`

---

## 🗄️ Banco de Dados & Migrações

1. **Criar o banco** (PostgreSQL):

   ```bash
   createdb inclui_aqui
   ```
2. **Gerar migrações** (quando alterar modelos):

   ```bash
   poetry run alembic revision --autogenerate -m "Minha nova migração"
   ```
3. **Aplicar migrações**:

   ```bash
   poetry run alembic upgrade head
   ```

O arquivo de configuração do Alembic está em `alembic.ini` e as versões ficam em `migrations/versions/`.

---

## 🔑 Autenticação JWT

* **Endpoint de token**

  ```http
  POST /token
  Content-Type: application/x-www-form-urlencoded

  username=seu_usuario&password=sua_senha
  ```

  * Retorna JSON:

    ```json
    {
      "access_token": "<JWT_TOKEN>",
      "token_type": "bearer"
    }
    ```

* **Protegendo rotas**
  Adicione header `Authorization: Bearer <JWT_TOKEN>` e use a dependência `get_current_user` para obter o usuário logado.

---

## 🧪 Testes

```bash
# Executa testes + cobertura
poetry run task test
```

* Os testes usam **pytest** e **pytest-cov**.
* Relatório HTML de cobertura será gerado em `htmlcov/`.

---

## ✍️ Lint & Formatação

* **Ruff** para lint:

  ```bash
  poetry run task lint
  ```
* **Ruff --fix** auto corrige problemas:

  ```bash
  poetry run task format
  ```
* **Black** (opcional, já integrado ao Ruff se você preferir).

---

## 🤝 Contribuindo

1. Faça um *fork* do projeto
2. Crie uma *branch* (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m "feat: adiciona X"`)
4. Abra um Pull Request

Por favor, siga o guia de estilo PEP 8 e escreva testes para suas alterações.

---

## 📄 Licença

Este projeto está sob a [MIT License](LICENSE).

---

<p align="center">
  <em>Feito com ♥ por Railan Santana</em>
</p>
```