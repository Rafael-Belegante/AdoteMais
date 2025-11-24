# ADOTE+

Website de adoção de animais de rua, com foco em **ação social permanente**
para amparo aos animais abandonados na região de **Joinville / SC**.

Projeto acadêmico - **SENAI/SC**

---

## 🎯 Objetivo

Desenvolver um website simples, responsivo e de fácil uso pela comunidade,
que engaje pessoas, ONGs e voluntários em uma corrente de adoção responsável
e cuidado com animais em situação de abandono.

Benefícios esperados:

- Engajamento social contínuo em prol dos animais;
- Apoio ao controle de zoonoses;
- Amparo a animais em situações insalubres.

---

## 👥 Perfis de acesso

- **Visitante**
  - Acessa o mural de animais disponíveis (cards).
- **Usuário (Adotante)**
  - Cria conta, faz login;
  - Solicita adoção de animais.
- **ONG / Voluntário**
  - Cadastra e gerencia animais encontrados;
  - Aprova ou nega pedidos de adoção;
  - Lê mensagens da comunidade.
- **Admin**
  - Possui visão global de usuários e dados;
  - Pode listar usuários e apoiar a gestão do sistema.

A modelagem segue:

- Diagrama de Atividade (fluxo de adoção);
- Diagrama de Casos de Uso;
- Diagrama Entidade-Relacionamento (USUARIO, ANIMAL, ADOCAO, MENSAGEM, ONG).

---

## 🏗 Arquitetura

Monorepo simples:

```bash
adote_mais/
├── backend/        # API FastAPI + SQLAlchemy
├── frontend/       # HTML/CSS/JS estáticos
└── README.md
```

### Backend

- **Framework**: FastAPI
- **Banco**: SQLite (simples para desenvolvimento; pode ser trocado para PostgreSQL em produção);
- **ORM**: SQLAlchemy;
- **Auth**: OAuth2 + JWT (python-jose);
- **Hash de senha**: `pbkdf2_sha256` (Passlib).

Entidades principais (de acordo com o MER):

- `Usuario` (com campo `tipo`: `usuario`, `ong`, `admin`);
- `ONG`;
- `Animal`;
- `Adocao`;
- `Mensagem`.

Rotas principais (API REST):

- `POST /auth/register` — cria usuário (tipo **usuario** ou **ong**);
- `POST /auth/login` — autenticação, retorna JWT;
- `GET  /auth/me` — dados do usuário logado;
- `GET  /animais/` — lista animais disponíveis (acesso público);
- `GET  /animais/{id}` — detalhes de um animal;
- `POST /animais/` — cadastra animal (ONG/Admin);
- `POST /adocoes/` — solicita adoção (Usuário/Admin);
- `GET  /adocoes/pendentes` — lista adoções pendentes (ONG/Admin);
- `PUT  /adocoes/{id}/aprovar` — aprova adoção (ONG/Admin);
- `PUT  /adocoes/{id}/negar` — nega adoção (ONG/Admin);
- `POST /mensagens/` — contato da comunidade;
- `GET  /mensagens/` — listagem de mensagens (ONG/Admin);
- `GET  /usuarios/` — lista de usuários (Admin);
- `GET  /usuarios/{id}` — detalhes de um usuário (ONG/Admin).

Segurança:

- Todas as senhas são armazenadas com hash (`pbkdf2_sha256`);
- Uso de JWT com expiração configurável;
- Decorator `require_role(...)` para limitar acesso às rotas por tipo de usuário;
- Cadastro público (`/auth/register`) **não permite criar admin** — apenas `usuario` e `ong`.

### Admin padrão

Ao iniciar a API (`uvicorn app.main:app`), o backend executa uma rotina de inicialização (`init_admin`) que:

1. Abre uma sessão no banco;
2. Verifica se já existe um usuário com o e-mail configurado como admin padrão;
3. Se **não existir**, cria automaticamente um usuário `tipo="admin"` com os dados abaixo.

