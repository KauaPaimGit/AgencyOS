# 🔐 Sistema de Autenticação - AgencyOS

## Visão Geral

O AgencyOS agora possui um sistema completo de autenticação que protege todos os dados do sistema. Apenas usuários autenticados podem acessar o dashboard e as funcionalidades.

## Arquitetura

### Backend (FastAPI)

- **Modelo User** ([app/models.py](app/models.py)): Tabela de usuários com campos id, username, email, password_hash, role, is_active, created_at, updated_at e last_login
- **Módulo de Autenticação** ([app/auth.py](app/auth.py)): Funções para hash de senhas (bcrypt), verificação de credenciais e autenticação
- **Endpoint /login** ([main.py](main.py)): API REST para autenticação de usuários

### Frontend (Streamlit)

- **Verificação de Sessão** ([frontend/app.py](frontend/app.py)): Sistema que bloqueia acesso não autenticado
- **Tela de Login**: Interface amigável para entrada de credenciais
- **Session State**: Mantém estado de autenticação durante a sessão
- **Botão de Logout**: Permite sair do sistema com segurança

### Segurança

- **Hash bcrypt**: Senhas nunca armazenadas em texto plano
- **Verificação de senha**: Comparação segura usando passlib
- **Role-based access**: Sistema preparado para diferentes perfis (admin, user, manager)
- **Token placeholder**: Preparado para implementação JWT futura

## 📦 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

A nova dependência adicionada:
- `passlib[bcrypt]` - Para hash e verificação segura de senhas

### 2. Criar Tabela no Banco de Dados

Existem duas opções:

**Opção A: Migração Manual (SQL)**
```bash
psql -U postgres -d agency_os -f migrations/003_add_users_table.sql
```

**Opção B: Automático via FastAPI**
```bash
# O FastAPI cria automaticamente ao iniciar
python -m uvicorn main:app --reload
```

O SQLAlchemy detecta o novo modelo `User` e cria a tabela automaticamente.

### 3. Criar Usuário Administrador

Execute o script de seed para criar seu primeiro usuário:

```bash
python create_admin.py
```

**Credenciais padrão criadas:**
- **Usuário:** `admin`
- **Senha:** `senha123`
- **Role:** `admin`
- **Email:** `admin@agencyos.com`

⚠️ **IMPORTANTE**: Altere a senha após o primeiro login!

## 🚀 Como Usar

### 1. Iniciar o Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Iniciar o Frontend

```bash
cd frontend
streamlit run app.py
```

### 3. Fazer Login

1. Abra o navegador em `http://localhost:8501`
2. Digite o usuário: `admin`
3. Digite a senha: `senha123`
4. Clique em "🚀 Entrar"

✅ Após autenticação, você terá acesso completo ao sistema!

### 4. Fazer Logout

- Clique no botão "🚪 Sair" na sidebar a qualquer momento
- Isso limpa a sessão e redireciona para a tela de login

## 🔑 Gerenciamento de Usuários

### Criar Novos Usuários

Atualmente, você pode criar usuários manualmente via SQL ou modificar o script `create_admin.py`:

```python
# Exemplo: Criar usuário regular
new_user = User(
    username="joao",
    email="joao@agencyos.com",
    password_hash=get_password_hash("senha_segura"),
    role="user",
    is_active=True
)
db.add(new_user)
db.commit()
```

### Papéis (Roles)

O sistema suporta diferentes perfis de usuário:

- **admin**: Acesso total ao sistema
- **manager**: Gerente de projetos (preparado para futuras restrições)
- **user**: Usuário padrão (preparado para futuras restrições)

### Desativar Usuário

```sql
UPDATE users SET is_active = FALSE WHERE username = 'nome_usuario';
```

## 🔒 Segurança Implementada

### ✅ O que está protegido

1. **Senhas com Hash bcrypt**: Impossível recuperar senha original
2. **Validação de credenciais**: Verificação segura no backend
3. **Session State**: Estado de autenticação mantido no Streamlit
4. **API protegida**: Endpoint /login com validação robusta
5. **Feedback de erros**: Mensagens claras sem expor informações sensíveis

### 🔄 Próximos Passos (Melhorias Futuras)

- [ ] **JWT Real**: Substituir "fake-jwt-token" por JWT assinado (PyJWT)
- [ ] **Middleware de Autenticação**: Proteger todos os endpoints da API
- [ ] **Expiração de Sessão**: Timeout automático após inatividade
- [ ] **Recuperação de Senha**: Fluxo de reset via email
- [ ] **Registro de Usuários**: Interface para criar novos usuários
- [ ] **Logs de Auditoria**: Registro de login/logout e ações
- [ ] **2FA (Two-Factor Auth)**: Camada extra de segurança

## 📝 Estrutura de Arquivos

```
SOG/
├── app/
│   ├── models.py         # ✅ Modelo User adicionado
│   ├── auth.py           # ✅ Novo: Funções de autenticação
│   ├── database.py
│   └── ...
├── frontend/
│   └── app.py            # ✅ Refatorado com login
├── migrations/
│   └── 003_add_users_table.sql  # ✅ Nova migração
├── create_admin.py       # ✅ Novo: Script de seed
├── main.py               # ✅ Endpoint /login adicionado
├── requirements.txt      # ✅ passlib[bcrypt] adicionado
└── AUTH_README.md        # 📄 Este arquivo
```

## 🐛 Troubleshooting

### Erro: "Credenciais inválidas"
- Verifique se você executou `python create_admin.py`
- Confirme que está usando `admin` / `senha123`
- Verifique se o banco de dados está online

### Erro: "API não está respondendo"
- Verifique se o uvicorn está rodando em `localhost:8000`
- Teste acessar `http://localhost:8000/` no navegador
- Verifique logs do console do FastAPI

### Erro: "Tabela users não existe"
- Execute a migração: `python create_admin.py` (cria automaticamente)
- Ou execute manualmente: `psql -f migrations/003_add_users_table.sql`

### Preciso criar novo usuário admin?
```bash
python create_admin.py
# Responda 's' quando perguntado se deseja atualizar a senha
```

## 📚 Documentação Técnica

### Endpoint de Login

**POST** `/login`

**Request:**
```json
{
  "username": "admin",
  "password": "senha123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login realizado com sucesso",
  "user_role": "admin",
  "username": "admin",
  "token": "fake-jwt-token-<uuid>"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Credenciais inválidas. Verifique seu usuário e senha."
}
```

### Modelo User

```python
class User(Base):
    id: UUID              # Chave primária
    username: str         # Único, indexado
    email: str            # Único, indexado
    password_hash: str    # Hash bcrypt
    role: str             # 'admin', 'user', 'manager'
    is_active: bool       # True/False
    created_at: datetime
    updated_at: datetime
    last_login: datetime  # Atualizado a cada login
```

---

**🎉 Sistema de Autenticação Implementado com Sucesso!**

Desenvolvido para o AgencyOS v1.2 - Vyron System
