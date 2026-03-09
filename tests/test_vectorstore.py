"""Testes do modulo vectorstore (funcoes puras, sem conexao ao banco)."""

import json
import os
from pathlib import Path

import pytest

from app.vectorstore.ingest import (
    _build_catalogo_text,
    _looks_like_tag_section,
    _process_xml_autorizado,
    _safe_get,
    _sanitize_catalogo_metadata,
    _split_regras_into_chunks,
)


class TestBuildCatalogoText:
    """Testes para geracao de texto descritivo do catalogo."""

    def test_basic_error(self) -> None:
        """Texto inclui todos os campos do erro."""
        erro = {
            "codigo_erro": "E001",
            "mensagem_erro": "Erro de Schema XML",
            "causa_raiz": "cTribNac ausente",
            "tags_relacionadas": ["cTribNac", "xDescServ"],
            "cam_codigos_relacionados": ["553"],
            "diagnostico": {
                "como_identificar": "Mensagem contem E001",
                "tag_verificar": "<cTribNac>",
                "valor_tipico_errado": "<cTribNac>1</cTribNac>",
                "valor_correto_esperado": "<cTribNac>140101</cTribNac>",
            },
            "solucao_detalhada": {
                "passos": ["Verificar campo codTributNacional"],
            },
            "solucao_resumida": "Preencher cTribNac com 6 digitos",
            "classificacao": "SOFTWARE",
        }
        text = _build_catalogo_text(erro)
        assert "E001" in text
        assert "cTribNac" in text
        assert "140101" in text
        assert "SOFTWARE" in text

    def test_missing_fields(self) -> None:
        """Texto gerado mesmo com campos faltantes."""
        erro = {"codigo_erro": "E999"}
        text = _build_catalogo_text(erro)
        assert "E999" in text
        assert "N/A" in text


class TestSanitizeCatalogoMetadata:
    """Testes para sanitizacao de metadata."""

    def test_removes_cnpj(self) -> None:
        """CNPJs sao substituidos no metadata."""
        erro = {
            "codigo_erro": "E001",
            "notas_adicionais": "CNPJ 02089242000129 concentra maioria",
        }
        meta = _sanitize_catalogo_metadata(erro)
        assert "02089242000129" not in meta["notas_adicionais"]
        assert "CNPJ_OMITIDO" in meta["notas_adicionais"]

    def test_removes_sensitive_fields(self) -> None:
        """Campos sensiveis sao omitidos."""
        erro = {
            "codigo_erro": "E001",
            "municipios_novos_dados": ["Lages"],
            "frequencia_novos_dados": 14,
        }
        meta = _sanitize_catalogo_metadata(erro)
        assert "municipios_novos_dados" not in meta
        assert "frequencia_novos_dados" not in meta
        assert meta["codigo_erro"] == "E001"


class TestSplitRegras:
    """Testes para split de regras de negocio."""

    def test_splits_by_h2(self) -> None:
        """Divide corretamente por secoes ##."""
        content = "# Titulo\nIntro\n\n## Secao 1\nConteudo 1\n\n## Secao 2\nConteudo 2"
        chunks = _split_regras_into_chunks(content)
        assert len(chunks) >= 2
        titles = [c[0] for c in chunks]
        assert any("Secao 1" in t for t in titles)

    def test_large_section_splits_by_h3(self) -> None:
        """Secoes grandes sao subdivididas por ###."""
        big = "## Secao Grande\n" + "x" * 2500 + "\n### Sub1\nConteudo\n### Sub2\nConteudo"
        chunks = _split_regras_into_chunks(big, max_chunk_size=2000)
        assert len(chunks) >= 2


class TestProcessXmlAutorizado:
    """Testes para processamento de XMLs autorizados."""

    def test_extracts_fields(self) -> None:
        """Extrai campos relevantes do JSON."""
        data = {
            "DadosRPS": {
                "RPS": [{
                    "natOp": "7",
                    "OptSN": "2",
                    "tpAmb": "1",
                    "regApTribSN": "",
                    "RegEspTrib": "",
                    "Servico": {
                        "codTributNacional": "040101",
                        "IteListServico": "04.01",
                        "CodigoNBS": "123012200",
                        "Cnae": "",
                        "cMun": "3170701",
                        "cMunIncidencia": "3170701",
                        "Valores": {
                            "ValServicos": "60.00",
                            "ValAliqISS": "3.000000",
                            "ValISS": "1.80",
                            "ISSRetido": "2",
                            "ValDescIncond": "0.00",
                        },
                    },
                    "Prestador": {"CNPJ_prest": "35723993000104"},
                    "Tomador": {"TomaCPF": "02398610608"},
                }]
            }
        }
        text, meta = _process_xml_autorizado(data, "test.json")
        assert "040101" in text
        assert "3.000000" in text
        # Dados pessoais NAO expostos
        assert "35723993000104" not in text
        assert "02398610608" not in text
        assert meta["codigo_servico"] == "040101"
        assert "cTribNac" in meta["tags_presentes"]

    def test_empty_rps(self) -> None:
        """Retorna vazio se nao tem RPS."""
        text, meta = _process_xml_autorizado({}, "empty.json")
        assert text == ""

    def test_no_personal_data_in_text(self) -> None:
        """Nenhum dado pessoal aparece no texto descritivo."""
        data = {
            "DadosRPS": {
                "RPS": [{
                    "natOp": "1",
                    "OptSN": "1",
                    "tpAmb": "1",
                    "Servico": {
                        "codTributNacional": "010301",
                        "Valores": {"ValServicos": "100.00"},
                    },
                    "Prestador": {
                        "CNPJ_prest": "12345678000199",
                        "xNome": "EMPRESA TESTE LTDA",
                        "enderPrest": {"xLgr": "Rua Teste", "Email": "test@test.com"},
                    },
                    "Tomador": {
                        "TomaCNPJ": "98765432000188",
                        "TomaRazaoSocial": "CLIENTE TESTE",
                        "TomaEmail": "cliente@test.com",
                    },
                }]
            }
        }
        text, meta = _process_xml_autorizado(data, "test2.json")
        assert "12345678000199" not in text
        assert "98765432000188" not in text
        assert "EMPRESA TESTE" not in text
        assert "CLIENTE TESTE" not in text
        assert "test@test.com" not in text


class TestSafeGet:
    """Testes para acesso seguro a dicts aninhados."""

    def test_existing_keys(self) -> None:
        data = {"a": {"b": {"c": 42}}}
        assert _safe_get(data, ["a", "b", "c"]) == 42

    def test_missing_key(self) -> None:
        data = {"a": {"b": 1}}
        assert _safe_get(data, ["a", "x"]) is None

    def test_empty_keys(self) -> None:
        data = {"a": 1}
        assert _safe_get(data, []) == data


class TestLooksLikeTagSection:
    """Testes para heuristica de deteccao de secao de TAG."""

    def test_tag_section(self) -> None:
        text = "### TAG cTribNac\nConteudo sobre a tag"
        assert _looks_like_tag_section(text, {"TAG ", "CamCodigo"})

    def test_general_section(self) -> None:
        text = "### Visao Geral\nTexto sobre o sistema"
        assert not _looks_like_tag_section(text, {"TAG ", "CamCodigo"})
