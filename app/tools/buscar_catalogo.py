"""Tool para buscar erros no catalogo enriquecido via vector store."""

from langchain.tools import tool

from app.vectorstore.retriever import search_catalogo_hibrido


@tool
def buscar_catalogo_erros(codigo_ou_mensagem_erro: str) -> str:
    """Busca no catalogo de erros enriquecido. Use quando receber o codigo ou mensagem de erro da rejeicao.

    Args:
        codigo_ou_mensagem_erro: Codigo do erro (ex: "E001") ou trecho da mensagem de erro retornada pela prefeitura.

    Returns:
        Informacoes sobre os erros mais similares encontrados no catalogo, incluindo causa raiz, TAGs afetadas e solucao.
    """
    results = search_catalogo_hibrido(codigo_ou_mensagem_erro, k=3)

    if not results:
        return (
            "Nenhum erro similar encontrado no catalogo. "
            "Tente analisar o XML diretamente usando as outras tools."
        )

    parts = []
    for i, r in enumerate(results, 1):
        meta = r.get("metadata", {})
        diag = meta.get("diagnostico", {})
        sol = meta.get("solucao_detalhada", {})
        tags = meta.get("tags_relacionadas", [])
        passos = sol.get("passos", [])

        section = []
        section.append(f"--- Resultado {i} ---")
        section.append(f"Codigo: {meta.get('codigo_erro', 'N/A')}")
        section.append(f"Mensagem: {meta.get('mensagem_erro', 'N/A')}")

        freq = meta.get("frequencia")
        perc = meta.get("percentual")
        if freq:
            section.append(f"Frequencia: {freq} ocorrencias ({perc})")

        if tags:
            section.append(f"TAGs relacionadas: {', '.join(str(t) for t in tags)}")

        section.append(f"Causa raiz: {meta.get('causa_raiz', 'N/A')}")
        section.append(f"Classificacao: {meta.get('classificacao', 'N/A')}")

        if diag:
            section.append(f"Como identificar: {diag.get('como_identificar', 'N/A')}")
            section.append(f"TAG a verificar: {diag.get('tag_verificar', 'N/A')}")
            section.append(f"Valor tipico errado: {diag.get('valor_tipico_errado', 'N/A')}")
            section.append(f"Valor correto esperado: {diag.get('valor_correto_esperado', 'N/A')}")

        section.append(f"Solucao resumida: {meta.get('solucao_resumida', 'N/A')}")

        if passos:
            section.append("Passos da solucao:")
            for j, passo in enumerate(passos, 1):
                section.append(f"  {j}. {passo}")

        xml_incorreto = sol.get("xml_exemplo_incorreto")
        xml_correto = sol.get("xml_exemplo_correto")
        if xml_incorreto:
            section.append(f"XML incorreto: {xml_incorreto}")
        if xml_correto:
            section.append(f"XML correto: {xml_correto}")

        parts.append(chr(10).join(section))

    return chr(10) + chr(10).join(parts)
