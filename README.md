# NFSe Betha Diagnostico Agent

Agente de IA para diagnostico de rejeicoes de NFSe padrao Betha (codigo 2945).

Recebe um XML rejeitado + mensagem de erro e retorna diagnostico estruturado com
causa raiz, TAGs com problema e passos de correcao.

## Stack

- **Python 3.11**, **LangChain v1** (create_agent), **LangGraph v1**
- **FastAPI** - API REST
- **PostgreSQL + PGVector** - Vector store
- **OpenAI GPT-4o-mini** - LLM; **text-embedding-3-small** - Embeddings
- **Docker** - Deploy via docker-compose

## Arquitetura

O agente usa `create_agent` (LangChain v1) com 4 tools especializadas:

1. `validar_xml_contra_template` - detecta padrao Betha/Nacional, TAGs faltantes
2. `buscar_catalogo_erros` - busca hibrida (exact + semantica) em 51 erros catalogados
3. `consultar_regra_negocio` - regras de preenchimento das TAGs
4. `buscar_xml_autorizado_similar` - XMLs de referencia com score threshold

Resposta estruturada via `ToolStrategy(DiagnosticoResponse)`.

## Setup Local

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar .env

```bash
cp .env.example .env
# Preencher: OPENAI_API_KEY, POSTGRES_USER, POSTGRES_PASSWORD
```

### 3. Subir PostgreSQL

```bash
docker-compose up postgres -d
```

### 4. Ingerir dados

```bash
python scripts/ingest_data.py --all
# 51 erros + 38 regras + 1149 XMLs = 1238 documentos
```

### 5. Iniciar API

```bash
uvicorn app.main:app --reload
# Docs: http://localhost:8000/docs
```

## Deploy Docker

```bash
cp .env.example .env
# Editar .env
docker-compose up --build -d
docker-compose exec api python scripts/ingest_data.py --all
```

## API

### POST /diagnostico

**Request:**
```json
{
  "xml": "<DPS versao=\"1.0\">...</DPS>",
  "erro": {
    "codigo": "E001",
    "mensagem": "E001: cvc-complex-type.2.4.b: O conteudo do elemento cServ nao completo."
  }
}
```

**Response:**
```json
{
  "status": "DIAGNOSTICADO",
  "tags_com_problema": [{"tag": "cTribNac", "valor_enviado": "", "valor_correto": "140101", "explicacao": "..."}],
  "solucao": {"resumo": "...", "passos": ["..."], "xml_corrigido": "..."},
  "metadata": {"classificacao": "SOFTWARE", "confianca": "ALTA", "erro_catalogado": true},
  "tempo_processamento_ms": 8432.5
}
```

- `status`: DIAGNOSTICADO | INCONCLUSIVO | FORA_DE_ESCOPO
- `classificacao`: CLIENTE | SOFTWARE | PREFEITURA | INDETERMINADO
- `confianca`: ALTA | MEDIA | BAIXA

### GET /health

```json
{"status": "ok", "agent_ready": true}
```

## Testes

```bash
# Testes unitarios (mock, sem LLM/banco)
pytest tests/test_api.py -v

# Todos os testes
pytest tests/ -v

# Teste com agente real (requer .env configurado)
python scripts/test_agent.py --direto
python scripts/test_agent.py --api
```

## Estrutura

```
app/
  agent/
    factory.py      # create_diagnostico_agent()
    prompts.py      # SYSTEM_PROMPT Betha 2945
    schemas.py      # DiagnosticoRequest, DiagnosticoResponse
  tools/            # 4 tools do agente
  vectorstore/      # PGEngine, ingestao, retrievers
  config.py
  main.py           # FastAPI com lifespan
data/
  catalogo_enriquecido.json   # 51 erros
  regras_negocio.md           # regras de preenchimento
  template_betha.xml          # template DPS
  xmls_autorizados/           # 1149 XMLs sanitizados
scripts/
  ingest_data.py    # --all | --catalogo | --regras | --xmls | --reindex-xmls
  test_tools.py     # testes das tools
  test_agent.py     # testes do agente
docs/
  validacao_fase3.md
```

## Erros mais comuns

| Codigo | Frequencia | Causa |
|--------|-----------|-------|
| E001 | 53% | cTribNac ausente ou formato incorreto (deve ter 6 digitos) |
| E042 | 28.6% | pAliq zerado em notas tributaveis |
| L12 | ~1% | Bloqueio especifico do municipio |

## LGPD

XMLs autorizados foram sanitizados: CNPJ anonimizado, razao social/endereco/email removidos.