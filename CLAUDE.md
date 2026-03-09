# NFSe Betha Diagnostico Agent

## Projeto
Agente de IA para diagnostico de rejeicoes NFSe padrao Betha (codigo 2945).

## Stack
- Python 3.11, LangChain v1 (>=1.2), LangGraph v1 (>=1.0), FastAPI
- PostgreSQL + PGVector (PGVectorStore via PGEngine + asyncpg), OpenAI GPT-4o-mini
- Docker para deploy

## APIs Principais
- `from langchain.agents import create_agent` (NAO usar create_react_agent - depreciado)
- `from langchain.tools import tool` (decorator para tools)
- `from langchain.agents.structured_output import ToolStrategy`
- `from langchain_postgres import PGEngine, PGVectorStore` (NAO usar PGVector - depreciado)
- NAO usar LangServe (descontinuado) - usar FastAPI diretamente

## Estrutura
- app/ - Codigo principal (config, main, agent/, tools/, vectorstore/)
- data/ - Dados (catalogo 51 erros, regras negocio, XMLs autorizados)
- scripts/ - Ingestao e teste manual
- tests/ - Testes pytest
- docs/ - Documentacao de referencia

## Banco de Dados
- PostgreSQL com PGVector, banco: ai_database
- PGVectorStore cria tabelas proprias: catalogo_erros, regras_negocio, xmls_autorizados
- Schema: id (UUID), content (TEXT), embedding (vector(1536)), cmetadata (JSONB)
- Connection string: postgresql+asyncpg:// (via pydantic-settings .env)

## VectorStore
- connection.py: PGEngine singleton com asyncpg, get_vectorstore(), init_vectorstore_table()
- ingest.py: Pre-processamento em texto descritivo, sanitizacao LGPD, batch insert
- retriever.py: search_catalogo(), search_regras(), search_xmls_autorizados()

## Status de Implementacao
- Prompt 1: COMPLETO (estrutura, configs, esqueletos)
- Prompt 2: COMPLETO (vectorstore, ingestao, retrievers, testes)
- Prompt 3: Pendente (implementar tools do agente)
- Prompt 4: Pendente (implementar agent factory, API completa)
