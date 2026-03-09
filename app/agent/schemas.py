"""Schemas Pydantic para input/output do agente e da API."""

from typing import Optional

from pydantic import BaseModel, Field


class ErroInput(BaseModel):
    """Erro retornado pela prefeitura."""

    codigo: Optional[str] = Field(None, description="Codigo do erro (ex: E001, E042)")
    mensagem: str = Field(..., description="Mensagem de erro retornada pela prefeitura")


class DiagnosticoRequest(BaseModel):
    """Requisicao de diagnostico de NFSe rejeitada."""

    xml: str = Field(..., description="Conteudo XML da NFSe rejeitada")
    erro: ErroInput = Field(..., description="Informacoes do erro retornado pela prefeitura")


class TagProblema(BaseModel):
    """Informacoes sobre uma TAG XML com problema."""

    tag: str = Field(..., description="Nome da TAG XML com problema (ex: cTribNac)")
    cam_codigo: Optional[str] = Field(None, description="CamCodigo correspondente no sistema")
    valor_enviado: str = Field(..., description="Valor enviado no XML rejeitado")
    valor_correto: str = Field(..., description="Valor correto esperado")
    explicacao: str = Field(..., description="Explicacao do problema nesta TAG")


class Solucao(BaseModel):
    """Solucao estruturada para o problema diagnosticado."""

    resumo: str = Field(..., description="Resumo da solucao em uma frase")
    passos: list[str] = Field(default_factory=list, description="Passos detalhados para correcao")
    xml_corrigido: str = Field(default="", description="Trecho do XML corrigido (apenas TAGs alteradas)")


class Metadata(BaseModel):
    """Metadados do diagnostico."""

    classificacao: str = Field(
        ...,
        description="Origem do erro: CLIENTE, SOFTWARE, PREFEITURA ou INDETERMINADO",
    )
    confianca: str = Field(
        ...,
        description="Nivel de confianca: ALTA, MEDIA ou BAIXA",
    )
    erro_catalogado: bool = Field(
        ...,
        description="True se o erro foi encontrado no catalogo de erros",
    )


class DiagnosticoResponse(BaseModel):
    """Resposta estruturada do agente de diagnostico."""

    status: str = Field(
        ...,
        description="Status do diagnostico: DIAGNOSTICADO, INCONCLUSIVO ou FORA_DE_ESCOPO",
    )
    tags_com_problema: list[TagProblema] = Field(
        default_factory=list,
        description="Lista de TAGs XML com problema identificado",
    )
    solucao: Solucao = Field(..., description="Solucao detalhada para o problema")
    metadata: Metadata = Field(..., description="Metadados do diagnostico")


class DiagnosticoAPIResponse(BaseModel):
    """Resposta da API REST de diagnostico, com tempo de processamento."""

    status: str = Field(..., description="Status: DIAGNOSTICADO, INCONCLUSIVO ou FORA_DE_ESCOPO")
    tags_com_problema: list[dict] = Field(default_factory=list)
    solucao: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    tempo_processamento_ms: float = Field(..., description="Tempo de processamento em milissegundos")
