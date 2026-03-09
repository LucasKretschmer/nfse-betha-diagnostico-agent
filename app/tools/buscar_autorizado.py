"""Tool para buscar XMLs autorizados como referencia."""

from langchain.tools import tool

from app.vectorstore.retriever import search_xmls_autorizados_com_threshold


@tool
def buscar_xml_autorizado_similar(descricao_servico_ou_tags: str) -> str:
    """Busca XMLs autorizados de referencia para comparacao estrutural. Use para encontrar um exemplo de XML que foi aceito, comparando estrutura e valores de referencia.

    Args:
        descricao_servico_ou_tags: Descricao do tipo de servico, codigo de servico, ou nomes de TAGs para encontrar XMLs de referencia similares.

    Returns:
        Estrutura e valores de referencia de um XML autorizado similar, util para comparar com o XML rejeitado.
    """
    results = search_xmls_autorizados_com_threshold(descricao_servico_ou_tags, k=2)

    if not results:
        return (
            "Nenhum XML autorizado de referencia encontrado na base "
            "para este tipo de servico."
        )

    parts = []
    for i, r in enumerate(results, 1):
        meta = r.get("metadata", {})
        conteudo = r.get("page_content", "")

        info = []
        info.append(f"--- XML Autorizado {i} ---")
        info.append(f"Arquivo: {meta.get('nome_arquivo', 'N/A')}")
        info.append(f"Codigo servico: {meta.get('codigo_servico', 'N/A')}")
        info.append(f"Municipio: {meta.get('municipio', 'N/A')}")
        info.append(f"Aliquota ISS: {meta.get('aliquota_iss', 'N/A')}")
        info.append(f"Natureza operacao: {meta.get('natureza_operacao', 'N/A')}")
        info.append(f"Optante Simples: {meta.get('optante_simples', 'N/A')}")

        tags_presentes = meta.get("tags_presentes", [])
        if tags_presentes:
            info.append(f"TAGs presentes: {', '.join(str(t) for t in tags_presentes)}")

        info.append("")
        info.append("Dados de referencia:")
        info.append(conteudo)
        info.append("")

        parts.append(chr(10).join(info))

    return chr(10).join(parts)
