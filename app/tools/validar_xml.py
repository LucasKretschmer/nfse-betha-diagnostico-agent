"""Tool para validar estrutura de XML NFSe Betha contra template."""

import logging
from pathlib import Path

from langchain.tools import tool
from lxml import etree

logger = logging.getLogger(__name__)

_TEMPLATE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "template_betha.xml"

# Namespaces conhecidos para deteccao de padrao
_BETHA_INDICATORS = ["betha", "2945", "2948"]
_NACIONAL_INDICATORS = ["abrasf", "nfse.gov.br", "ginfes", "issnet"]


def _detect_pattern(root: etree._Element) -> str:
    """Detecta se o XML e padrao BETHA, NACIONAL ou INDETERMINADO."""
    xml_str = etree.tostring(root, encoding="unicode").lower()
    nsmap = root.nsmap

    # Verificar namespaces
    for ns_val in nsmap.values():
        if ns_val:
            ns_lower = ns_val.lower()
            if any(ind in ns_lower for ind in _NACIONAL_INDICATORS):
                return "NACIONAL"

    # Verificar conteudo
    if any(ind in xml_str for ind in _NACIONAL_INDICATORS):
        return "NACIONAL"

    # XML com tag raiz DPS e estrutura infDPS e padrao Betha
    tag_local = etree.QName(root.tag).localname if root.tag else ""
    if tag_local == "DPS":
        return "BETHA"

    # Verificar indicadores Betha no conteudo
    if any(ind in xml_str for ind in _BETHA_INDICATORS):
        return "BETHA"

    return "INDETERMINADO"


def _strip_ns(tag: str) -> str:
    """Remove namespace de um tag name."""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _get_all_tag_paths(element: etree._Element, prefix: str = "") -> dict[str, str]:
    """Retorna dict de {caminho_tag: valor_texto} para todos os elementos."""
    result = {}
    tag_name = _strip_ns(element.tag)
    current_path = f"{prefix}/{tag_name}" if prefix else tag_name

    text = (element.text or "").strip()
    if text:
        result[current_path] = text
    else:
        result[current_path] = ""

    for child in element:
        child_results = _get_all_tag_paths(child, current_path)
        result.update(child_results)

    return result


def _load_template() -> etree._Element:
    """Carrega e parseia o template Betha."""
    if not _TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template nao encontrado: {_TEMPLATE_PATH}")
    return etree.parse(str(_TEMPLATE_PATH)).getroot()


def _is_placeholder(value: str) -> bool:
    """Verifica se um valor e placeholder do template (AAAAAAAAAA, 99999, etc)."""
    if not value:
        return True
    stripped = value.strip()
    if stripped in ("AAAAAAAAAA", "0", "99999", "99999.99"):
        return True
    if all(c == "A" for c in stripped):
        return True
    return False


@tool
def validar_xml_contra_template(xml_cliente: str) -> str:
    """Valida o XML do cliente comparando com o template Betha. Identifica TAGs faltantes, valores vazios e se o XML e padrao Betha ou Nacional.

    Args:
        xml_cliente: Conteudo completo do XML enviado pelo cliente.

    Returns:
        Lista de divergencias encontradas e identificacao do padrao do XML.
    """
    # Parse do XML do cliente
    try:
        cliente_root = etree.fromstring(xml_cliente.encode("utf-8"))
    except etree.XMLSyntaxError as e:
        return f"ERRO: XML malformado - nao foi possivel parsear o XML.\nDetalhe: {e}"

    # Deteccao de padrao
    padrao = _detect_pattern(cliente_root)

    if padrao == "NACIONAL":
        return (
            "XML identificado como padrao NACIONAL, fora do escopo deste agente "
            "que atende apenas padrao Betha (2945)."
        )

    # Carregar template
    try:
        template_root = _load_template()
    except FileNotFoundError as e:
        return f"ERRO: {e}"

    # Extrair paths de ambos
    template_tags = _get_all_tag_paths(template_root)
    cliente_tags = _get_all_tag_paths(cliente_root)

    # Remover tags de assinatura digital do cliente (Signature)
    cliente_tags = {
        k: v for k, v in cliente_tags.items()
        if "Signature" not in k and "SignedInfo" not in k
        and "KeyInfo" not in k and "X509" not in k
    }

    # Comparar
    template_set = set(template_tags.keys())
    cliente_set = set(cliente_tags.keys())

    # TAGs no template mas ausentes no cliente
    tags_faltantes = sorted(template_set - cliente_set)

    # TAGs com valor vazio no cliente que tem valor no template
    tags_vazias = []
    for path in sorted(cliente_set & template_set):
        if not cliente_tags[path] and template_tags[path] and not _is_placeholder(template_tags[path]):
            tags_vazias.append(path)

    # TAGs extras no cliente (nao no template)
    tags_extras = sorted(cliente_set - template_set)

    # Montar relatorio
    report = []
    report.append(f"=== Validacao XML contra Template Betha ===")
    report.append(f"Padrao detectado: {padrao}")
    report.append(f"TAGs no template: {len(template_set)}")
    report.append(f"TAGs no cliente: {len(cliente_set)}")
    report.append("")

    if tags_faltantes:
        report.append(f"## TAGs FALTANTES no XML do cliente ({len(tags_faltantes)}):")
        # Filtrar para mostrar apenas tags folha (sem filhos no template)
        tags_folha_faltantes = []
        for t in tags_faltantes:
            has_children = any(other.startswith(t + "/") for other in template_set)
            if not has_children:
                tags_folha_faltantes.append(t)
            else:
                # Grupo inteiro ausente - mostrar o pai
                pass

        # Agrupar por pai para clareza
        shown = set()
        for t in tags_faltantes:
            # Verificar se e um grupo (tem filhos tambem faltantes)
            children_missing = [c for c in tags_faltantes if c.startswith(t + "/")]
            parent = "/".join(t.split("/")[:-1])
            if parent in shown:
                continue
            if children_missing and len(children_missing) > 2:
                report.append(f"  - {t} (bloco inteiro ausente, {len(children_missing)} sub-tags)")
                shown.add(t)
            elif t not in shown:
                report.append(f"  - {t}")
                shown.add(t)
        report.append("")

    if tags_vazias:
        report.append(f"## TAGs com VALOR VAZIO no cliente ({len(tags_vazias)}):")
        for t in tags_vazias:
            report.append(f"  - {t} (template sugere valor)")
        report.append("")

    if tags_extras:
        report.append(f"## TAGs EXTRAS no cliente (nao no template) ({len(tags_extras)}):")
        for t in tags_extras:
            val = cliente_tags[t]
            if val:
                report.append(f"  - {t} = {val[:100]}")
            else:
                report.append(f"  - {t}")
        report.append("")

    if not tags_faltantes and not tags_vazias:
        report.append("Nenhuma divergencia estrutural significativa encontrada.")

    return "\n".join(report)
