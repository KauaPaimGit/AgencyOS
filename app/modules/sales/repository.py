"""
Sales Repository — Persistência do módulo Growth & Sales
=========================================================
Funções de acesso a dados que não pertencem diretamente ao router.
"""

from __future__ import annotations

import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app import models

log = logging.getLogger("vyron.sales.repository")


def save_discovery_batch(
    db: Session,
    businesses: List[Dict[str, Any]],
    source_query: str,
) -> int:
    """
    Persiste um lote de leads descobertos pelo Lead Hunter.

    Realiza upsert por ``place_id``:
      - Se o lead já existe (mesmo ``place_id``), ignora.
      - Se é novo, insere.

    Para leads sem ``place_id``, gera uma chave derivada de nome+endereço
    para evitar duplicatas óbvias.

    Args:
        db: sessão SQLAlchemy (sync)
        businesses: lista de dicts vindos de ``search_business()``
        source_query: string de busca original (ex.: "pizzaria in Passos, MG")

    Returns:
        Quantidade de registros efetivamente inseridos.
    """
    if not businesses:
        return 0

    rows: list[dict] = []
    for biz in businesses:
        place_id = biz.get("place_id")
        if not place_id:
            # chave derivada para dedup
            name = (biz.get("name") or "").strip().lower()
            addr = (biz.get("address") or "").strip().lower()
            place_id = f"derived:{name}|{addr}" if name else None

        rating_raw = biz.get("rating")
        rating_val = None
        if rating_raw is not None:
            try:
                rating_val = Decimal(str(rating_raw))
            except (InvalidOperation, ValueError):
                rating_val = None

        rows.append(
            {
                "id": uuid4(),
                "name": (biz.get("name") or "Sem nome")[:255],
                "address": (biz.get("address") or None),
                "phone": (biz.get("phone") or None),
                "rating": rating_val,
                "source_query": source_query[:255],
                "place_id": place_id,
                "discovered_at": datetime.utcnow(),
            }
        )

    if not rows:
        return 0

    stmt = pg_insert(models.LeadDiscovery).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["place_id"])

    result = db.execute(stmt)
    db.commit()

    inserted = result.rowcount if result.rowcount else 0  # type: ignore[union-attr]
    log.info("LeadDiscovery batch: %d/%d inseridos (query=%s)", inserted, len(rows), source_query)
    return inserted
