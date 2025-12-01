
# ADOTE+

Website de adoção de animais de rua, com foco em **ação social permanente**
para amparo aos animais abandonados.

Projeto acadêmico – **SENAI/SC**

---

## 🎯 Objetivo

Desenvolver um sistema web simples, responsivo e de fácil uso pela comunidade,
que conecte **adotantes**, **ONGs** e **voluntários** em uma corrente de adoção
responsável e cuidado com animais em situação de abandono.

Benefícios esperados:

- Engajamento social contínuo em prol dos animais;
- Apoio ao controle de zoonoses;
- Amparo a animais em situações insalubres;
- Transparência via auditoria das ações realizadas no sistema.

---

## 👥 Perfis de acesso

- **Visitante**
  - Acessa o mural público de animais disponíveis (cards);
  - Visualiza detalhes de cada animal.

- **Usuário (Adotante)**
  - Cria conta e faz login;
  - Solicita adoção de animais;
  - Acompanha seus pedidos em **Minhas Adoções**;
  - Visualiza e atualiza seus dados no **Perfil**.

- **Anunciante**
  - Cria conta e faz login;
  - Cadastra e gerencia animais encontrados (CRUD de animais);
  - Faz upload de fotos (convertidas para JPG e redimensionadas para tamanho padrão, evitando imagens muito grandes/pequenas);
  - Visualiza pedidos de adoção para seus animais;
  - Aprova ou nega pedidos com **mensagem obrigatória** para o adotante;
  - Visualiza seus dados no **Perfil**.

- **Admin**
  - Possui visão global de usuários;
  - Gerencia contas de usuários (CRUD);
  - Consulta **logs de auditoria** (histórico de ações do sistema) com filtro por usuário.

---

## 🏗 Arquitetura

Estrutura geral (monorepo simples):

```
adote_mais/
├── backend/          # API em FastAPI + SQLAlchemy
├── frontend/         # HTML/CSS/JS estáticos
└── README.md
```

### Tecnologias principais

**Backend**

- Framework: **FastAPI**
- ORM: **SQLAlchemy**
- Banco: **SQLite** (desenvolvimento; facilmente substituível por PostgreSQL/MySQL)
- Auth: OAuth2 + JWT (python-jose)
- Hash de senha: `pbkdf2_sha256` (Passlib)
- Validação: Pydantic v2 (`pydantic-settings` para config)

**Frontend**

- HTML sem framework (foco didático);
- CSS responsivo;
- JavaScript modular (arquivos separados por responsabilidade):
  - `api.js` – comunicação com a API;
  - `session.js` – controle de sessão e menu dinâmico;
  - `animais.js` – mural e listagem de animais;
  - `adocao.js` – fluxo de pedido de adoção;
  - `painel_anunciante.js` – CRUD de animais + pedidos;
  - `painel_admin.js` – gestão de usuários + auditoria;
  - outros arquivos de página (ex.: `auth.js`, etc.).

---

## 🗂 Estrutura do backend

Principais diretórios/arquivos (simplificado):

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py          # Settings (env, JWT, admin default, CORS, DB)
│   │   ├── database.py        # Engine, SessionLocal, Base, get_db
│   │   └── security.py        # hash/verify, JWT, get_current_user, require_role
│   ├── middleware/
│   │   └── security_headers.py
│   ├── models/
│   │   ├── usuario.py
│   │   ├── animal.py
│   │   ├── adocao.py
│   │   └── log_auditoria.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── animal.py
│   │   ├── adocao.py
│   │   └── log.py
│   ├── services/
│   │   ├── usuario_service.py
│   │   ├── animais_service.py
│   │   ├── adocao_service.py
│   │   └── log_service.py
│   └── routes/
│       ├── auth.py
│       ├── animais.py
│       ├── adocoes.py
│       ├── usuarios.py
│       ├── logs.py
│       └── uploads.py         # upload/resize de fotos de animais
└── ...
```

### Configuração (`core/config.py`)

- `DATABASE_URL` – URL do banco (por padrão, `sqlite:///./adote_mais.db`);
- `JWT_SECRET_KEY` e `JWT_ALGORITHM`;
- `ACCESS_TOKEN_EXPIRE_MINUTES`;
- Admin padrão:

  ```py
  ADMIN_DEFAULT_EMAIL = "admin@adotemais.com"
  ADMIN_DEFAULT_PASSWORD = "Admin@123"
  ADMIN_DEFAULT_NAME = "Administrador ADOTE+"
  ```

Valores podem ser sobrescritos via `.env`.

---

## 🎨 Frontend – Páginas e navegação

Servido como arquivos estáticos (ex.: `http://localhost:5500`):

---

## 🚀 Como rodar o projeto

### 1. Backend (API ADOTE+)

Requisitos:

- Python 3.10+
- Virtualenv recomendado

Passos:

```
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
# source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

A API ficará disponível em: `http://localhost:8000`

Documentação automática:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

Na primeira execução:

- As tabelas são criadas automaticamente;
- Se não existir admin com o e-mail padrão, um usuário admin é criado.

### 2. Frontend (arquivos estáticos)

Você pode subir um servidor HTTP simples, por exemplo:

```
cd frontend
python -m http.server 5500
```

Acesse:

- `http://localhost:5500/index.html`

Certifique-se de que o backend (`http://localhost:8000`) esteja rodando para login, adoções, etc.

---

## 🔑 Admin padrão

Configuração inicial (por padrão):

- E-mail: `admin@adotemais.com`
- Senha: `Admin@123`
- Nome: `Administrador ADOTE+`

> Em produção, **sempre** troque esses valores via `.env` e force mudança de senha inicial.

---

## 🔒 Considerações de segurança

- Senhas:
  - Nunca são armazenadas em texto puro, apenas hash (`pbkdf2_sha256`).
- JWT:
  - Assinado com chave configurável em `JWT_SECRET_KEY`;
  - Tempo de expiração configurado em `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Autorização:
  - `require_role(...)` protege rotas sensíveis por tipo de perfil;
  - Cadastro público **não** permite criar administradores.
- CORS:
  - Configurado para permitir o frontend em desenvolvimento (`localhost`).
  - Em produção, recomenda-se restringir a origens específicas (domínio do frontend).
- Uploads de imagem:
  - Tratamento de arquivos limitado a imagens;
  - Conversão/redimensionamento reduz risco de upload de arquivos gigantes e melhora UX.

---

Projeto focado em:

- **Responsividade**;
- **Simplicidade de uso** para comunidade local;
- **Rastreabilidade** via logs de auditoria;
- **Boas práticas básicas de segurança** para um contexto acadêmico.

ADOTE+ busca incentivar uma cultura de adoção responsável e apoio contínuo
a animais abandonados na região.
