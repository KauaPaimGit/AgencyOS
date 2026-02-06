"""
SCRIPT DE EMERGÊNCIA: Criação de Usuário Admin no Banco Remoto
Usa conexão direta via SQLAlchemy para criar admin quando não há acesso ao Shell
"""

import sys
import getpass
from uuid import uuid4
from datetime import datetime

try:
    from sqlalchemy import create_engine, text, inspect
    from sqlalchemy.orm import sessionmaker
    import bcrypt
except ImportError as e:
    print("\n❌ ERRO: Dependências não instaladas!")
    print("\n📦 Execute: pip install sqlalchemy psycopg2-binary bcrypt")
    print(f"\nDetalhes: {e}")
    sys.exit(1)

print("=" * 70)
print("🚨 SCRIPT DE EMERGÊNCIA - CRIAÇÃO DE ADMIN NO BANCO REMOTO")
print("=" * 70)
print()

# ============================================
# 1. SOLICITAR DATABASE_URL
# ============================================
print("📋 Cole a DATABASE_URL do Render (será corrigida automaticamente):")
database_url = input("URL: ").strip()

if not database_url:
    print("\n❌ URL não pode ser vazia!")
    sys.exit(1)

# CRÍTICO: Corrigir postgres:// para postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    print("✅ URL corrigida: postgres:// → postgresql://")

print(f"\n🔗 Conectando em: {database_url[:50]}...")

# ============================================
# 2. TESTAR CONEXÃO
# ============================================
try:
    engine = create_engine(database_url, pool_pre_ping=True)
    
    # Testa a conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        result.fetchone()
    
    print("✅ Conexão estabelecida com sucesso!")
    
except Exception as e:
    print(f"\n❌ ERRO AO CONECTAR NO BANCO:")
    print(f"   {e}")
    print("\n💡 Verifique se:")
    print("   1. A URL está correta")
    print("   2. O banco está acessível")
    print("   3. As credenciais estão corretas")
    sys.exit(1)

# ============================================
# 3. VERIFICAR SE TABELA USERS EXISTE
# ============================================
try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'users' not in tables:
        print("\n⚠️ AVISO: Tabela 'users' não existe no banco!")
        print("💡 Execute primeiro: python main.py (para criar as tabelas)")
        create_table = input("\n❓ Deseja criar a tabela agora? (s/n): ").lower()
        
        if create_table == 's':
            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        id UUID PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        role VARCHAR(50) NOT NULL DEFAULT 'user',
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                """))
                conn.commit()
                print("✅ Tabela 'users' criada com sucesso!")
        else:
            print("\n❌ Cancelado pelo usuário.")
            sys.exit(0)
    else:
        print("✅ Tabela 'users' encontrada!")
    
except Exception as e:
    print(f"\n❌ ERRO ao verificar tabelas: {e}")
    sys.exit(1)

# ============================================
# 4. SOLICITAR DADOS DO ADMIN
# ============================================
print("\n" + "=" * 70)
print("👤 DADOS DO USUÁRIO ADMIN")
print("=" * 70)

username = input("\n📝 Username: ").strip()
if not username:
    print("❌ Username não pode ser vazio!")
    sys.exit(1)

email = input("📧 Email: ").strip()
if not email:
    print("❌ Email não pode ser vazio!")
    sys.exit(1)

password = getpass.getpass("🔒 Senha: ")
if not password:
    print("❌ Senha não pode ser vazia!")
    sys.exit(1)

password_confirm = getpass.getpass("🔒 Confirme a senha: ")
if password != password_confirm:
    print("❌ As senhas não coincidem!")
    sys.exit(1)

# ============================================
# 5. GERAR HASH DA SENHA
# ============================================
print("\n🔐 Gerando hash da senha...")
try:
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print("✅ Hash gerado com sucesso!")
except Exception as e:
    print(f"❌ ERRO ao gerar hash: {e}")
    sys.exit(1)

# ============================================
# 6. VERIFICAR SE USUÁRIO JÁ EXISTE
# ============================================
Session = sessionmaker(bind=engine)
session = Session()

try:
    result = session.execute(
        text("SELECT id, username, email, role FROM users WHERE username = :username OR email = :email"),
        {"username": username, "email": email}
    )
    existing_user = result.fetchone()
    
    if existing_user:
        print(f"\n⚠️ USUÁRIO JÁ EXISTE:")
        print(f"   ID: {existing_user[0]}")
        print(f"   Username: {existing_user[1]}")
        print(f"   Email: {existing_user[2]}")
        print(f"   Role: {existing_user[3]}")
        
        update = input("\n❓ Deseja atualizar a senha deste usuário? (s/n): ").lower()
        
        if update == 's':
            # Atualiza a senha
            session.execute(
                text("""
                    UPDATE users 
                    SET password_hash = :password_hash,
                        role = 'admin',
                        is_active = TRUE,
                        updated_at = :updated_at
                    WHERE username = :username
                """),
                {
                    "password_hash": password_hash,
                    "username": username,
                    "updated_at": datetime.utcnow()
                }
            )
            session.commit()
            
            print("\n✅ SENHA ATUALIZADA COM SUCESSO!")
            print(f"\n🎉 Usuário: {username}")
            print(f"📧 Email: {email}")
            print(f"🎭 Role: admin")
            print("\n✅ Você já pode fazer login no sistema!")
        else:
            print("\n❌ Operação cancelada.")
        
        session.close()
        sys.exit(0)
    
except Exception as e:
    print(f"\n⚠️ Erro ao verificar usuário existente: {e}")
    print("Continuando com a criação...")

# ============================================
# 7. CRIAR NOVO USUÁRIO ADMIN
# ============================================
print("\n🚀 Criando usuário admin...")

try:
    user_id = str(uuid4())
    now = datetime.utcnow()
    
    session.execute(
        text("""
            INSERT INTO users (id, username, email, password_hash, role, is_active, created_at, updated_at)
            VALUES (:id, :username, :email, :password_hash, :role, :is_active, :created_at, :updated_at)
        """),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": "admin",
            "is_active": True,
            "created_at": now,
            "updated_at": now
        }
    )
    
    session.commit()
    
    print("\n" + "=" * 70)
    print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
    print("=" * 70)
    print(f"\n🆔 ID: {user_id}")
    print(f"👤 Username: {username}")
    print(f"📧 Email: {email}")
    print(f"🎭 Role: admin")
    print(f"✅ Status: Ativo")
    print("\n🎉 Você já pode fazer login no sistema!")
    print("=" * 70)
    
except Exception as e:
    session.rollback()
    print(f"\n❌ ERRO AO CRIAR USUÁRIO:")
    print(f"   {e}")
    print("\n💡 Possíveis causas:")
    print("   1. Username ou email já existem")
    print("   2. Falta de permissões no banco")
    print("   3. Erro de sintaxe SQL")
    sys.exit(1)

finally:
    session.close()

print("\n✅ Script finalizado com sucesso!")
