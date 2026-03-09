"""Script para ingestao de todos os dados no PGVectorStore.

Uso:
    python -m scripts.ingest_data --all
    python -m scripts.ingest_data --catalogo
    python -m scripts.ingest_data --regras
    python -m scripts.ingest_data --xmls
"""

import argparse
import logging
import sys
from pathlib import Path

# Adicionar raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.vectorstore.ingest import (
    ingest_catalogo,
    ingest_regras,
    ingest_xmls_autorizados,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Executa ingestao de dados conforme argumentos CLI."""
    parser = argparse.ArgumentParser(description="Ingestao de dados no PGVectorStore")
    parser.add_argument("--catalogo", action="store_true", help="Ingerir catalogo de erros")
    parser.add_argument("--regras", action="store_true", help="Ingerir regras de negocio")
    parser.add_argument("--xmls", action="store_true", help="Ingerir XMLs autorizados")
    parser.add_argument("--all", action="store_true", help="Ingerir todos os dados")
    parser.add_argument("--reindex-xmls", action="store_true", help="Re-ingerir apenas XMLs autorizados (com codigo_servico corrigido)")
    args = parser.parse_args()

    if not any([args.catalogo, args.regras, args.xmls, getattr(args, "reindex_xmls", False), args.all]):
        parser.print_help()
        sys.exit(1)

    total = 0

    if args.catalogo or args.all:
        catalogo_path = DATA_DIR / "catalogo_enriquecido.json"
        if not catalogo_path.exists():
            logger.error("Arquivo nao encontrado: %s", catalogo_path)
            sys.exit(1)
        try:
            count = ingest_catalogo(str(catalogo_path))
            total += count
        except Exception as e:
            logger.error("Erro ao ingerir catalogo: %s", e)
            sys.exit(1)

    if args.regras or args.all:
        regras_path = DATA_DIR / "regras_negocio.md"
        if not regras_path.exists():
            logger.error("Arquivo nao encontrado: %s", regras_path)
            sys.exit(1)
        try:
            count = ingest_regras(str(regras_path))
            total += count
        except Exception as e:
            logger.error("Erro ao ingerir regras: %s", e)
            sys.exit(1)

    if args.xmls or args.all or getattr(args, "reindex_xmls", False):
        xmls_path = DATA_DIR / "xmls_autorizados"
        if not xmls_path.exists():
            logger.error("Diretorio nao encontrado: %s", xmls_path)
            sys.exit(1)
        try:
            count = ingest_xmls_autorizados(str(xmls_path))
            total += count
        except Exception as e:
            logger.error("Erro ao ingerir XMLs: %s", e)
            sys.exit(1)

    print(f"\n=== Ingestao concluida: {total} documentos no total ===")


if __name__ == "__main__":
    main()
