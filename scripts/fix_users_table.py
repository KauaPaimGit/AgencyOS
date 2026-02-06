"""
Script para corrigir/recriar a tabela users
Este script dropa a tabela users existente e recria com o esquema correto
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carrega variáveis de ambiente
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/agency_os"
)

def fix_users_table():
    """
    Recria a tabela users com o esquema correto
    """
    print("=" * 60)
    print("🔧 CORREÇÃO DA TABELA USERS")
    print("=" * 60)
    
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        
        with engine.connect() as conn:
            print("\n⚠️  Esta operação irá DROPAR a tabela users existente!")
            print("   Todos os usuários serão removidos.")
            print("\n❓ Deseja continuar? (s/n): ", end="")
            resposta = input().strip().lower()
            
            if resposta != 's':
                print("\n❌ Operação cancelada.")
                return
            
            print("\n🗑️  Dropando tabela users antiga...")
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.commit()
            print("✅ Tabela antiga removida")
            
            print("\n🔨 Criando nova tabela users...")
            conn.execute(text("""
                CREATE TABLE users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL DEFAULT 'user',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ Tabela criada com sucesso")
            
            print("\n📊 Criando índices...")
            conn.execute(text("CREATE INDEX idx_users_username ON users(username)"))
            conn.execute(text("CREATE INDEX idx_users_email ON users(email)"))
            conn.execute(text("CREATE INDEX idx_users_role ON users(role)"))
            conn.commit()
            print("✅ Índices criados")
            
            print("\n" + "=" * 60)
            print("✅ Tabela users corrigida com sucesso!")
            print("=" * 60)
            print("\n💡 Próximo passo: Execute 'python create_admin.py'")
            
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fix_users_table()
