# Sistema de Cadastros

Aplicativo desktop para gerenciamento de pessoas, desenvolvido em **Python** com **CustomTkinter**. O sistema reúne cadastro, consulta, organização e análise de informações em uma interface gráfica moderna com tema escuro.

## Funcionalidades

### Cadastro e gerenciamento de pessoas
- Cadastro de pessoas com nome, data de nascimento e sexo.
- Cálculo automático da idade com base na data de nascimento.
- Atualização da idade conforme a passagem do tempo.
- Edição e exclusão de cadastros.
- Exclusão de todos os cadastros com confirmação.
- Pesquisa por nome.
- Filtros por sexo e faixa etária.
- Ordenação por data de cadastro, nome e idade.
- Paginação para organizar a exibição dos registros.

### Dashboard
- Indicadores de pessoas cadastradas, homens, mulheres, maiores de idade, menores de idade e pessoas com 60 anos ou mais.
- Gráfico de rosca com a proporção por sexo.
- Gráfico de rosca com a proporção por faixa etária.
- Exibição de quantidade e percentual nas legendas dos gráficos.
- Destaques para a pessoa mais velha e a pessoa mais nova.
- Atualização dos indicadores e gráficos conforme os dados dos cadastros.

### Relatórios e exportação
- Relação detalhada dos cadastros, incluindo ID, nome, idade, sexo e data de nascimento.
- Paginação dos registros.
- Exportação dos dados para **CSV**, **Excel (.xlsx)** e **PDF**.

### Importação, backup e recuperação
- Importação de cadastros a partir de arquivos **CSV** e **Excel (.xlsx/.xlsm)**.
- Validação dos dados durante a importação.
- Criação de backup dos cadastros e dos registros da lixeira em arquivo JSON.
- Restauração dos dados a partir de um backup.
- Lixeira para consultar e restaurar cadastros excluídos.
- Exclusão permanente de registros e opção para esvaziar a lixeira.

### Histórico e configurações
- Histórico de atividades com data e horário.
- Opção para limpar o histórico.
- Interface disponível em **português, inglês e espanhol**.
- Preferência de idioma salva localmente.

## Tecnologias utilizadas

- **Python 3.10+** — linguagem principal.
- **CustomTkinter** — interface gráfica desktop.
- **Matplotlib** — gráficos de rosca do Dashboard.
- **OpenPyXL** — leitura e geração de arquivos Excel.
- **ReportLab** — geração de relatórios em PDF.
- **JSON** — persistência local dos cadastros e dados auxiliares.
- **CSV** — importação e exportação de dados.

O projeto também utiliza recursos da biblioteca padrão do Python, como `json`, `csv`, `datetime` e `pathlib`.

## Requisitos

- Python 3.10 ou superior.
- Pip.

## Como executar

1. Baixe ou clone o repositório.
2. Abra o terminal na pasta `sistema_cadastros`, onde está localizado o arquivo `main.py`.
3. Crie um ambiente virtual (opcional, recomendado):

   ```bash
   python -m venv .venv
   ```

4. Ative o ambiente virtual no Windows:

   ```powershell
   .venv\Scripts\activate
   ```

5. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Inicie o sistema:

   ```bash
   python main.py
   ```

## Dependências

O arquivo `requirements.txt` contém:

```text
customtkinter>=5.2.2
openpyxl
reportlab
matplotlib>=3.8.0
```

## Armazenamento dos dados

Os cadastros são armazenados localmente em arquivos JSON. O banco principal fica em `data/pessoas.json`.

O sistema também utiliza arquivos auxiliares locais para informações como histórico de atividades, configurações e lixeira. Esses arquivos são criados ou atualizados durante o uso do programa.

Os backups são gerados em formato JSON no local escolhido pelo usuário durante a operação.

> **Observação:** os registros utilizados para demonstração do projeto são fictícios. Recomenda-se manter cópias de segurança da pasta `data` e dos arquivos JSON auxiliares antes de alterações importantes.

## Estrutura do projeto

```text
sistema_cadastros/
├── app/
│   ├── database.py
│   ├── validators.py
│   ├── services.py
│   └── ui.py
├── data/
│   └── pessoas.json
├── main.py
├── requirements.txt
└── README.md
```

Os arquivos JSON auxiliares são criados ou utilizados pelo sistema durante a execução.

## Objetivo do projeto

Projeto desenvolvido para praticar e demonstrar conceitos de desenvolvimento com Python, incluindo:

- Organização de código em módulos.
- Construção de interfaces gráficas com CustomTkinter.
- Operações CRUD (criar, consultar, atualizar e excluir).
- Validação de dados e tratamento de exceções.
- Manipulação de datas e cálculo automático de idade.
- Persistência local com JSON.
- Importação e exportação de arquivos.
- Geração de relatórios e visualização de dados.
- Backup, restauração e recuperação de registros.

## Autor

**Matheus Santana Costa Leite**

- GitHub: [matheus-santana-dev](https://github.com/matheus-santana-dev)