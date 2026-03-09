"""Tool para consultar regras de negocio do padrao Betha 2945."""

from langchain.tools import tool

from app.vectorstore.retriever import search_regras


@tool
def consultar_regra_negocio(nome_tag_ou_camcodigo: str) -> str:
    """Consulta as regras de negocio de preenchimento do XML NFSe Betha. Use quando precisar saber como uma TAG especifica deve ser preenchida.

    Args:
        nome_tag_ou_camcodigo: Nome da TAG XML (ex: "Aliquota", "ValorIss") ou CamCodigo do sistema (ex: "CAM001").

    Returns:
        Regras de preenchimento, validacoes, dependencias e particularidades da TAG consultada.
    """
    results = search_regras(nome_tag_ou_camcodigo, k=5)

    if not results:
        return (
            "Nenhuma regra encontrada para esta TAG. "
            "Verifique o nome exato da TAG no template Betha."
        )

    parts = []
    for i, r in enumerate(results, 1):
        meta = r.get("metadata", {})
        secao = meta.get("secao", "N/A")
        tipo = meta.get("tipo", "N/A")
        conteudo = r.get("page_content", "")

        parts.append(f"--- Regra {i} (secao: {secao}, tipo: {tipo}) ---")
        parts.append(conteudo)
        parts.append("")

    return chr(10).join(parts)
