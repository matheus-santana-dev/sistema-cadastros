from datetime import date, datetime

from .database import carregar_pessoas, salvar_pessoas


def _normalizar_data_nascimento(valor):
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if valor is None:
        return None

    texto = str(valor).strip()
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ValueError("Data de nascimento inválida. Use DD/MM/AAAA.")


def _calcular_idade(nascimento):
    hoje = date.today()
    return hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )


class CadastroService:
    def __init__(self):
        self.pessoas = carregar_pessoas()
        self._sincronizar_idades()

    def _salvar(self):
        salvar_pessoas(self.pessoas)

    def _sincronizar_idades(self):
        """Mantém a idade persistida coerente com a data de nascimento."""
        alterou = False
        for pessoa in self.pessoas:
            valor = pessoa.get("data_nascimento")
            if not valor:
                continue
            try:
                nascimento = _normalizar_data_nascimento(valor)
            except ValueError:
                continue
            if nascimento > date.today():
                continue

            idade_atual = _calcular_idade(nascimento)
            if pessoa.get("idade") != idade_atual:
                pessoa["idade"] = idade_atual
                alterou = True

            pessoa["data_nascimento"] = nascimento.isoformat()

        if alterou:
            self._salvar()

    def listar(self):
        # Retorna cópias para impedir alterações externas sem persistência.
        return [dict(pessoa) for pessoa in self.pessoas]

    def adicionar(self, nome, idade, sexo, data_nascimento=None):
        nome_normalizado = str(nome).strip().upper()
        if not nome_normalizado:
            raise ValueError("O nome é obrigatório.")
        if sexo not in {"M", "F"}:
            raise ValueError("Sexo inválido. Use M ou F.")

        nascimento = _normalizar_data_nascimento(data_nascimento)
        if nascimento:
            if nascimento > date.today():
                raise ValueError("A data de nascimento não pode estar no futuro.")
            idade_final = _calcular_idade(nascimento)
        else:
            idade_final = int(idade)
            if idade_final < 0:
                raise ValueError("A idade não pode ser negativa.")

        ids = []
        for pessoa in self.pessoas:
            try:
                ids.append(int(pessoa.get("id", 0)))
            except (TypeError, ValueError):
                continue
        novo_id = max(ids, default=0) + 1

        pessoa = {
            "id": novo_id,
            "nome": nome_normalizado,
            "idade": idade_final,
            "sexo": sexo,
        }
        if nascimento:
            pessoa["data_nascimento"] = nascimento.isoformat()

        self.pessoas.append(pessoa)
        try:
            self._salvar()
        except Exception:
            self.pessoas.pop()
            raise
        return dict(pessoa)

    def atualizar(self, pessoa_id, nome, idade, sexo, data_nascimento=None):
        nome_normalizado = str(nome).strip().upper()
        if not nome_normalizado:
            raise ValueError("O nome é obrigatório.")
        if sexo not in {"M", "F"}:
            raise ValueError("Sexo inválido. Use M ou F.")

        nascimento = _normalizar_data_nascimento(data_nascimento)
        for pessoa in self.pessoas:
            if pessoa.get("id") == pessoa_id:
                anterior = dict(pessoa)
                pessoa["nome"] = nome_normalizado
                pessoa["sexo"] = sexo

                if nascimento is not None:
                    if nascimento > date.today():
                        pessoa.clear()
                        pessoa.update(anterior)
                        raise ValueError("A data de nascimento não pode estar no futuro.")
                    pessoa["data_nascimento"] = nascimento.isoformat()
                    pessoa["idade"] = _calcular_idade(nascimento)
                elif pessoa.get("data_nascimento"):
                    # Não apaga a data de nascimento em atualizações antigas de quatro argumentos.
                    nascimento_salvo = _normalizar_data_nascimento(pessoa["data_nascimento"])
                    pessoa["idade"] = _calcular_idade(nascimento_salvo)
                else:
                    pessoa["idade"] = int(idade)
                    if pessoa["idade"] < 0:
                        pessoa.clear()
                        pessoa.update(anterior)
                        raise ValueError("A idade não pode ser negativa.")

                try:
                    self._salvar()
                except Exception:
                    pessoa.clear()
                    pessoa.update(anterior)
                    raise
                return dict(pessoa)

        return None

    def excluir(self, pessoa_id):
        for indice, pessoa in enumerate(self.pessoas):
            if pessoa.get("id") == pessoa_id:
                removida = self.pessoas.pop(indice)
                try:
                    self._salvar()
                except Exception:
                    self.pessoas.insert(indice, removida)
                    raise
                return True
        return False

    def estatisticas(self):
        pessoas = self.listar()
        idades = []
        for pessoa in pessoas:
            try:
                idade = int(pessoa.get("idade", 0))
            except (TypeError, ValueError):
                idade = 0
            idades.append((pessoa, idade))

        total = len(pessoas)
        homens = sum(1 for pessoa in pessoas if pessoa.get("sexo") == "M")
        mulheres = sum(1 for pessoa in pessoas if pessoa.get("sexo") == "F")
        maiores = sum(1 for _, idade in idades if idade >= 18)
        menores = sum(1 for _, idade in idades if idade < 18)
        idosos = sum(1 for _, idade in idades if idade >= 60)
        mais_velha = max(idades, key=lambda item: item[1], default=(None, 0))[0]
        mais_nova = min(idades, key=lambda item: item[1], default=(None, 0))[0]

        return {
            "total": total,
            "homens": homens,
            "mulheres": mulheres,
            "maiores": maiores,
            "menores": menores,
            "idosos": idosos,
            "mais_velha": mais_velha,
            "mais_nova": mais_nova,
        }
