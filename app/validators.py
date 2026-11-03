import re
from datetime import date, datetime


# Aceita nomes com acentos, espaços, hífens e apóstrofos.
_PADRAO_NOME = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[ '\u2019-][A-Za-zÀ-ÖØ-öø-ÿ]+)*"
)


def validar_nome(nome):
    if not isinstance(nome, str):
        return False, "O nome deve ser informado como texto."

    nome = nome.strip()

    if not nome:
        return False, "O nome é obrigatório."

    if len(nome) < 2:
        return False, "O nome deve ter pelo menos 2 caracteres."

    if len(nome) > 80:
        return False, "O nome deve ter no máximo 80 caracteres."

    if not _PADRAO_NOME.fullmatch(nome):
        return False, "O nome deve conter apenas letras, espaços, hífens ou apóstrofos."

    return True, ""


def validar_idade(idade):
    try:
        idade = int(str(idade).strip())
    except (TypeError, ValueError):
        return False, "A idade deve ser um número inteiro."

    if idade < 1 or idade >= 130:
        return False, "Informe uma idade entre 1 e 129 anos."

    return True, ""


def normalizar_sexo(sexo):
    if not isinstance(sexo, str):
        return None

    valor = sexo.strip().upper()

    if valor in ("M", "MASCULINO"):
        return "M"

    if valor in ("F", "FEMININO"):
        return "F"

    return None


def validar_sexo(sexo):
    if normalizar_sexo(sexo) is None:
        return False, "Selecione Masculino ou Feminino."

    return True, ""


def validar_data_nascimento(data_nascimento):
    """Aceita DD/MM/AAAA (tela) ou AAAA-MM-DD (armazenamento)."""
    if not isinstance(data_nascimento, str):
        return False, "A data de nascimento deve ser informada como texto."

    valor = data_nascimento.strip()
    if not valor:
        return False, "A data de nascimento é obrigatória."

    data = None
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            data = datetime.strptime(valor, formato).date()
            break
        except ValueError:
            continue

    if data is None:
        return False, "Informe uma data válida no formato DD/MM/AAAA."

    if data > date.today():
        return False, "A data de nascimento não pode ser futura."

    return True, ""
