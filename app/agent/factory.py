"""Factory para criacao do agente de diagnostico NFSe Betha."""

import logging

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langgraph.graph.state import CompiledStateGraph

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.schemas import DiagnosticoResponse
from app.config import get_settings
from app.tools.buscar_autorizado import buscar_xml_autorizado_similar
from app.tools.buscar_catalogo import buscar_catalogo_erros
from app.tools.consultar_regra import consultar_regra_negocio
from app.tools.validar_xml import validar_xml_contra_template

logger = logging.getLogger(__name__)

_agent: CompiledStateGraph | None = None


def get_agent_tools() -> list:
    """Retorna a lista de tools disponiveis para o agente."""
    return [
        validar_xml_contra_template,
        buscar_catalogo_erros,
        consultar_regra_negocio,
        buscar_xml_autorizado_similar,
    ]


def create_diagnostico_agent() -> CompiledStateGraph:
    """Cria e retorna o agente de diagnostico NFSe Betha.

    Usa create_agent do LangChain v1 com 4 tools e structured output
    via ToolStrategy(DiagnosticoResponse).

    Returns:
        CompiledStateGraph pronto para .invoke()
    """
    settings = get_settings()

    model = init_chat_model(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        model_provider="openai",
        temperature=0,
    )

    tools = get_agent_tools()

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        response_format=ToolStrategy(DiagnosticoResponse),
        name="diagnostico_nfse_betha",
    )

    logger.info(
        "Agente criado com %d tools e structured output DiagnosticoResponse",
        len(tools),
    )
    return agent


def get_or_create_agent() -> CompiledStateGraph:
    """Retorna instancia singleton do agente.

    Cria o agente na primeira chamada e reutiliza nas subsequentes.
    Thread-safe para uso em FastAPI.

    Returns:
        CompiledStateGraph singleton
    """
    global _agent
    if _agent is None:
        _agent = create_diagnostico_agent()
        logger.info("Agente singleton criado")
    return _agent
