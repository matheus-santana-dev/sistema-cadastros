import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "pessoas.json"


def carregar_pessoas():
    """Carrega os cadastros sem esconder arquivos JSON corrompidos."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise RuntimeError(
            f"O arquivo de cadastros está inválido: {DATA_FILE}. "
            "Não foi criado um arquivo vazio para evitar sobrescrever seus dados. "
            "Faça uma cópia do arquivo antes de tentar recuperá-lo."
        ) from erro
    except OSError as erro:
        raise RuntimeError(f"Não foi possível ler os cadastros: {erro}") from erro

    if not isinstance(dados, list):
        raise RuntimeError(
            f"O conteúdo de {DATA_FILE.name} não está no formato esperado (lista JSON)."
        )

    if not all(isinstance(pessoa, dict) for pessoa in dados):
        raise RuntimeError(
            f"O arquivo {DATA_FILE.name} contém registros inválidos. "
            "Os dados não foram alterados."
        )

    return [dict(pessoa) for pessoa in dados]


def salvar_pessoas(pessoas):
    """Salva os cadastros com substituição atômica para reduzir risco de corrupção."""
    if not isinstance(pessoas, list) or not all(isinstance(p, dict) for p in pessoas):
        raise ValueError("Os cadastros precisam ser informados em uma lista de registros.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    arquivo_temporario = DATA_FILE.with_name(DATA_FILE.name + ".tmp")

    try:
        with arquivo_temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(pessoas, arquivo, ensure_ascii=False, indent=4)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(arquivo_temporario, DATA_FILE)
    except OSError:
        try:
            arquivo_temporario.unlink(missing_ok=True)
        except OSError:
            pass
        raise
