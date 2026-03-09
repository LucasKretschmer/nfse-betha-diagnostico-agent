"""Script de teste do agente de diagnostico NFSe Betha.

Uso:
    python scripts/test_agent.py --direto
    python scripts/test_agent.py --api
    python scripts/test_agent.py --todos
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REJEITADO_DIR = DATA_DIR / "exemplo_rejeitado"


def carregar_xml_rejeitado() -> str:
    xml_files = list(REJEITADO_DIR.glob("*.xml"))
    if not xml_files:
        raise FileNotFoundError(f"Nenhum XML encontrado em {REJEITADO_DIR}")
    with open(xml_files[0], "r", encoding="utf-8") as f:
        return f.read()


def teste_direto_agente():
    """Teste 1: invocacao direta do agente."""
    print("=" * 60)
    print("TESTE 1 - Invocacao direta do agente")
    print("=" * 60)

    from langchain_core.messages import HumanMessage
    from app.agent.factory import create_diagnostico_agent

    xml = carregar_xml_rejeitado()
    mensagem_erro = "E001: cvc-complex-type.2.4.b: O conteudo do elemento cServ nao completo."
    codigo_erro = "E001"

    sep = chr(10)
    human_msg = (
        "Diagnostique a seguinte rejeicao de NFSe Betha:" + sep + sep
        + "Codigo: " + codigo_erro + ". Erro: " + mensagem_erro + sep + sep
        + "XML rejeitado:" + sep + xml
    )

    print(f"XML carregado: {len(xml)} chars")
    print(f"Erro: {mensagem_erro}")
    print("")

    print("Criando agente...")
    agent = create_diagnostico_agent()

    print("Invocando agente (pode demorar 15-45s)...")
    inicio = time.time()
    result = agent.invoke({"messages": [HumanMessage(content=human_msg)]})
    tempo = time.time() - inicio

    structured = result.get("structured_response")
    print(f"Tempo: {tempo:.1f}s")
    print("")

    if structured:
        print(f"Status: {structured.status}")
        tags = [t.tag for t in structured.tags_com_problema]
        print(f"Tags com problema: {tags}")
        print(f"Classificacao: {structured.metadata.classificacao}")
        print(f"Confianca: {structured.metadata.confianca}")
        print(f"Erro catalogado: {structured.metadata.erro_catalogado}")
        print(f"Resumo: {structured.solucao.resumo}")
        print(f"Passos ({len(structured.solucao.passos)}):")
        for i, passo in enumerate(structured.solucao.passos, 1):
            print(f"  {i}. {passo}")
        if structured.solucao.xml_corrigido:
            print(f"XML corrigido (trecho): {structured.solucao.xml_corrigido[:200]}")
        print("")
        print("TESTE 1: PASSOU")
    else:
        msgs = result.get("messages", [])
        if msgs:
            print(f"Ultima mensagem: {msgs[-1].content[:500]}")
        print("TESTE 1: FALHOU (sem structured_response)")


def teste_api_http():
    """Teste 2: invocacao via HTTP da API FastAPI."""
    print("=" * 60)
    print("TESTE 2 - Invocacao via API HTTP")
    print("=" * 60)

    try:
        import httpx
    except ImportError:
        print("httpx nao instalado. pip install httpx")
        print("TESTE 2: PULADO")
        return

    xml = carregar_xml_rejeitado()
    payload = {
        "xml": xml,
        "erro": {
            "codigo": "E001",
            "mensagem": "E001: cvc-complex-type.2.4.b: O conteudo do elemento cServ nao completo.",
        },
    }

    base_url = "http://localhost:8000"
    print(f"Chamando {base_url}/diagnostico ...")

    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.get(f"{base_url}/health")
            if resp.status_code != 200:
                print("TESTE 2: PULADO (API nao disponivel)")
                return
            print(f"Health: {resp.json()}")

            resp = client.post(f"{base_url}/diagnostico", json=payload)
            print(f"Status HTTP: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"Status diagnostico: {data.get(str(chr(115)+chr(116)+chr(97)+chr(116)+chr(117)+chr(115)))}")
                print(f"Tempo ms: {data.get(str(chr(116)+chr(101)+chr(109)+chr(112)+chr(111)+chr(95)+chr(109)+chr(115)))}")
                print("TESTE 2: PASSOU")
            else:
                print(f"Erro: {resp.text[:500]}")
                print("TESTE 2: FALHOU")
    except Exception as e:
        print(f"API nao disponivel: {e}")
        print("Inicie com: uvicorn app.main:app --reload")
        print("TESTE 2: PULADO")


def teste_edge_cases():
    """Teste 3: casos de borda."""
    print("=" * 60)
    print("TESTE 3 - Casos de borda")
    print("=" * 60)

    from langchain_core.messages import HumanMessage
    from app.agent.factory import create_diagnostico_agent

    agent = create_diagnostico_agent()

    print("--- Caso 3a: XML malformado ---")
    sep = chr(10)
    msg_invalido = (
        "Diagnostique esta rejeicao:" + sep
        + "Erro: E001" + sep
        + "XML: isso nao eh xml valido"
    )
    result = agent.invoke({"messages": [HumanMessage(content=msg_invalido)]})
    structured = result.get("structured_response")
    if structured:
        print(f"Status: {structured.status}")
        print("Caso 3a: OK")
    else:
        print("Caso 3a: sem structured_response")
    print("")


def main():
    parser = argparse.ArgumentParser(description="Testes do agente de diagnostico")
    parser.add_argument("--direto", action="store_true")
    parser.add_argument("--api", action="store_true")
    parser.add_argument("--edge", action="store_true")
    parser.add_argument("--todos", action="store_true")
    args = parser.parse_args()

    if not any([args.direto, args.api, args.edge, args.todos]):
        parser.print_help()
        sys.exit(1)

    if args.direto or args.todos:
        teste_direto_agente()

    if args.api or args.todos:
        teste_api_http()

    if args.edge or args.todos:
        teste_edge_cases()


if __name__ == "__main__":
    main()
