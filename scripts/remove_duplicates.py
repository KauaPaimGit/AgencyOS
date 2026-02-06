"""
Script para Remover Projetos Duplicados

Remove projetos com mesmo nome e cliente, mantendo apenas o mais recente
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ Erro: DATABASE_URL não encontrada no arquivo .env")
    exit(1)

# Cria engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("=" * 60)
print("🔄 LIMPEZA: Removendo Projetos Duplicados")
print("=" * 60)

try:
    # Busca projetos duplicados (mesmo nome e cliente_id)
    query = text("""
        SELECT 
            name, 
            client_id, 
            COUNT(*) as total,
            STRING_AGG(id::text, ', ') as ids
        FROM projects
        GROUP BY name, client_id
        HAVING COUNT(*) > 1
    """)
    
    duplicates = session.execute(query).fetchall()
    
    if not duplicates:
        print("✅ Nenhum projeto duplicado encontrado!")
        session.close()
        exit(0)
    
    print(f"📊 {len(duplicates)} grupo(s) de projetos duplicados encontrados\n")
    
    total_removed = 0
    
    for dup in duplicates:
        name, client_id, total, ids_str = dup
        ids = ids_str.split(', ')
        
        print(f"🔍 Projeto: '{name}' | Cliente ID: {client_id}")
        print(f"   Total de duplicatas: {total}")
        
        # Busca todos os projetos duplicados ordenados por data de criação (mais recente primeiro)
        projects_query = text("""
            SELECT id, created_at
            FROM projects
            WHERE name = :name AND client_id = :client_id
            ORDER BY created_at DESC
        """)
        
        projects = session.execute(
            projects_query, 
            {"name": name, "client_id": client_id}
        ).fetchall()
        
        # Mantém o primeiro (mais recente), remove os outros
        keep_id = projects[0][0]
        remove_ids = [p[0] for p in projects[1:]]
        
        print(f"   ✅ Mantendo: {keep_id}")
        print(f"   🗑️  Removendo: {len(remove_ids)} duplicata(s)")
        
        # Remove as duplicatas
        for remove_id in remove_ids:
            session.execute(
                text("DELETE FROM projects WHERE id = :id"),
                {"id": remove_id}
            )
            total_removed += 1
        
        print()
    
    # Commit das alterações
    session.commit()
    
    print("=" * 60)
    print(f"✅ Limpeza concluída com sucesso!")
    print(f"🗑️  {total_removed} projeto(s) duplicado(s) removido(s)")
    print("=" * 60)
    
except Exception as e:
    session.rollback()
    print(f"\n❌ Erro durante a limpeza: {e}")
    print("\n⚠️ Rollback realizado - nenhuma alteração foi aplicada")
    exit(1)
finally:
    session.close()