Valores padrão (podem ser sobrescritos via `.env`):

- `ADMIN_DEFAULT_EMAIL = "admin@adotemais.local"`
- `ADMIN_DEFAULT_PASSWORD = "Admin@123"`
- `ADMIN_DEFAULT_NAME = "Administrador ADOTE+"`

> **Importante:** em ambiente real, altere essas credenciais por variáveis de ambiente
> e troque a senha assim que possível usando uma rotina própria de troca de senha.

Fluxo recomendado na primeira execução:

1. Suba o backend (ver seção “Como rodar”);
2. A rotina de boot criará o admin padrão caso ele ainda não exista;
3. Acesse o frontend, vá na tela de login e entre com:
   - E-mail: `admin@adotemais.local`
   - Senha: `Admin@123`
4. Com esse admin, você pode:
   - Cadastrar novos usuários e ONGs;
   - Gerenciar dados via API.

---

## 🎨 Frontend

- HTML sem framework para facilitar entendimento acadêmico;
- CSS responsivo preparado para uso em celulares e tablets;
- JS simples com `fetch` consumindo a API (CORS liberado para desenvolvimento).

Páginas principais:

- `index.html` — mural de animais e apresentação do projeto;
- `login.html` — login e cadastro de usuários (adotante ou ONG/Voluntário);
- `painel_usuario.html` — base para evoluir a área logada do adotante;
- `painel_ong.html` — painel de ONG/Voluntário:
  - Lista adoções pendentes;
  - Permite aprovar/recusar pedidos;
- `painel_admin.html` — painel do Admin:
  - Lista todos os usuários cadastrados.

Cadastro:

- Na tela de cadastro, o usuário pode escolher o tipo de conta:
  - `Usuário (Adotante)` → `tipo = "usuario"`;
  - `ONG / Voluntário` → `tipo = "ong"`.

---

## 🚀 Como rodar

### 1. Backend (API ADOTE+)

```bash
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

> Na primeira execução, se ainda não houver admin cadastrado,
> o backend criará automaticamente o usuário **admin padrão**.

### 2. Frontend (cliente web)

Como os arquivos são estáticos, você pode servir com o próprio Python:

```bash
cd ../frontend
python -m http.server 5500
```

Acesse no navegador:

- `http://localhost:5500/index.html`

> Certifique-se de que o backend (`http://localhost:8000`) esteja rodando antes
> de usar as funcionalidades que dependem de login.

---

## 🔑 Login inicial (Admin padrão)

1. Certifique-se de que o backend está rodando;
2. Acesse `http://localhost:5500/login.html`;
3. Faça login com:

   - E-mail: `admin@adotemais.local`
   - Senha: `Admin@123`

4. Após logar como admin, você pode:
   - Cadastrar usuários adotantes e ONGs;
   - Acessar o painel de administração (`painel_admin.html`);
   - (Opcional) implementar e usar um endpoint de troca de senha.

---

## 🔒 Observações de segurança

- A chave JWT (`JWT_SECRET_KEY`) está em `app/core/config.py` (classe `Settings`);
  use um valor forte e configure via variáveis de ambiente ou arquivo `.env`;
- Modelo de settings em `backend/.env.example`;
- Hash de senha com `pbkdf2_sha256` via Passlib;
- Cadastro público cria apenas usuários de tipo `usuario` ou `ong`, nunca `admin`;
- Rotas críticas exigem papéis específicos (`require_role("ong", "admin")`, etc.);
- Para ambiente real:
  - Usar HTTPS (proxy reverso com Nginx, por exemplo);
  - Usar banco de dados como PostgreSQL;
  - Restringir CORS para o domínio real do frontend.

---

Projeto focado em **responsividade, simplicidade de uso**
e **engajamento social contínuo** em favor dos animais abandonados
do estado de **Santa Catarina (SC)**.
