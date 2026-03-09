"""Script de teste isolado das 4 tools do agente.

Testa cada tool individualmente com dados reais do projeto.
Requer: PostgreSQL rodando com dados ingeridos, .env configurado.
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.tools.buscar_catalogo import buscar_catalogo_erros
from app.tools.consultar_regra import consultar_regra_negocio
from app.tools.validar_xml import validar_xml_contra_template
from app.tools.buscar_autorizado import buscar_xml_autorizado_similar


def test_buscar_catalogo():
    print("=" * 60)
    print("TESTE 1: buscar_catalogo_erros")
    print("=" * 60)
    result = buscar_catalogo_erros.invoke("E001")
    print(result[:1500])
    print("..." if len(result) > 1500 else "")
    assert "Nenhum erro similar" not in result, "Deveria encontrar E001"
    print(chr(10) + ">>> TESTE 1 OK" + chr(10))


def test_consultar_regra():
    print("=" * 60)
    print("TESTE 2: consultar_regra_negocio")
    print("=" * 60)
    result = consultar_regra_negocio.invoke("cTribNac")
    print(result[:1500])
    print("..." if len(result) > 1500 else "")
    assert "Nenhuma regra" not in result, "Deveria encontrar regras para cTribNac"
    print(chr(10) + ">>> TESTE 2 OK" + chr(10))


def test_validar_xml():
    print("=" * 60)
    print("TESTE 3: validar_xml_contra_template")
    print("=" * 60)
    xml_path = Path(__file__).resolve().parent.parent / "data" / "exemplo_rejeitado" / "RPS1094667600012600000000001268700001.xml"
    if xml_path.exists():
        with open(xml_path, "r", encoding="utf-8") as f:
            xml_content = f.read()
    else:
        xml_content = chr(60) + "DPS versao=" + chr(34) + "1.0" + chr(34) + chr(62) + chr(60) + "infDPS id=" + chr(34) + "test" + chr(34) + chr(62) + chr(60) + "tpAmb" + chr(62) + "2" + chr(60) + "/tpAmb" + chr(62) + chr(60) + "/infDPS" + chr(62) + chr(60) + "/DPS" + chr(62)
    result = validar_xml_contra_template.invoke(xml_content)
    print(result[:2000])
    print("..." if len(result) > 2000 else "")
    assert "BETHA" in result, "Deveria detectar padrao BETHA"
    print(chr(10) + ">>> TESTE 3 OK" + chr(10))


def test_validar_xml_malformado():
    print("=" * 60)
    print("TESTE 3b: validar_xml_contra_template (XML malformado)")
    print("=" * 60)
    result = validar_xml_contra_template.invoke("<xml>sem fechamento")
    print(result)
    assert "ERRO" in result, "Deveria reportar erro de parse"
    print(chr(10) + ">>> TESTE 3b OK" + chr(10))


def test_buscar_autorizado():
    print("=" * 60)
    print("TESTE 4: buscar_xml_autorizado_similar")
    print("=" * 60)
    result = buscar_xml_autorizado_similar.invoke("servico tributacao nacional cTribNac aliquota ISS")
    print(result[:1500])
    print("..." if len(result) > 1500 else "")
    assert "Nenhum XML autorizado" not in result, "Deveria encontrar XMLs autorizados"
    print(chr(10) + ">>> TESTE 4 OK" + chr(10))


def main():
    print(chr(10) + "Iniciando testes das tools do agente..." + chr(10))
    errors = []
    for test_fn in [test_buscar_catalogo, test_consultar_regra, test_validar_xml, test_validar_xml_malformado, test_buscar_autorizado]:
        try:
            test_fn()
        except Exception as e:
            print(chr(10) + ">>> FALHA: " + str(e) + chr(10))
            errors.append((test_fn.__name__, str(e)))
    print(chr(10) + "=" * 60)
    if errors:
        print("RESULTADO: " + str(len(errors)) + " teste(s) falharam:")
        for name, err in errors:
            print("  - " + name + ": " + err)
        sys.exit(1)
    else:
        print("RESULTADO: Todos os testes passaram!")
    print("=" * 60)


if __name__ == "__main__":
    main()
