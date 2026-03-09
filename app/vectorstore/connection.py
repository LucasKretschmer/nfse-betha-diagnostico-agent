"""Conexao com PostgreSQL e PGVectorStore.

Usa PGEngine (langchain-postgres) com driver asyncpg para conexao.
O PGEngine cria internamente um event loop em thread separada,
permitindo chamadas sincronas via .create_sync() e .init_vectorstore_table().

NOTA: O PGVectorStore cria suas proprias tabelas com schema:
  - id (UUID), content (TEXT), embedding (vector), cmetadata (JSONB)
  Essas tabelas sao DIFERENTES das tabelas pre-existentes no banco.
  O LangChain gerencia completamente o ciclo de vida dessas tabelas.
"""

import logging

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore

from app.config import get_settings

logger = logging.getLogger(__name__)

VECTOR_SIZE = 1536  # text-embedding-3-small dimension

_engine: PGEngine | None = None


def get_embeddings() -> OpenAIEmbeddings:
    """Retorna instancia de OpenAIEmbeddings configurada.

    Returns:
        OpenAIEmbeddings com modelo text-embedding-3-small (1536 dims)
    """
    settings = get_settings()
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        openai_api_key=settings.openai_api_key,
    )


def get_engine() -> PGEngine:
    """Retorna instancia singleton de PGEngine.

    Usa driver asyncpg conforme requerido pelo PGEngine.

    Returns:
        PGEngine conectado ao PostgreSQL
    """
    global _engine
    if _engine is None:
        settings = get_settings()
        connection_string = (
            f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        _engine = PGEngine.from_connection_string(url=connection_string)
        logger.info(
            "PGEngine criado para %s:%s/%s",
            settings.postgres_host,
            settings.postgres_port,
            settings.postgres_db,
        )
    return _engine


def init_vectorstore_table(table_name: str) -> None:
    """Inicializa tabela de vectorstore se nao existir.

    Cria tabela com schema padrao do LangChain:
    id (UUID), content (TEXT), embedding (vector(1536)), cmetadata (JSONB)

    Args:
        table_name: Nome da tabela
    """
    engine = get_engine()
    try:
        engine.init_vectorstore_table(
            table_name=table_name,
            vector_size=VECTOR_SIZE,
        )
        logger.info("Tabela '%s' inicializada", table_name)
    except Exception as e:
        if "already exists" in str(e).lower():
            logger.info("Tabela '%s' ja existe, pulando criacao", table_name)
        else:
            raise


def get_vectorstore(collection_name: str) -> PGVectorStore:
    """Retorna instancia de PGVectorStore para uma collection.

    Args:
        collection_name: Nome da tabela/collection

    Returns:
        PGVectorStore configurado e conectado
    """
    engine = get_engine()
    embeddings = get_embeddings()
    return PGVectorStore.create_sync(
        engine=engine,
        table_name=collection_name,
        embedding_service=embeddings,
    )
