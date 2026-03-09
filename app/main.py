"""FastAPI application - ponto de entrada da API REST."""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage

from app.agent.factory import get_or_create_agent
from app.agent.schemas import DiagnosticoAPIResponse, DiagnosticoRequest, DiagnosticoResponse

logger = logging.getLogger(__name__)

_agent = None


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Inicializa o agente na startup e libera recursos no shutdown."""
    global _agent
    logger.info("Iniciando agente de diagnostico NFSe...")
    try:
        _agent = get_or_create_agent()
        logger.info("Agente inicializado com sucesso")
    except Exception as e:
        logger.error("Erro ao inicializar agente: %s", e)
        raise
    yield
    logger.info("Encerrando agente")
    _agent = None


app = FastAPI(
    title="NFSe Betha Diagnostico Agent",
    description="Agente de IA para diagnostico de rejeicoes NFSe padrao Betha 2945",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "agent_ready": _agent is not None,
    }


@app.post("/diagnostico", response_model=DiagnosticoAPIResponse)
async def diagnosticar_xml(request: DiagnosticoRequest) -> DiagnosticoAPIResponse:
    """Diagnostica uma NFSe rejeitada e retorna solucao estruturada.

    Recebe o XML rejeitado e o erro retornado pela prefeitura.
    Usa o agente LLM com 4 tools especializadas para gerar o diagnostico.
    """
    if _agent is None:
        raise HTTPException(status_code=503, detail="Agente nao inicializado")

    erro_info = "Erro: " + request.erro.mensagem
    if request.erro.codigo:
        erro_info = "Codigo: " + request.erro.codigo + ". " + erro_info

    sep = chr(10)
    human_message = ("Diagnostique a seguinte rejeicao de NFSe Betha:" + sep + sep + erro_info + sep + sep + "XML rejeitado:" + sep + request.xml)

    inicio = time.time()
    try:
        result = _agent.invoke({"messages": [HumanMessage(content=human_message)]})
    except Exception as e:
        logger.error("Erro ao invocar agente: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do agente: " + str(e))

    tempo_ms = (time.time() - inicio) * 1000

    structured: DiagnosticoResponse | None = result.get("structured_response")

    if structured is None:
        logger.warning("structured_response ausente no resultado do agente")
        raise HTTPException(status_code=500, detail="Agente nao retornou resposta estruturada")

    return DiagnosticoAPIResponse(
        status=structured.status,
        tags_com_problema=[t.model_dump() for t in structured.tags_com_problema],
        solucao=structured.solucao.model_dump(),
        metadata=structured.metadata.model_dump(),
        tempo_processamento_ms=round(tempo_ms, 2),
    )
