"""Ingestao de dados no PGVectorStore.

Estrategia: pre-processar dados estruturados em texto descritivo
antes de gerar embeddings, para melhor busca semantica.

LGPD: Dados pessoais (CNPJ, razao social, endereco, email, telefone)
sao REMOVIDOS ou SANITIZADOS antes da ingestao.
"""

import json
import logging
import re
import uuid
from pathlib import Path
from typing import Any

from langchain_core.documents import Document

from app.config import get_settings
from app.vectorstore.connection import get_vectorstore, init_vectorstore_table

logger = logging.getLogger(__name__)

_RE_CNPJ = re.compile(r"\d{14}")


def ingest_catalogo(json_path: str) -> int:
    """Ingere catalogo de erros no PGVectorStore.

    Para cada erro, gera texto descritivo pesquisavel com:
    codigo, mensagem, causa raiz, tags, diagnostico completo, solucao.

    Args:
        json_path: Caminho para catalogo_enriquecido.json

    Returns:
        Numero de documentos ingeridos
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    if not isinstance(catalogo, list):
        raise ValueError(f"JSON deve ser uma lista de erros, recebeu {type(catalogo)}")

    settings = get_settings()
    table_name = settings.pgvector_collection_catalogo
    init_vectorstore_table(table_name)
    vectorstore = get_vectorstore(table_name)

    documents = []
    for erro in catalogo:
        page_content = _build_catalogo_text(erro)
        metadata = _sanitize_catalogo_metadata(erro)
        doc = Document(
            id=str(uuid.uuid4()),
            page_content=page_content,
            metadata=metadata,
        )
        documents.append(doc)

    vectorstore.add_documents(documents)
    count = len(documents)
    print(f"Catalogo: {count} erros ingeridos com sucesso")
    logger.info("Catalogo: %d erros ingeridos", count)
    return count


def _build_catalogo_text(erro: dict[str, Any]) -> str:
    """Gera texto descritivo pesquisavel para um erro do catalogo."""
    tags = ", ".join(erro.get("tags_relacionadas", []))
    cam_codigos = ", ".join(str(c) for c in erro.get("cam_codigos_relacionados", []))
    diag = erro.get("diagnostico", {})
    sol = erro.get("solucao_detalhada", {})
    passos = " ".join(sol.get("passos", []))

    parts = [
        f"Erro {erro.get('codigo_erro', 'N/A')}: {erro.get('mensagem_erro', 'N/A')}.",
        f"Causa raiz: {erro.get('causa_raiz', 'N/A')}.",
        f"TAGs relacionadas: {tags}.",
        f"CamCodigos: {cam_codigos}.",
        f"Diagnostico: {diag.get('como_identificar', 'N/A')}.",
        f"TAG a verificar: {diag.get('tag_verificar', 'N/A')}.",
        f"Valor tipico incorreto: {diag.get('valor_tipico_errado', 'N/A')}.",
        f"Valor correto esperado: {diag.get('valor_correto_esperado', 'N/A')}.",
        f"Solucao resumida: {erro.get('solucao_resumida', 'N/A')}.",
        f"Passos da solucao: {passos}.",
        f"Classificacao: {erro.get('classificacao', 'N/A')}.",
    ]
    return "\n".join(parts)


def _sanitize_catalogo_metadata(erro: dict[str, Any]) -> dict[str, Any]:
    """Remove dados sensiveis do metadata do catalogo."""
    skip_fields = {"municipios_novos_dados", "frequencia_novos_dados"}
    metadata = {}
    for key, value in erro.items():
        if key in skip_fields:
            continue
        if isinstance(value, str):
            value = _RE_CNPJ.sub("CNPJ_OMITIDO", value)
        metadata[key] = value
    if "notas_adicionais" in metadata and isinstance(metadata["notas_adicionais"], str):
        metadata["notas_adicionais"] = _RE_CNPJ.sub(
            "CNPJ_OMITIDO", metadata["notas_adicionais"]
        )
    return metadata


# ---------------------------------------------------------------------------
# Regras de negocio
# ---------------------------------------------------------------------------

def ingest_regras(md_path: str) -> int:
    """Ingere regras de negocio no PGVectorStore.

    Divide o markdown em chunks por secao (## e ###).
    Identifica blocos de TAG individual e gera texto descritivo.

    Args:
        md_path: Caminho para regras_negocio.md

    Returns:
        Numero de chunks ingeridos
    """
    path = Path(md_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {md_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = _split_regras_into_chunks(content)

    settings = get_settings()
    table_name = settings.pgvector_collection_regras
    init_vectorstore_table(table_name)
    vectorstore = get_vectorstore(table_name)

    documents = []
    tag_count = 0
    secao_count = 0
    for titulo, texto, is_tag in chunks:
        doc = Document(
            id=str(uuid.uuid4()),
            page_content=texto,
            metadata={
                "secao": titulo,
                "tipo": "tag" if is_tag else "secao_geral",
                "fonte": "regras_negocio.md",
            },
        )
        documents.append(doc)
        if is_tag:
            tag_count += 1
        else:
            secao_count += 1

    vectorstore.add_documents(documents)
    count = len(documents)
    print(
        f"Regras: {count} chunks ingeridos ({tag_count} TAGs + {secao_count} secoes gerais)"
    )
    logger.info(
        "Regras: %d chunks ingeridos (%d TAGs + %d secoes)", count, tag_count, secao_count
    )
    return count


def _split_regras_into_chunks(
    content: str, max_chunk_size: int = 2000
) -> list[tuple[str, str, bool]]:
    """Divide markdown de regras em chunks semanticos.

    Returns:
        Lista de (titulo, conteudo, is_tag_chunk)
    """
    sections = content.split("\n## ")
    chunks: list[tuple[str, str, bool]] = []
    tag_keywords = {"TAG ", "CamCodigo", "<", "tag_"}

    for i, section in enumerate(sections):
        if i == 0:
            if section.strip():
                title = section.split("\n")[0].strip("# ").strip()
                chunks.append((title or "Cabecalho", section.strip(), False))
            continue

        full_section = "## " + section
        lines = full_section.split("\n")
        title = lines[0].strip("# ").strip()

        if len(full_section) <= max_chunk_size:
            is_tag = _looks_like_tag_section(full_section, tag_keywords)
            chunks.append((title, full_section.strip(), is_tag))
        else:
            subsections = full_section.split("\n### ")
            for j, subsec in enumerate(subsections):
                if j == 0:
                    sub_title = title
                    sub_content = subsec.strip()
                    is_tag = False
                else:
                    sub_content = "### " + subsec
                    first_line = sub_content.split("\n")[0]
                    sub_title = title + " > " + first_line.strip("# ").strip()
                    sub_content = sub_content.strip()
                    is_tag = _looks_like_tag_section(sub_content, tag_keywords)
                if sub_content:
                    chunks.append((sub_title, sub_content, is_tag))

    return chunks


def _looks_like_tag_section(text: str, keywords: set[str]) -> bool:
    """Heuristica: secao parece documentar uma TAG XML especifica."""
    first_lines = "\n".join(text.split("\n")[:5])
    return any(kw in first_lines for kw in keywords)


# ---------------------------------------------------------------------------
# XMLs autorizados
# ---------------------------------------------------------------------------

def ingest_xmls_autorizados(dir_path: str) -> int:
    """Ingere XMLs autorizados no PGVectorStore.

    Le cada arquivo JSON, SANITIZA dados pessoais e gera texto
    descritivo focando na estrutura de TAGs e valores de referencia.

    Args:
        dir_path: Caminho para diretorio xmls_autorizados/

    Returns:
        Numero de XMLs ingeridos
    """
    path = Path(dir_path)
    if not path.exists():
        raise FileNotFoundError(f"Diretorio nao encontrado: {dir_path}")

    files = sorted(path.glob("*.json"))
    if not files:
        print(f"Nenhum arquivo JSON encontrado em {dir_path}")
        return 0

    settings = get_settings()
    table_name = settings.pgvector_collection_xmls
    init_vectorstore_table(table_name)
    vectorstore = get_vectorstore(table_name)

    documents = []
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)

            text, meta = _process_xml_autorizado(raw, filepath.name)
            if not text:
                continue

            doc = Document(
                id=str(uuid.uuid4()),
                page_content=text,
                metadata=meta,
            )
            documents.append(doc)
        except Exception as e:
            logger.warning("Erro ao processar %s: %s", filepath.name, e)
            continue

    if documents:
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            vectorstore.add_documents(batch)
            logger.info("Lote %d-%d inserido", i, i + len(batch))

    count = len(documents)
    print(f"XMLs autorizados: {count} documentos ingeridos (sanitizados)")
    logger.info("XMLs autorizados: %d documentos ingeridos", count)
    return count


def _process_xml_autorizado(
    data: dict[str, Any], filename: str
) -> tuple[str, dict[str, Any]]:
    """Processa um JSON de XML autorizado, sanitiza e gera texto descritivo."""
    rps_list = _safe_get(data, ["DadosRPS", "RPS"])
    if not rps_list or not isinstance(rps_list, list):
        return "", {}

    rps = rps_list[0]
    servico = _safe_get(rps, ["Servico"]) or {}
    valores = _safe_get(servico, ["Valores"]) or {}
    tomador = _safe_get(rps, ["Tomador"]) or {}

    # Extrair dados relevantes (NAO pessoais)
    cod_trib_nac = servico.get("codTributNacional", "")
    ite_list_serv = servico.get("IteListServico", "")
    cnae = servico.get("Cnae", "")
    codigo_nbs = servico.get("CodigoNBS", "")
    c_mun = servico.get("cMun", "")
    c_mun_incid = servico.get("cMunIncidencia", "")
    nat_op = rps.get("natOp", "")
    opt_sn = rps.get("OptSN", "")
    reg_ap_trib = rps.get("regApTribSN", "")
    reg_esp_trib = rps.get("RegEspTrib", "")
    tp_amb = rps.get("tpAmb", "")

    val_servicos = valores.get("ValServicos", "")
    val_aliq_iss = valores.get("ValAliqISS", "")
    val_iss = valores.get("ValISS", "")
    iss_retido = valores.get("ISSRetido", "")
    val_desc_incond = valores.get("ValDescIncond", "")

    # Tags presentes
    tags_presentes = []
    if cod_trib_nac:
        tags_presentes.append("cTribNac")
    if ite_list_serv:
        tags_presentes.append("IteListServico")
    if codigo_nbs:
        tags_presentes.append("cNBS")
    if cnae:
        tags_presentes.append("CNAE")
    if nat_op:
        tags_presentes.append("natOp")
    if val_aliq_iss:
        tags_presentes.append("pAliq")
    if iss_retido:
        tags_presentes.append("tpRetISSQN")

    tom_tipo = "CNPJ" if tomador.get("TomaCNPJ") else (
        "CPF" if tomador.get("TomaCPF") else "N/A"
    )

    # Gerar texto descritivo sanitizado
    parts = ["XML autorizado de referencia."]
    if cod_trib_nac:
        parts.append(f"Codigo tributacao nacional: {cod_trib_nac}.")
    if ite_list_serv:
        parts.append(f"Item lista servico: {ite_list_serv}.")
    if codigo_nbs:
        parts.append(f"Codigo NBS: {codigo_nbs}.")
    if cnae:
        parts.append(f"CNAE: {cnae}.")
    if nat_op:
        parts.append(f"Natureza operacao: {nat_op}.")
    if opt_sn:
        parts.append(f"Optante Simples Nacional: {opt_sn}.")
    if reg_ap_trib:
        parts.append(f"Regime apuracao tributaria SN: {reg_ap_trib}.")
    if reg_esp_trib:
        parts.append(f"Regime especial tributacao: {reg_esp_trib}.")
    if tp_amb:
        parts.append(f"Ambiente: {tp_amb}.")
    if c_mun:
        parts.append(f"Municipio prestacao: {c_mun}.")
    if c_mun_incid:
        parts.append(f"Municipio incidencia: {c_mun_incid}.")
    if val_servicos:
        parts.append(f"Valor servicos: {val_servicos}.")
    if val_aliq_iss:
        parts.append(f"Aliquota ISS: {val_aliq_iss}.")
    if val_iss:
        parts.append(f"Valor ISS: {val_iss}.")
    if iss_retido:
        parts.append(f"ISS retido: {iss_retido}.")
    if val_desc_incond:
        parts.append(f"Desconto incondicional: {val_desc_incond}.")
    parts.append(f"Tipo tomador: {tom_tipo}.")
    if tags_presentes:
        parts.append(f"TAGs presentes: {', '.join(tags_presentes)}.")

    text = "\n".join(parts)

    metadata = {
        "nome_arquivo": filename,
        "tags_presentes": tags_presentes,
        "codigo_servico": ite_list_serv,
        "municipio": c_mun,
        "aliquota_iss": val_aliq_iss,
        "natureza_operacao": nat_op,
        "optante_simples": opt_sn,
    }

    return text, metadata


def _safe_get(data: Any, keys: list[str]) -> Any:
    """Acesso seguro a chaves aninhadas em dict."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current
