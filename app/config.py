"""Configuracao da aplicacao via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuracoes da aplicacao, carregadas de variaveis de ambiente / .env."""

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # PostgreSQL
    postgres_host: str = "host.docker.internal"
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str = "ai_database"

    # PGVector collections
    pgvector_collection_catalogo: str = "catalogo_erros"
    pgvector_collection_regras: str = "regras_negocio"
    pgvector_collection_xmls: str = "xmls_autorizados"

    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "info"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def postgres_connection_string(self) -> str:
        """Retorna connection string para psycopg."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Singleton de Settings com cache."""
    return Settings()
