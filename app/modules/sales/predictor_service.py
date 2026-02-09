"""
Market Predictor Service v1.2.1
================================
Processa dados de CompetitorIntel para gerar:
  1. Viability Index (0–100)  — índice de viabilidade do nicho
  2. Recomendação Estratégica — frase de conselho automatizada

Algoritmo cruza market_sentiment, traffic_tier e ads_status
usando pesos calibrados para o mercado brasileiro de agências.

Autor: Vyron System Engine
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models

log = logging.getLogger("vyron.predictor")


# ──────────────────────────────────────────────────────────
# CONSTANTES DE PESO PARA O ALGORITMO
# ──────────────────────────────────────────────────────────

_TRAFFIC_SCORES = {
    "low": 85,        # pouca concorrência → oportunidade
    "medium": 60,
    "high": 35,
    "very_high": 15,  # mercado saturado
}

_ADS_SCORES = {
    "Nenhum detectado": 90,           # ninguém investindo → brecha
    "Google Ads": 50,
    "Meta Ads": 55,
    "LinkedIn Ads": 60,
    "TikTok Ads": 65,
    "Google Ads, Meta Ads": 25,       # investimento pesado → difícil
}

# Pesos relativos de cada fator
_W_SENTIMENT = 0.30
_W_TRAFFIC = 0.35
_W_ADS = 0.35


# ──────────────────────────────────────────────────────────
# DATACLASS DE RESULTADO
# ──────────────────────────────────────────────────────────

@dataclass
class PredictionResult:
    """Resultado da predição de viabilidade de mercado."""
    viability_index: int           # 0–100
    sentiment_score: float         # -1.0 a 1.0 (média)
    traffic_tier: str              # tier predominante
    ads_status: str                # plataforma predominante
    recommendation: str            # frase de conselho
    risk_level: str                # low, medium, high
    competitors_analyzed: int      # quantidade de intels processadas
    breakdown: dict                # detalhamento dos sub-scores


# ──────────────────────────────────────────────────────────
# SERVIÇO PRINCIPAL
# ──────────────────────────────────────────────────────────

class MarketPredictorService:
    """
    Serviço de predição de mercado baseado em CompetitorIntel.

    Recebe um lead_id, busca todos os CompetitorIntel associados,
    cruza os dados e retorna um PredictionResult com o índice de
    viabilidade e a recomendação estratégica.
    """

    @staticmethod
    def predict(db: Session, lead_id) -> PredictionResult:
        """
        Gera predição de viabilidade para o nicho de um lead.

        Args:
            db: Sessão SQLAlchemy.
            lead_id: UUID do lead (LeadDiscovery).

        Returns:
            PredictionResult com índice, recomendação e breakdown.

        Raises:
            ValueError: se o lead não existir ou não tiver intels.
        """
        lead = (
            db.query(models.LeadDiscovery)
            .filter(models.LeadDiscovery.id == lead_id)
            .first()
        )
        if not lead:
            raise ValueError(f"Lead {lead_id} não encontrado.")

        intels: List[models.CompetitorIntel] = (
            db.query(models.CompetitorIntel)
            .filter(models.CompetitorIntel.lead_id == lead_id)
            .all()
        )
        if not intels:
            raise ValueError(
                f"Nenhuma análise competitiva encontrada para o lead '{lead.name}'. "
                "Execute o Spy Module primeiro."
            )

        return MarketPredictorService._calculate(intels)

    @staticmethod
    def predict_by_query(db: Session, source_query: str) -> PredictionResult:
        """
        Gera predição agregada para todos os leads de uma query.

        Útil para avaliar o nicho inteiro (ex: 'pizzaria in Passos, MG').
        """
        leads = (
            db.query(models.LeadDiscovery)
            .filter(models.LeadDiscovery.source_query == source_query)
            .all()
        )
        if not leads:
            raise ValueError(f"Nenhum lead encontrado para a query '{source_query}'.")

        lead_ids = [l.id for l in leads]
        intels: List[models.CompetitorIntel] = (
            db.query(models.CompetitorIntel)
            .filter(models.CompetitorIntel.lead_id.in_(lead_ids))
            .all()
        )
        if not intels:
            raise ValueError(
                f"Nenhuma análise competitiva para a query '{source_query}'. "
                "Execute o Spy Module nos leads primeiro."
            )

        return MarketPredictorService._calculate(intels)

    # ──────────────────────────────────────────────────────
    # CORE DO ALGORITMO
    # ──────────────────────────────────────────────────────

    @staticmethod
    def _calculate(intels: List[models.CompetitorIntel]) -> PredictionResult:
        """Calcula o Viability Index a partir de uma lista de CompetitorIntel."""

        # 1. Agrega sentimento
        sentiments = [
            float(i.market_sentiment)
            for i in intels
            if i.market_sentiment is not None
        ]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

        # Normaliza sentiment de (-1,1) → (0,100)
        sentiment_score = (avg_sentiment + 1.0) / 2.0 * 100.0

        # 2. Agrega traffic tier (moda — tier mais frequente)
        tier_counts: dict[str, int] = {}
        for i in intels:
            t = i.estimated_traffic_tier or "medium"
            tier_counts[t] = tier_counts.get(t, 0) + 1
        dominant_tier = max(tier_counts, key=tier_counts.get)  # type: ignore
        traffic_score = _TRAFFIC_SCORES.get(dominant_tier, 50)

        # 3. Agrega ads status (moda)
        ads_counts: dict[str, int] = {}
        for i in intels:
            a = i.ads_platform or "Nenhum detectado"
            ads_counts[a] = ads_counts.get(a, 0) + 1
        dominant_ads = max(ads_counts, key=ads_counts.get)  # type: ignore
        ads_score = _ADS_SCORES.get(dominant_ads, 50)

        # 4. Calcula índice ponderado
        raw_index = (
            sentiment_score * _W_SENTIMENT
            + traffic_score * _W_TRAFFIC
            + ads_score * _W_ADS
        )
        viability_index = max(0, min(100, int(round(raw_index))))

        # 5. Classifica risco
        if viability_index >= 70:
            risk_level = "low"
        elif viability_index >= 40:
            risk_level = "medium"
        else:
            risk_level = "high"

        # 6. Gera recomendação estratégica
        recommendation = MarketPredictorService._generate_recommendation(
            viability_index, dominant_tier, dominant_ads, avg_sentiment, risk_level
        )

        return PredictionResult(
            viability_index=viability_index,
            sentiment_score=round(avg_sentiment, 2),
            traffic_tier=dominant_tier,
            ads_status=dominant_ads,
            recommendation=recommendation,
            risk_level=risk_level,
            competitors_analyzed=len(intels),
            breakdown={
                "sentiment_raw": round(avg_sentiment, 3),
                "sentiment_normalized": round(sentiment_score, 1),
                "traffic_score": traffic_score,
                "ads_score": ads_score,
                "weights": {
                    "sentiment": _W_SENTIMENT,
                    "traffic": _W_TRAFFIC,
                    "ads": _W_ADS,
                },
            },
        )

    # ──────────────────────────────────────────────────────
    # GERADOR DE RECOMENDAÇÕES
    # ──────────────────────────────────────────────────────

    @staticmethod
    def _generate_recommendation(
        index: int,
        traffic: str,
        ads: str,
        sentiment: float,
        risk: str,
    ) -> str:
        """Gera frase de conselho estratégico baseada nos indicadores."""

        parts: list[str] = []

        # Viabilidade geral
        if index >= 75:
            parts.append(
                "Oportunidade alta: mercado com espaço significativo para entrada."
            )
        elif index >= 55:
            parts.append(
                "Oportunidade moderada: nicho competitivo, mas com brechas exploráveis."
            )
        elif index >= 35:
            parts.append(
                "Nicho desafiador: concorrência relevante, exige diferenciação clara."
            )
        else:
            parts.append(
                "Nicho saturado: barreira de entrada alta, foque em sub-nichos."
            )

        # Ads insights
        if ads == "Nenhum detectado":
            parts.append(
                "Baixa concorrência em Ads — oportunidade de dominar o tráfego pago."
            )
        elif ads == "Google Ads, Meta Ads":
            parts.append(
                "Concorrentes investem pesado em Ads (Google + Meta) — "
                "considere estratégia de branding orgânico ou canais alternativos."
            )
        elif "Google" in ads:
            parts.append(
                "Presença ativa em Google Ads — avalie Meta Ads ou TikTok como alternativa."
            )
        elif "Meta" in ads:
            parts.append(
                "Presença ativa em Meta Ads — Google Ads pode ser canal menos disputado."
            )
        else:
            parts.append(f"Concorrência em {ads} — explore canais não explorados.")

        # Traffic insights
        if traffic in ("high", "very_high"):
            parts.append(
                "Tráfego alto indica marcas consolidadas — "
                "foque em diferenciação de branding e propostas de valor únicas."
            )
        elif traffic == "low":
            parts.append(
                "Tráfego baixo no nicho — possível brecha para captura rápida de market share."
            )

        # Sentimento
        if sentiment < -0.1:
            parts.append(
                "Sentimento de mercado negativo pode indicar insatisfação dos consumidores — "
                "oportunidade para oferecer experiência superior."
            )
        elif sentiment > 0.6:
            parts.append(
                "Sentimento positivo alto — mercado receptivo. "
                "Ideal para campanhas de awareness e conversão direta."
            )

        return " ".join(parts)
