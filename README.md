# ADOTE+

Website de adoção de animais de rua, com foco em **ação social permanente**
para amparo aos animais abandonados na região de **Joinville / SC**.

Projeto acadêmico - **SENAI/SC - Joinville Sul**

## 🎯 Objetivo

Desenvolver um website simples, responsivo e de fácil uso pela comunidade,
que engaje pessoas, ONGs e voluntários em uma corrente de adoção responsável
e cuidado com animais em situação de abandono.

Benefícios esperados:
- Engajamento social contínuo em prol dos animais;
- Apoio ao controle de zoonoses;
- Amparo a animais em situações insalubres.

## 👥 Perfis de acesso

- **Visitante**
  - Acessa o mural de animais disponíveis (cards).
- **Usuário (adotante)**
  - Cria conta, faz login;
  - Solicita adoção de animais.
- **ONG / Voluntário**
  - Cadastra e gerencia animais encontrados;
  - Aprova ou nega pedidos de adoção;
  - Lê mensagens da comunidade.
- **Admin**
  - Possui visão global de usuários e dados (CRUD de usuários via API).

A modelagem segue:
- Diagrama de Atividade (fluxo de adoção);
- Diagrama de Casos de Uso;
- Diagrama Entidade-Relacionamento (USUARIO, ANIMAL, ADOCAO, MENSAGEM, ONG).

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
- **Banco**: SQLite (simples para desenvolvimento; pode ser trocado para PostgreSQL)
- **ORM**: SQLAlchemy
- **Auth**: OAuth2 + JWT (python-jose)
- **Hash de senha**: bcrypt (passlib)

Entidades principais (de acordo com o MER):
- `Usuario` (com campo `tipo`: `usuario`, `ong`, `admin`)
- `ONG`
- `Animal`
- `Adocao`
- `Mensagem`

Rotas principais:
- `POST /auth/register` — cria usuário
- `POST /auth/login` — retorna JWT
- `GET /animais/` — lista animais disponíveis (visitante)
- `POST /animais/` — cadastra animal (ONG/Admin)
- `POST /adocoes/` — solicita adoção (Usuário)
- `PUT /adocoes/{id}/aprovar` — aprova adoção (ONG/Admin)
- `PUT /adocoes/{id}/negar` — nega adoção (ONG/Admin)
- `POST /mensagens/` — contato da comunidade
- `GET /mensagens/` — listagem para ONG/Admin

Segurança:
- Todas as senhas são armazenadas com hash (bcrypt);
- Uso de JWT com expiração configurável;
- Decorator `require_role` para limitar acesso por tipo de usuário.

### Frontend

- HTML sem framework para facilitar entendimento acadêmico;
- CSS responsivo preparado para uso em celulares e tablets;
- JS simples com `fetch` consumindo a API (CORS liberado no backend).

Páginas:
- `index.html` — mural de animais e apresentação do projeto;
- `login.html` — login e cadastro de usuário adotante;
- `painel_usuario.html` — base para evoluir área logada;
- (painéis de ONG/Admin podem ser adicionados como melhoria futura).

## 🚀 Como rodar

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

A API ficará disponível em: `http://localhost:8000`

Documentação automática:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### 2. Frontend

Como os arquivos são estáticos, você pode:

**Opção simples (Python):**
```bash
cd ../frontend
python -m http.server 5500
```

Acesse: `http://localhost:5500/index.html`

> Certifique-se de que o backend (`localhost:8000`) esteja rodando.

## 🔒 Observações de segurança

- A chave JWT (`JWT_SECRET_KEY`) está em `app/core/config.py`.  
  Em produção, configure via variáveis de ambiente ou arquivo `.env`.
- Para ambiente real, usar HTTPS e banco de dados robusto (PostgreSQL).
- Aplicar controle mais refinado de criação de usuários `ong` e `admin`
  (por exemplo, somente admin pode promovê-los).

## 📌 Possíveis melhorias

- Painel completo para ONG (lista de adoções pendentes e aprovação via interface web);
- Dashboard para Admin;
- Upload de imagens em vez de `foto_url`;
- Notificação por e-mail para aprovados/negados;
- Filtro de animais por porte, espécie e bairro;
- Internacionalização (pt-BR / en-US).

---

Projeto focado em **responsividade, simplicidade de uso** e **engajamento social**
em favor dos animais abandonados do estado de SC.


## ⚙️ Pronto para produção (base)

- JWT com expiração configurável e chave externa via `.env`;
- Cabeçalhos de segurança básicos (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection);
- Papéis separados: `usuario`, `ong`, `admin` com proteção de rotas no backend;
- Cadastro público sempre cria usuários do tipo `usuario` (evita criação de admin/ong via formulário);
- Frontend responsivo preparado para mobile e tablets;
- Arquivo `.env.example` incluído para facilitar configuração em servidores.

Em ambiente real, recomenda-se:

- Executar o backend com `uvicorn` ou `gunicorn` por trás de um proxy reverso (Nginx);
- Utilizar banco como PostgreSQL em vez de SQLite;
- Restringir o CORS para o domínio real do frontend (ajustando `BACKEND_CORS_ORIGINS`).
