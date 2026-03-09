"""Funcoes de busca semantica nos vector stores."""

import logging
import re
from typing import Any

from app.config import get_settings
from app.vectorstore.connection import get_vectorstore

logger = logging.getLogger(__name__)


def search_catalogo(query: str, k: int = 3) -> list[dict[str, Any]]:
    """Busca semantica no catalogo de erros.

    Args:
        query: Texto de busca (codigo de erro, descricao, tag, etc)
        k: Numero maximo de resultados

    Returns:
        Lista de dicts com page_content e metadata de cada resultado
    """
    settings = get_settings()
    vectorstore = get_vectorstore(settings.pgvector_collection_catalogo)
    results = vectorstore.similarity_search(query, k=k)
    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in results
    ]


def search_regras(query: str, k: int = 3) -> list[dict[str, Any]]:
    """Busca semantica nas regras de negocio.

    Args:
        query: Texto de busca (nome de tag, regra, secao, etc)
        k: Numero maximo de resultados

    Returns:
        Lista de dicts com page_content e metadata de cada resultado
    """
    settings = get_settings()
    vectorstore = get_vectorstore(settings.pgvector_collection_regras)
    results = vectorstore.similarity_search(query, k=k)
    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in results
    ]


def search_xmls_autorizados(query: str, k: int = 2) -> list[dict[str, Any]]:
    """Busca semantica nos XMLs autorizados.

    Args:
        query: Texto de busca (CNPJ, descricao servico, tags, etc)
        k: Numero maximo de resultados

    Returns:
        Lista de dicts com page_content e metadata de cada resultado
    """
    settings = get_settings()
    vectorstore = get_vectorstore(settings.pgvector_collection_xmls)
    results = vectorstore.similarity_search(query, k=k)
    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in results
    ]


def search_catalogo_hibrido(query: str, k: int = 3) -> list[dict[str, Any]]:
    """Busca hibrida no catalogo: tenta match exato por codigo_erro, fallback semantico.

    Se a query parece um codigo de erro (ex: E001, E042, L12), busca k=10 resultados
    e promove o resultado com metadata.codigo_erro == query para o topo.
    Caso contrario, usa busca semantica pura.

    Args:
        query: Codigo de erro ou trecho de mensagem
        k: Numero maximo de resultados

    Returns:
        Lista de dicts com page_content e metadata
    """
    settings = get_settings()
    vectorstore = get_vectorstore(settings.pgvector_collection_catalogo)

    # Detectar se query parece um codigo de erro (letras + digitos, curto)
    _RE_CODIGO = re.compile(r"^[A-Za-z]{1,3}[0-9]{1,4}$")
    query_stripped = query.strip()
    is_code_query = bool(_RE_CODIGO.match(query_stripped))

    if is_code_query:
        # Buscar amplo e fazer exact match em Python
        results = vectorstore.similarity_search(query_stripped, k=15)
        codigo_upper = query_stripped.upper()
        exatos = [doc for doc in results if doc.metadata.get("codigo_erro", "").upper() == codigo_upper]
        outros = [doc for doc in results if doc.metadata.get("codigo_erro", "").upper() != codigo_upper]
        ordenados = exatos + outros
    else:
        ordenados = vectorstore.similarity_search(query_stripped, k=k * 3)

    return [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in ordenados[:k]
    ]


def search_xmls_autorizados_com_threshold(
    query: str, k: int = 2, min_relevance: float = 0.35
) -> list[dict[str, Any]]:
    """Busca semantica nos XMLs autorizados com threshold de relevancia.

    Usa similarity_search_with_relevance_scores para filtrar resultados
    abaixo do threshold (scores variam de 0 a 1, maior = mais relevante).

    Args:
        query: Texto de busca
        k: Numero maximo de resultados
        min_relevance: Score minimo de relevancia (0.0-1.0). Abaixo disso = nao relevante.

    Returns:
        Lista de dicts com page_content e metadata. Vazia se nenhum acima do threshold.
    """
    settings = get_settings()
    vectorstore = get_vectorstore(settings.pgvector_collection_xmls)
    results_with_scores = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    filtered = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc, score in results_with_scores
        if score >= min_relevance
    ]
    return filtered
