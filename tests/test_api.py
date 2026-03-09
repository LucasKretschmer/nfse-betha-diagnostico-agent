"""Testes da API REST do agente de diagnostico NFSe Betha.

Estes testes usam mocks para evitar chamadas reais ao LLM e banco de dados.
Para rodar: pytest tests/test_api.py -v
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REJEITADO_DIR = DATA_DIR / "exemplo_rejeitado"


def get_xml_rejeitado() -> str:
    xml_files = list(REJEITADO_DIR.glob("*.xml"))
    if xml_files:
        return xml_files[0].read_text(encoding="utf-8")
    return "<DPS versao=chr(34)1.0chr(34)><infDPS></infDPS></DPS>"


def make_mock_structured_response():
    """Cria um DiagnosticoResponse mockado."""
    from app.agent.schemas import DiagnosticoResponse, Metadata, Solucao, TagProblema
    return DiagnosticoResponse(
        status="DIAGNOSTICADO",
        tags_com_problema=[
            TagProblema(
                tag="cTribNac",
                cam_codigo="CAM001",
                valor_enviado="",
                valor_correto="140101",
                explicacao="Campo cTribNac ausente em cServ",
            )
        ],
        solucao=Solucao(
            resumo="Adicionar cTribNac com 6 digitos em cServ",
            passos=["Verificar codTributNacional no cadastro"],
            xml_corrigido="<cTribNac>140101</cTribNac>",
        ),
        metadata=Metadata(
            classificacao="SOFTWARE",
            confianca="ALTA",
            erro_catalogado=True,
        ),
    )


@pytest.fixture
def mock_agent():
    """Fixture que retorna um agente mockado."""
    structured = make_mock_structured_response()
    agent = MagicMock()
    agent.invoke.return_value = {"structured_response": structured, "messages": []}
    return agent


@pytest.fixture
def client(mock_agent):
    """TestClient com agente mockado via patch no lifespan."""
    from app.main import app
    with patch("app.main.get_or_create_agent", return_value=mock_agent):
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c


class TestHealthEndpoint:
    """Testes para o endpoint /health."""

    def test_health_sem_agente(self, client):
        """Testa health check com agente=None apos startup."""
        import app.main as main_module
        orig = main_module._agent
        main_module._agent = None
        try:
            resp = client.get("/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "ok"
            assert data["agent_ready"] is False
        finally:
            main_module._agent = orig

    def test_health_com_agente(self, client):
        """Testa health check com agente inicializado."""
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["agent_ready"] is True


class TestDiagnosticoEndpoint:
    """Testes para o endpoint /diagnostico."""

    def test_diagnostico_retorna_200(self, client):
        """Testa que /diagnostico retorna 200 com XML valido."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {
                "codigo": "E001",
                "mensagem": "E001: cvc-complex-type.2.4.b: conteudo do elemento cServ nao completo",
            },
        }
        resp = client.post("/diagnostico", json=payload)
        assert resp.status_code == 200

    def test_diagnostico_estrutura_resposta(self, client):
        """Testa que a resposta tem todos os campos obrigatorios."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {
                "codigo": "E001",
                "mensagem": "E001: erro de schema",
            },
        }
        resp = client.post("/diagnostico", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "tags_com_problema" in data
        assert "solucao" in data
        assert "metadata" in data
        assert "tempo_processamento_ms" in data

    def test_diagnostico_status_valido(self, client):
        """Testa que o status esta entre os valores validos."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"codigo": "E001", "mensagem": "erro"},
        }
        resp = client.post("/diagnostico", json=payload)
        data = resp.json()
        assert data["status"] in {"DIAGNOSTICADO", "INCONCLUSIVO", "FORA_DE_ESCOPO"}

    def test_diagnostico_classificacao_valida(self, client):
        """Testa que a classificacao esta entre os valores validos."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"codigo": "E001", "mensagem": "erro"},
        }
        resp = client.post("/diagnostico", json=payload)
        data = resp.json()
        meta = data.get("metadata", {})
        assert meta.get("classificacao") in {
            "CLIENTE", "SOFTWARE", "PREFEITURA", "INDETERMINADO"
        }

    def test_diagnostico_confianca_valida(self, client):
        """Testa que a confianca esta entre os valores validos."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"codigo": "E001", "mensagem": "erro"},
        }
        resp = client.post("/diagnostico", json=payload)
        data = resp.json()
        meta = data.get("metadata", {})
        assert meta.get("confianca") in {"ALTA", "MEDIA", "BAIXA"}

    def test_diagnostico_sem_codigo_erro(self, client):
        """Testa que codigo_erro e opcional."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"mensagem": "Erro desconhecido sem codigo"},
        }
        resp = client.post("/diagnostico", json=payload)
        assert resp.status_code == 200

    def test_diagnostico_sem_agente_retorna_503(self, client):
        """Testa que com agente=None retorna 503."""
        import app.main as main_module
        orig = main_module._agent
        main_module._agent = None
        try:
            resp = client.post("/diagnostico", json={"xml": "<DPS/>", "erro": {"mensagem": "erro"}})
            assert resp.status_code == 503
        finally:
            main_module._agent = orig

    def test_diagnostico_tags_com_problema_lista(self, client):
        """Testa que tags_com_problema e uma lista."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"codigo": "E001", "mensagem": "erro"},
        }
        resp = client.post("/diagnostico", json=payload)
        data = resp.json()
        assert isinstance(data["tags_com_problema"], list)

    def test_diagnostico_solucao_tem_passos(self, client):
        """Testa que solucao contem passos."""
        xml = get_xml_rejeitado()
        payload = {
            "xml": xml,
            "erro": {"codigo": "E001", "mensagem": "erro"},
        }
        resp = client.post("/diagnostico", json=payload)
        data = resp.json()
        solucao = data.get("solucao", {})
        assert "resumo" in solucao
        assert "passos" in solucao
        assert isinstance(solucao["passos"], list)
