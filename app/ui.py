import csv
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
import unicodedata
from uuid import uuid4

import customtkinter as ctk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .services import CadastroService
from .validators import validar_nome, validar_idade, validar_sexo


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# ----------------------------
# PALETA DE CORES
# Preto, cinza e verde
# ----------------------------

# Fundos
COR_FUNDO = "#080808"
COR_SIDEBAR = "#101010"
COR_CARD = "#181818"
COR_ITEM = "#222222"
COR_BORDA = "#303030"

# Destaque (verde)
COR_DESTAQUE = "#22c55e"
COR_DESTAQUE_HOVER = "#16a34a"
COR_TEXTO_NO_DESTAQUE = "#080808"

# Textos
COR_TEXTO = "#f5f5f5"
COR_TEXTO_CORPO = "#d4d4d4"
COR_TEXTO_MENU = "#e5e5e5"
COR_TEXTO_SEC = "#a3a3a3"
COR_TEXTO_MUDO = "#737373"

# Menu lateral
COR_MENU_HOVER = "#262626"
COR_MENU_ATIVO = "#292929"

# Botões
COR_BOTAO_NEUTRO = "#303030"
COR_BOTAO_NEUTRO_HOVER = "#404040"
COR_BOTAO_SEC = "#383838"
COR_BOTAO_SEC_HOVER = "#484848"
COR_BOTAO_VERDE = "#22c55e"
COR_BOTAO_VERDE_HOVER = "#16a34a"
COR_PERIGO = "#8f2932"
COR_PERIGO_HOVER = "#a8323d"

# Avisos (mensagens no canto)
COR_SUCESSO = "#22c55e"
COR_AVISO = "#facc15"
COR_ERRO = "#ef4444"

TEMPO_AVISO_MS = 3000


# Traduções da interface. Os valores internos do banco permanecem os mesmos;
# somente os textos exibidos ao usuário são alterados.
TRADUCOES = {
    "English": {
        "CADASTROS": "PEOPLE",
        "Sistema de Cadastros": "Registration System",
        "Sistema de gerenciamento": "Management system",
        "Dashboard": "Dashboard",
        "Cadastros": "People",
        "Relatórios": "Reports",
        "Histórico": "Activity history",
        "Configurações": "Settings",
        "Visão geral e indicadores dos cadastros": "Overview and registration statistics",
        "Pessoas cadastradas": "Registered people",
        "Homens": "Men",
        "Mulheres": "Women",
        "Maiores de idade": "Adults (18+)",
        "Menores de idade": "Minors (under 18)",
        "60 anos ou mais": "60 years or older",
        "Distribuição por sexo": "Distribution by gender",
        "Proporção por sexo": "Gender proportion",
        "Proporção por faixa etária": "Age group proportion",
        "Quantidade:": "Quantity:",
        "Pessoas": "People",
        "Distribuição por faixa etária": "Distribution by age group",
        "Menores de 18": "Under 18",
        "18 a 59 anos": "18 to 59 years",
        "Menor de 18": "Under 18",
        "18 ou mais": "18 or older",
        "60 ou mais": "60 or older",
        "Nome": "Name",
        "Sexo": "Gender",
        "▣  Dashboard": "▣  Dashboard",
        "☷  Cadastros": "☷  People",
        "▤  Relatórios": "▤  Reports",
        "⟲  Histórico": "⟲  Activity history",
        "⛭  Configurações": "⛭  Settings",
        "Pessoa mais velha": "Oldest person",
        "Pessoa mais nova": "Youngest person",
        "Nenhum cadastro": "No registrations",
        "anos": "years",
        "Novo cadastro": "New registration",
        "Adicione, pesquise, edite ou remova pessoas": "Add, search, edit, or remove people",
        "Nome completo": "Full name",
        "Idade": "Age",
        "Masculino": "Male",
        "Feminino": "Female",
        "Cadastrar pessoa": "Add person",
        "Limpar formulário": "Clear form",
        "AÇÕES ADMINISTRATIVAS": "ADMINISTRATIVE ACTIONS",
        "Ferramentas de dados": "Data tools",
        "Excluir todos os cadastros": "Delete all registrations",
        "Modo: novo cadastro": "Mode: new registration",
        "Pesquisar por nome...": "Search by name...",
        "Sexo: Todos": "Gender: All",
        "Sexo: Masculino": "Gender: Male",
        "Sexo: Feminino": "Gender: Female",
        "Idade: Todas": "Age: All",
        "Idade: Menor de 18": "Age: Under 18",
        "Idade: 18 ou mais": "Age: 18 or older",
        "Idade: 60 ou mais": "Age: 60 or older",
        "Ordenar: Padrão": "Sort: Default",
        "Ordenar: Mais recentes": "Sort: Newest",
        "Ordenar: Nome A-Z": "Sort: Name A-Z",
        "Ordenar: Nome Z-A": "Sort: Name Z-A",
        "Ordenar: Menor idade": "Sort: Youngest first",
        "Ordenar: Maior idade": "Sort: Oldest first",
        "← Anterior": "← Previous",
        "Próxima →": "Next →",
        "Nenhum cadastro encontrado.": "No registrations found.",
        "Editar": "Edit",
        "Excluir": "Delete",
        "Excluir?": "Delete?",
        "Sim": "Yes",
        "Não": "No",
        "Salvar alterações": "Save changes",
        "Modo: editando cadastro #": "Mode: editing registration #",
        "Nome inválido": "Invalid name",
        "Idade inválida": "Invalid age",
        "Sexo inválido": "Invalid gender",
        "Pessoa cadastrada com sucesso!": "Person added successfully!",
        "Cadastro atualizado com sucesso!": "Registration updated successfully!",
        "Cadastro de ": "Registration for ",
        " excluído.": " deleted.",
        "Não há cadastros para excluir.": "There are no registrations to delete.",
        "Excluir todos os cadastros?": "Delete all registrations?",
        "Você está prestes a excluir ": "You are about to delete ",
        " cadastro(s).\nEssa ação não poderá ser desfeita.": " registration(s).\nThis action cannot be undone.",
        "Cancelar": "Cancel",
        "Sim, excluir todos": "Yes, delete all",
        "Ocorreu um erro durante a exclusão. Confira os cadastros restantes.": "An error occurred while deleting. Check the remaining registrations.",
        "Não foi possível concluir": "Unable to complete",
        " cadastro(s) excluído(s) com sucesso!": " registration(s) deleted successfully!",
        "Relatórios": "Reports",
        "Consulte a relação completa de pessoas e exporte os dados": "View the full list of people and export the data",
        " cadastro(s) encontrados": " registration(s) found",
        "Exportar CSV": "Export CSV",
        "Exportar Excel": "Export Excel",
        "Exportar PDF": "Export PDF",
        "Relação detalhada de cadastros": "Detailed registration list",
        "Nenhum cadastro disponível para exibir.": "No registrations available to display.",
        "Salvar relatório de cadastros": "Save registrations report",
        "Salvar relatório em Excel": "Save report as Excel",
        "Salvar relatório em PDF": "Save report as PDF",
        "Arquivo CSV": "CSV file",
        "Planilha Excel": "Excel workbook",
        "Arquivo PDF": "PDF file",
        "Não há cadastros para exportar.": "There are no registrations to export.",
        "Falha na exportação": "Export failed",
        "Exportação concluída": "Export completed",
        "Biblioteca necessária": "Required library",
        "Para exportar Excel, instale a dependência: python -m pip install openpyxl": "To export Excel, install the dependency: python -m pip install openpyxl",
        "Para exportar PDF, instale a dependência: python -m pip install reportlab": "To export PDF, install the dependency: python -m pip install reportlab",
        "Histórico de atividades": "Activity history",
        "Acompanhe os cadastros, alterações, exclusões e exportações": "Track registrations, changes, deletions, and exports",
        "Limpar histórico": "Clear history",
        "Deseja apagar todo o histórico?": "Do you want to clear the entire history?",
        "Essa ação não poderá ser desfeita.": "This action cannot be undone.",
        "Sim, limpar histórico": "Yes, clear history",
        "Histórico apagado com sucesso.": "History cleared successfully.",
        "Não há atividades para limpar.": "There are no activities to clear.",
        "Atividade": "Activity",
        "Nenhuma atividade registrada ainda.": "No activity has been recorded yet.",
        "Configurações": "Settings",
        "Ajuste algumas preferências de visualização do sistema": "Adjust the system language preference",
        "Idioma": "Language",
        "Escolha o idioma da interface.": "Choose the interface language.",
        "Aplicar idioma": "Apply language",
        "Idioma atualizado com sucesso!": "Language updated successfully!",
        "Não foi possível salvar as configurações: ": "Could not save settings: ",
        "Selecione um idioma válido.": "Select a valid language.",
        "Falha ao salvar": "Save failed",
        "A ação foi concluída, mas não foi possível salvar o histórico no disco.": "The action was completed, but the activity history could not be saved to disk.",
        "Histórico não salvo": "History not saved",
        "Cadastro criado": "Registration created",
        "Cadastro atualizado": "Registration updated",
        "Cadastro excluído": "Registration deleted",
        "Exclusão em massa": "Bulk deletion",
        "Relatório CSV exportado": "CSV report exported",
        "Relatório Excel exportado": "Excel report exported",
        "Relatório PDF exportado": "PDF report exported",
        "Idioma alterado": "Language changed",
        "Configurações atualizadas": "Settings updated",
        "Salvar configurações": "Save settings",
        "Total de registros: ": "Total records: ",
        "Relatório de Cadastros": "Registration Report",
        "ID": "ID", "NOME": "NAME", "IDADE": "AGE", "SEXO": "GENDER",
    },
    "Español": {
        "CADASTROS": "REGISTROS",
        "Sistema de Cadastros": "Sistema de registros",
        "Sistema de gerenciamento": "Sistema de gestión",
        "Dashboard": "Panel principal",
        "Cadastros": "Registros",
        "Relatórios": "Informes",
        "Histórico": "Historial",
        "Configurações": "Configuración",
        "Visão geral e indicadores dos cadastros": "Resumen e indicadores de los registros",
        "Pessoas cadastradas": "Personas registradas",
        "Homens": "Hombres",
        "Mulheres": "Mujeres",
        "Maiores de idade": "Mayores de edad",
        "Menores de idade": "Menores de edad",
        "60 anos ou mais": "60 años o más",
        "Distribuição por sexo": "Distribución por sexo",
        "Proporção por sexo": "Proporción por sexo",
        "Proporção por faixa etária": "Proporción por grupo de edad",
        "Quantidade:": "Cantidad:",
        "Pessoas": "Personas",
        "Distribuição por faixa etária": "Distribución por grupo de edad",
        "Menores de 18": "Menores de 18",
        "18 a 59 anos": "De 18 a 59 años",
        "Menor de 18": "Menor de 18",
        "18 ou mais": "18 o más",
        "60 ou mais": "60 o más",
        "Nome": "Nombre",
        "Sexo": "Sexo",
        "▣  Dashboard": "▣  Panel principal",
        "☷  Cadastros": "☷  Registros",
        "▤  Relatórios": "▤  Informes",
        "⟲  Histórico": "⟲  Historial",
        "⛭  Configurações": "⛭  Configuración",
        "Pessoa mais velha": "Persona de mayor edad",
        "Pessoa mais nova": "Persona más joven",
        "Nenhum cadastro": "Ningún registro",
        "anos": "años",
        "Novo cadastro": "Nuevo registro",
        "Adicione, pesquise, edite ou remova pessoas": "Agregue, busque, edite o elimine personas",
        "Nome completo": "Nombre completo",
        "Idade": "Edad",
        "Masculino": "Masculino",
        "Feminino": "Femenino",
        "Cadastrar pessoa": "Registrar persona",
        "Limpar formulário": "Limpiar formulario",
        "AÇÕES ADMINISTRATIVAS": "ACCIONES ADMINISTRATIVAS",
        "Ferramentas de dados": "Herramientas de datos",
        "Excluir todos os cadastros": "Eliminar todos los registros",
        "Modo: novo cadastro": "Modo: nuevo registro",
        "Pesquisar por nome...": "Buscar por nombre...",
        "Sexo: Todos": "Sexo: Todos",
        "Sexo: Masculino": "Sexo: Masculino",
        "Sexo: Feminino": "Sexo: Femenino",
        "Idade: Todas": "Edad: Todas",
        "Idade: Menor de 18": "Edad: Menor de 18",
        "Idade: 18 ou mais": "Edad: 18 o más",
        "Idade: 60 ou mais": "Edad: 60 o más",
        "Ordenar: Padrão": "Ordenar: Predeterminado",
        "Ordenar: Mais recentes": "Ordenar: Más recientes",
        "Ordenar: Nome A-Z": "Ordenar: Nombre A-Z",
        "Ordenar: Nome Z-A": "Ordenar: Nombre Z-A",
        "Ordenar: Menor idade": "Ordenar: Menor edad",
        "Ordenar: Maior idade": "Ordenar: Mayor edad",
        "← Anterior": "← Anterior",
        "Próxima →": "Siguiente →",
        "Nenhum cadastro encontrado.": "No se encontraron registros.",
        "Editar": "Editar",
        "Excluir": "Eliminar",
        "Excluir?": "¿Eliminar?",
        "Sim": "Sí",
        "Não": "No",
        "Salvar alterações": "Guardar cambios",
        "Modo: editando cadastro #": "Modo: editando registro #",
        "Nome inválido": "Nombre no válido",
        "Idade inválida": "Edad no válida",
        "Sexo inválido": "Sexo no válido",
        "Pessoa cadastrada com sucesso!": "¡Persona registrada correctamente!",
        "Cadastro atualizado com sucesso!": "¡Registro actualizado correctamente!",
        "Cadastro de ": "Registro de ",
        " excluído.": " eliminado.",
        "Não há cadastros para excluir.": "No hay registros para eliminar.",
        "Excluir todos os cadastros?": "¿Eliminar todos los registros?",
        "Você está prestes a excluir ": "Está a punto de eliminar ",
        " cadastro(s).\nEssa ação não poderá ser desfeita.": " registro(s).\nEsta acción no se puede deshacer.",
        "Cancelar": "Cancelar",
        "Sim, excluir todos": "Sí, eliminar todos",
        "Ocorreu um erro durante a exclusão. Confira os cadastros restantes.": "Ocurrió un error durante la eliminación. Revise los registros restantes.",
        "Não foi possível concluir": "No se pudo completar",
        " cadastro(s) excluído(s) com sucesso!": " registro(s) eliminado(s) correctamente!",
        "Consulte a relação completa de pessoas e exporte os dados": "Consulte la lista completa de personas y exporte los datos",
        " cadastro(s) encontrados": " registro(s) encontrados",
        "Exportar CSV": "Exportar CSV",
        "Exportar Excel": "Exportar Excel",
        "Exportar PDF": "Exportar PDF",
        "Relação detalhada de cadastros": "Lista detallada de registros",
        "Nenhum cadastro disponível para exibir.": "No hay registros disponibles para mostrar.",
        "Salvar relatório de cadastros": "Guardar informe de registros",
        "Salvar relatório em Excel": "Guardar informe en Excel",
        "Salvar relatório em PDF": "Guardar informe en PDF",
        "Arquivo CSV": "Archivo CSV",
        "Planilha Excel": "Hoja de Excel",
        "Arquivo PDF": "Archivo PDF",
        "Não há cadastros para exportar.": "No hay registros para exportar.",
        "Falha na exportação": "Error de exportación",
        "Exportação concluída": "Exportación completada",
        "Biblioteca necessária": "Biblioteca necesaria",
        "Para exportar Excel, instale a dependência: python -m pip install openpyxl": "Para exportar a Excel, instale la dependencia: python -m pip install openpyxl",
        "Para exportar PDF, instale a dependência: python -m pip install reportlab": "Para exportar a PDF, instale la dependencia: python -m pip install reportlab",
        "Histórico de atividades": "Historial de actividad",
        "Limpar histórico": "Borrar historial",
        "Deseja apagar todo o histórico?": "¿Desea borrar todo el historial?",
        "Essa ação não poderá ser desfeita.": "Esta acción no se puede deshacer.",
        "Sim, limpar histórico": "Sí, borrar historial",
        "Histórico apagado com sucesso.": "Historial borrado correctamente.",
        "Não há atividades para limpar.": "No hay actividades para borrar.",
        "Acompanhe os cadastros, alterações, exclusões e exportações": "Consulte los registros, cambios, eliminaciones y exportaciones",
        "Atividade": "Actividad",
        "Nenhuma atividade registrada ainda.": "Todavía no hay actividades registradas.",
        "Ajuste algumas preferências de visualização do sistema": "Ajuste el idioma de la interfaz",
        "Idioma": "Idioma",
        "Escolha o idioma da interface.": "Elija el idioma de la interfaz.",
        "Aplicar idioma": "Aplicar idioma",
        "Idioma atualizado com sucesso!": "¡Idioma actualizado correctamente!",
        "Não foi possível salvar as configurações: ": "No se pudo guardar la configuración: ",
        "Selecione um idioma válido.": "Seleccione un idioma válido.",
        "Falha ao salvar": "Error al guardar",
        "A ação foi concluída, mas não foi possível salvar o histórico no disco.": "La acción se completó, pero no fue posible guardar el historial en el disco.",
        "Histórico não salvo": "Historial no guardado",
        "Cadastro criado": "Registro creado",
        "Cadastro atualizado": "Registro actualizado",
        "Cadastro excluído": "Registro eliminado",
        "Exclusão em massa": "Eliminación masiva",
        "Relatório CSV exportado": "Informe CSV exportado",
        "Relatório Excel exportado": "Informe Excel exportado",
        "Relatório PDF exportado": "Informe PDF exportado",
        "Idioma alterado": "Idioma cambiado",
        "Configurações atualizadas": "Configuración actualizada",
        "Total de registros: ": "Total de registros: ",
        "Relatório de Cadastros": "Informe de registros",
        "ID": "ID", "NOME": "NOMBRE", "IDADE": "EDAD", "SEXO": "SEXO",
    },
}


TRADUCOES["English"].update({
    "DD/MM/AAAA": "DD/MM/YYYY",
    "▧  Lixeira": "▧  Recycle bin",
    "Importar Excel/CSV": "Import Excel/CSV",
    "Fazer backup": "Create backup",
    "Restaurar backup": "Restore backup",
    "Data de nascimento (DD/MM/AAAA)": "Date of birth (DD/MM/YYYY)",
    "Data de nascimento": "Date of birth",
    "Nascimento não informado": "Date of birth not provided",
    "Data de nascimento inválida. Use DD/MM/AAAA.": "Invalid date of birth. Use DD/MM/YYYY.",
    "A data de nascimento não pode estar no futuro.": "Date of birth cannot be in the future.",
    "A data de nascimento é obrigatória.": "Date of birth is required.",
    "Importar cadastros": "Import registrations",
    "Selecione um arquivo Excel ou CSV": "Select an Excel or CSV file",
    "Arquivo CSV ou Excel": "CSV or Excel file",
    "Importação concluída": "Import completed",
    "Importados: ": "Imported: ",
    "Ignorados: ": "Skipped: ",
    "O arquivo precisa conter as colunas Nome, Data de nascimento e Sexo.": "The file must contain Name, Date of birth, and Gender columns.",
    "Nenhum registro válido foi encontrado no arquivo.": "No valid records were found in the file.",
    "Lixeira": "Recycle bin",
    "Cadastros excluídos ficam disponíveis aqui para restauração ou exclusão permanente.": "Deleted registrations are available here for restoration or permanent deletion.",
    "Restaurar": "Restore",
    "Excluir permanentemente": "Delete permanently",
    "Esvaziar lixeira": "Empty recycle bin",
    "A lixeira está vazia.": "The recycle bin is empty.",
    "Deseja restaurar este cadastro?": "Do you want to restore this registration?",
    "Cadastro restaurado com sucesso.": "Registration restored successfully.",
    "Cadastro removido permanentemente.": "Registration permanently deleted.",
    "Deseja esvaziar a lixeira?": "Do you want to empty the recycle bin?",
    "Lixeira esvaziada com sucesso.": "Recycle bin emptied successfully.",
    "Fazer backup dos cadastros": "Back up registrations",
    "Backup criado com sucesso.": "Backup created successfully.",
    "Selecione o arquivo de backup": "Select the backup file",
    "Arquivo de backup inválido ou incompatível.": "Invalid or incompatible backup file.",
    "Restaurar backup?": "Restore backup?",
    "Os cadastros atuais serão substituídos pelos dados do backup.\nEssa ação não poderá ser desfeita.": "Current registrations will be replaced with backup data.\nThis action cannot be undone.",
    "Backup restaurado com sucesso.": "Backup restored successfully.",
    "Falha ao restaurar backup": "Failed to restore backup",
    "Data de nascimento: ": "Date of birth: ",
    "Exportação de cadastros": "Registration export",
    "Cadastro importado": "Registration imported",
    "Backup criado": "Backup created",
    "Backup restaurado": "Backup restored",
    "Cadastro restaurado": "Registration restored",
    "Cadastro excluído permanentemente": "Registration permanently deleted",
    "Importação de cadastros": "Registrations imported",
    "Cadastro movido para a lixeira": "Registration moved to recycle bin",
    "Lixeira esvaziada": "Recycle bin emptied",
    "NASCIMENTO": "BIRTH DATE",
    "Este cadastro antigo não tem data de nascimento. Informe-a para atualizar.": "This older registration has no date of birth. Enter it to update the record.",
    "Mover todos para a lixeira?": "Move all registrations to the recycle bin?",
    "Mover todos para a lixeira": "Move all to recycle bin",
})

TRADUCOES["Español"].update({
    "DD/MM/AAAA": "DD/MM/AAAA",
    "▧  Lixeira": "▧  Papelera",
    "Importar Excel/CSV": "Importar Excel/CSV",
    "Fazer backup": "Crear copia de seguridad",
    "Restaurar backup": "Restaurar copia de seguridad",
    "Data de nascimento (DD/MM/AAAA)": "Fecha de nacimiento (DD/MM/AAAA)",
    "Data de nascimento": "Fecha de nacimiento",
    "Nascimento não informado": "Fecha de nacimiento no informada",
    "Data de nascimento inválida. Use DD/MM/AAAA.": "Fecha de nacimiento no válida. Use DD/MM/AAAA.",
    "A data de nascimento não pode estar no futuro.": "La fecha de nacimiento no puede ser futura.",
    "A data de nascimento é obrigatória.": "La fecha de nacimiento es obligatoria.",
    "Importar cadastros": "Importar registros",
    "Selecione um arquivo Excel ou CSV": "Seleccione un archivo Excel o CSV",
    "Arquivo CSV ou Excel": "Archivo CSV o Excel",
    "Importação concluída": "Importación completada",
    "Importados: ": "Importados: ",
    "Ignorados: ": "Omitidos: ",
    "O arquivo precisa conter as colunas Nome, Data de nascimento e Sexo.": "El archivo debe contener las columnas Nombre, Fecha de nacimiento y Sexo.",
    "Nenhum registro válido foi encontrado no arquivo.": "No se encontraron registros válidos en el archivo.",
    "Lixeira": "Papelera",
    "Cadastros excluídos ficam disponíveis aqui para restauração ou exclusão permanente.": "Los registros eliminados están disponibles aquí para restaurarlos o eliminarlos permanentemente.",
    "Restaurar": "Restaurar",
    "Excluir permanentemente": "Eliminar permanentemente",
    "Esvaziar lixeira": "Vaciar papelera",
    "A lixeira está vazia.": "La papelera está vacía.",
    "Deseja restaurar este cadastro?": "¿Desea restaurar este registro?",
    "Cadastro restaurado com sucesso.": "Registro restaurado correctamente.",
    "Cadastro removido permanentemente.": "Registro eliminado permanentemente.",
    "Deseja esvaziar a lixeira?": "¿Desea vaciar la papelera?",
    "Lixeira esvaziada com sucesso.": "Papelera vaciada correctamente.",
    "Fazer backup dos cadastros": "Crear copia de seguridad de registros",
    "Backup criado com sucesso.": "Copia de seguridad creada correctamente.",
    "Selecione o arquivo de backup": "Seleccione el archivo de copia de seguridad",
    "Arquivo de backup inválido ou incompatível.": "Archivo de copia de seguridad no válido o incompatible.",
    "Restaurar backup?": "¿Restaurar copia de seguridad?",
    "Os cadastros atuais serão substituídos pelos dados do backup.\nEssa ação não poderá ser desfeita.": "Los registros actuales serán reemplazados por los datos de la copia de seguridad.\nEsta acción no se puede deshacer.",
    "Backup restaurado com sucesso.": "Copia de seguridad restaurada correctamente.",
    "Falha ao restaurar backup": "Error al restaurar la copia de seguridad",
    "Data de nascimento: ": "Fecha de nacimiento: ",
    "Exportação de cadastros": "Exportación de registros",
    "Cadastro importado": "Registro importado",
    "Backup criado": "Copia de seguridad creada",
    "Backup restaurado": "Copia de seguridad restaurada",
    "Cadastro restaurado": "Registro restaurado",
    "Cadastro excluído permanentemente": "Registro eliminado permanentemente",
    "Importação de cadastros": "Registros importados",
    "Cadastro movido para a lixeira": "Registro movido a la papelera",
    "Lixeira esvaziada": "Papelera vaciada",
    "NASCIMENTO": "NACIMIENTO",
    "Este cadastro antigo não tem data de nascimento. Informe-a para atualizar.": "Este registro antiguo no tiene fecha de nacimiento. Ingrésela para actualizarlo.",
    "Mover todos para a lixeira?": "¿Mover todos los registros a la papelera?",
    "Mover todos para a lixeira": "Mover todos a la papelera",
})

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.service = CadastroService()
        self.pessoa_selecionada = None

        # Dados complementares ficam em arquivos auxiliares ao lado do ui.py.
        self.caminho_nascimentos = Path(__file__).resolve().with_name("dados_nascimento.json")
        self.caminho_lixeira = Path(__file__).resolve().with_name("lixeira_cadastros.json")
        self.dados_nascimento = self.carregar_dados_nascimento()
        self.migrar_nascimentos_legados()
        self.lixeira_cadastros = self.carregar_lixeira()
        self.pagina_lixeira = 1
        self.itens_por_pagina_lixeira = 5

        # Preferências e histórico ficam salvos junto deste módulo.
        self.configuracoes = self.carregar_configuracoes()
        self.idioma = self.configuracoes.get("idioma", "Português")
        self.tela_ativa = "dashboard"
        self.historico_atividades = self.carregar_historico()
        self.sincronizar_idades_por_nascimento()

        self.title(self.t("Sistema de Cadastros"))
        self.geometry("1180x720")
        self.minsize(1000, 650)

        self.configure(fg_color=COR_FUNDO)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._busca_job = None
        self._aviso = None
        self._aviso_job = None
        self.botoes_menu = {}

        # A lista usa páginas de cards, sem rolagem interna.
        # Isso evita o defeito visual conhecido do CTkScrollableFrame ao rolar rápido.
        self.pagina_atual = 1
        # Quantidade fixa por página: não é uma preferência configurável.
        self.itens_por_pagina = 5
        self.itens_por_pagina_relatorio = 7
        self.total_paginas = 1

        self.criar_sidebar()
        self.traduzir_arvore(self.sidebar)
        self.criar_conteudo()
        self.criar_tela_cadastros()

        self.mostrar_dashboard()
        self.agendar_verificacao_diaria_idades()

    # ----------------------------
    # CONFIGURAÇÕES E HISTÓRICO
    # ----------------------------

    def carregar_configuracoes(self):
        """Carrega somente o idioma e remove preferências antigas do JSON."""
        self.caminho_configuracoes = Path(__file__).resolve().with_name("configuracoes.json")

        dados = {}
        try:
            with self.caminho_configuracoes.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (OSError, json.JSONDecodeError):
            dados = {}

        if not isinstance(dados, dict):
            dados = {}

        idioma = dados.get("idioma", "Português")
        if idioma not in {"Português", "English", "Español"}:
            idioma = "Português"

        # O arquivo passa a conter apenas o idioma. Assim, chaves antigas como
        # itens_por_pagina_cadastros e itens_por_pagina_relatorios são removidas.
        configuracoes = {"idioma": idioma}
        try:
            with self.caminho_configuracoes.open("w", encoding="utf-8") as arquivo:
                json.dump(configuracoes, arquivo, ensure_ascii=False, indent=4)
        except OSError:
            # O sistema continua funcionando com o idioma carregado em memória.
            pass

        return configuracoes

    def carregar_historico(self):
        """Lê o histórico persistido; um arquivo ausente começa vazio."""
        self.caminho_historico = Path(__file__).resolve().with_name("historico_atividades.json")
        try:
            with self.caminho_historico.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def registrar_atividade(self, acao, detalhes):
        """Registra uma ação e tenta salvá-la em arquivo para persistir entre execuções."""
        registro = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            # Guarda o histórico em português como formato canônico; a tela traduz
            # os registros ao exibi-los, permitindo alternar o idioma depois.
            "acao": str(acao),
            "detalhes": str(detalhes),
        }
        self.historico_atividades.insert(0, registro)

        try:
            with self.caminho_historico.open("w", encoding="utf-8") as arquivo:
                json.dump(self.historico_atividades, arquivo, ensure_ascii=False, indent=4)
        except OSError:
            # A ação principal já foi concluída; o histórico permanece em memória nesta sessão.
            self.mostrar_aviso(
                "A ação foi concluída, mas não foi possível salvar o histórico no disco.",
                "aviso",
                titulo="Histórico não salvo"
            )

    def carregar_dados_nascimento(self):
        try:
            with self.caminho_nascimentos.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return dados if isinstance(dados, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def salvar_dados_nascimento(self):
        with self.caminho_nascimentos.open("w", encoding="utf-8") as arquivo:
            json.dump(self.dados_nascimento, arquivo, ensure_ascii=False, indent=4)

    def migrar_nascimentos_legados(self):
        """Move datas do antigo dados_nascimento.json para cada pessoa em pessoas.json."""
        if not self.dados_nascimento:
            return

        pessoas_por_id = {str(p.get("id")): p for p in self.service.listar()}
        pendentes = {}
        alterou = False

        for pessoa_id, valor in list(self.dados_nascimento.items()):
            pessoa = pessoas_por_id.get(str(pessoa_id))
            if pessoa is None or pessoa.get("data_nascimento"):
                # Datas de IDs inexistentes ou já migrados não precisam ficar no arquivo antigo.
                continue

            try:
                nascimento = self.normalizar_data_nascimento(valor)
            except ValueError:
                pendentes[str(pessoa_id)] = valor
                continue

            if nascimento > date.today():
                # Mantém o valor antigo para não descartá-lo; o usuário poderá corrigir ao editar.
                pendentes[str(pessoa_id)] = valor
                continue

            idade = self.calcular_idade(nascimento)
            self.service.atualizar(
                pessoa["id"], pessoa["nome"], idade, pessoa["sexo"], nascimento.isoformat()
            )
            alterou = True

        # O arquivo auxiliar passa a guardar apenas datas antigas que ainda precisam de correção.
        if alterou or pendentes != self.dados_nascimento:
            self.dados_nascimento = pendentes
            self.salvar_dados_nascimento()

    def carregar_lixeira(self):
        try:
            with self.caminho_lixeira.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                return []
            registros_validos = []
            for registro in dados:
                if not isinstance(registro, dict):
                    continue
                registro.setdefault("chave_lixeira", str(uuid4()))
                registros_validos.append(registro)
            return registros_validos
        except (OSError, json.JSONDecodeError):
            return []

    def salvar_lixeira(self):
        with self.caminho_lixeira.open("w", encoding="utf-8") as arquivo:
            json.dump(self.lixeira_cadastros, arquivo, ensure_ascii=False, indent=4)

    @staticmethod
    def normalizar_data_nascimento(valor):
        """Converte datas comuns de planilhas e do formulário em date."""
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        if valor is None:
            raise ValueError("A data de nascimento é obrigatória.")

        texto = str(valor).strip()
        formatos = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y")
        for formato in formatos:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue
        raise ValueError("Data de nascimento inválida. Use DD/MM/AAAA.")

    @staticmethod
    def calcular_idade(data_nascimento):
        hoje = date.today()
        return hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )

    def nascimento_da_pessoa(self, pessoa):
        valor = pessoa.get("data_nascimento") or self.dados_nascimento.get(str(pessoa.get("id")))
        if not valor:
            return None
        try:
            return self.normalizar_data_nascimento(valor)
        except ValueError:
            return None

    def sincronizar_idades_por_nascimento(self):
        """Atualiza a idade salva sempre que a data atual exigir uma mudança."""
        alterou = False
        for pessoa in self.service.listar():
            nascimento = self.nascimento_da_pessoa(pessoa)
            if nascimento is None:
                continue
            idade_atual = self.calcular_idade(nascimento)
            try:
                idade_salva = int(pessoa.get("idade", -1))
            except (TypeError, ValueError):
                idade_salva = -1
            if idade_salva != idade_atual:
                try:
                    self.service.atualizar(
                        pessoa["id"], pessoa["nome"], idade_atual, pessoa["sexo"]
                    )
                    alterou = True
                except Exception:
                    # Um cadastro incompatível não deve impedir a abertura do sistema.
                    continue
        if alterou:
            # Mantém os indicadores e relatórios coerentes ao abrir o programa.
            pass

    def agendar_verificacao_diaria_idades(self):
        agora = datetime.now()
        amanha = (agora + timedelta(days=1)).replace(hour=0, minute=0, second=5, microsecond=0)
        atraso = max(1000, int((amanha - agora).total_seconds() * 1000))
        self.after(atraso, self.verificar_idades_diariamente)

    def verificar_idades_diariamente(self):
        try:
            self.sincronizar_idades_por_nascimento()
            if self.tela_ativa == "dashboard":
                self.mostrar_dashboard()
            elif self.tela_ativa == "cadastros":
                self.atualizar_lista()
            elif self.tela_ativa == "relatorios":
                self.atualizar_tabela_relatorio()
        finally:
            self.agendar_verificacao_diaria_idades()

    def localizar_cadastro_adicionado(self, ids_anteriores, nome, idade, sexo):
        atuais = self.service.listar()
        novos = [p for p in atuais if str(p.get("id")) not in ids_anteriores]
        if novos:
            return max(novos, key=lambda p: int(p.get("id", 0)))
        candidatos = [
            p for p in atuais
            if p.get("nome", "").casefold() == nome.casefold()
            and int(p.get("idade", -1)) == idade
            and p.get("sexo") == sexo
        ]
        return max(candidatos, key=lambda p: int(p.get("id", 0))) if candidatos else None

    def adicionar_com_nascimento(self, nome, data_nascimento, sexo):
        idade = self.calcular_idade(data_nascimento)
        return self.service.adicionar(
            nome, idade, sexo, data_nascimento=data_nascimento.isoformat()
        )

    def mover_para_lixeira(self, pessoa):
        registro = dict(pessoa)
        nascimento = self.nascimento_da_pessoa(pessoa)
        registro["data_nascimento"] = nascimento.isoformat() if nascimento else None
        registro["data_exclusao"] = datetime.now().isoformat(timespec="seconds")
        registro["chave_lixeira"] = str(uuid4())

        self.lixeira_cadastros.insert(0, registro)
        try:
            self.salvar_lixeira()
            self.service.excluir(pessoa["id"])
        except Exception:
            self.lixeira_cadastros = [
                item for item in self.lixeira_cadastros
                if item.get("chave_lixeira") != registro["chave_lixeira"]
            ]
            try:
                self.salvar_lixeira()
            except OSError:
                pass
            raise

        self.dados_nascimento.pop(str(pessoa["id"]), None)
        try:
            self.salvar_dados_nascimento()
        except OSError:
            # A data permanece no registro principal ou na lixeira; o arquivo auxiliar é legado.
            pass
        return registro

    def recarregar_tela_atual(self):
        telas = {
            "dashboard": self.mostrar_dashboard,
            "cadastros": self.mostrar_cadastros,
            "relatorios": self.mostrar_relatorios,
            "lixeira": self.mostrar_lixeira,
            "historico": self.mostrar_historico,
            "configuracoes": self.mostrar_configuracoes,
        }
        telas.get(self.tela_ativa, self.mostrar_dashboard)()

    def salvar_arquivo_configuracoes(self):
        with self.caminho_configuracoes.open("w", encoding="utf-8") as arquivo:
            json.dump(self.configuracoes, arquivo, ensure_ascii=False, indent=4)

    def t(self, texto):
        """Retorna a tradução do texto conforme o idioma selecionado."""
        if not isinstance(texto, str) or self.idioma == "Português":
            return texto

        traducoes = TRADUCOES.get(self.idioma, {})
        if texto in traducoes:
            return traducoes[texto]

        # Textos dinâmicos que incluem quantidades ou números de página.
        pagina = re.fullmatch(r"Página (\d+) de (\d+)(?:  •  (\d+) cadastro\(s\))?", texto)
        if pagina:
            atual, total, registros = pagina.groups()
            if self.idioma == "English":
                resultado = f"Page {atual} of {total}"
                return resultado + (f"  •  {registros} registration(s)" if registros else "")
            resultado = f"Página {atual} de {total}"
            return resultado + (f"  •  {registros} registro(s)" if registros else "")

        total_atividades = re.fullmatch(r"(\d+) atividade\(s\) registrada\(s\)", texto)
        if total_atividades:
            quantidade = int(total_atividades.group(1))
            if self.idioma == "English":
                return f"{quantidade} activity recorded" if quantidade == 1 else f"{quantidade} activities recorded"
            return f"{quantidade} actividad registrada" if quantidade == 1 else f"{quantidade} actividades registradas"

        importacao = re.match(r"Importados: (\d+)  •  Ignorados: (\d+)(.*)", texto, re.DOTALL)
        if importacao:
            importados, ignorados, complemento = importacao.groups()
            if self.idioma == "English":
                return f"Imported: {importados}  •  Skipped: {ignorados}{complemento}"
            return f"Importados: {importados}  •  Omitidos: {ignorados}{complemento}"

        total_lixeira = re.fullmatch(r"(\d+) cadastro\(s\) na lixeira", texto)
        if total_lixeira:
            quantidade = int(total_lixeira.group(1))
            if self.idioma == "English":
                return f"{quantidade} registration(s) in recycle bin"
            return f"{quantidade} registro(s) en la papelera"

        total_registros = re.fullmatch(r"(\d+) cadastro\(s\) encontrados", texto)
        if total_registros:
            quantidade = int(total_registros.group(1))
            if self.idioma == "English":
                return f"{quantidade} registration found" if quantidade == 1 else f"{quantidade} registrations found"
            return f"{quantidade} registro encontrado" if quantidade == 1 else f"{quantidade} registros encontrados"

        # Frases dinâmicas com nomes, IDs e quantidades.
        prefixos = {
            "English": {
                "Modo: editando cadastro #": "Mode: editing registration #",
                "Cadastro de ": "Registration for ",
                "Você está prestes a excluir ": "You are about to delete ",
                "Você está prestes a mover ": "You are about to move ",
                "PDF exportado com ": "PDF exported with ",
                "Planilha exportada com ": "Spreadsheet exported with ",
                "Relatório exportado com ": "Report exported with ",
                "Não foi possível gerar a planilha: ": "Could not create the spreadsheet: ",
                "Não foi possível gerar o PDF: ": "Could not create the PDF: ",
                "Não foi possível salvar o arquivo: ": "Could not save the file: ",
                "Não foi possível salvar as configurações: ": "Could not save settings: ",
            },
            "Español": {
                "Modo: editando cadastro #": "Modo: editando registro #",
                "Cadastro de ": "Registro de ",
                "Você está prestes a excluir ": "Está a punto de eliminar ",
                "Você está prestes a mover ": "Está a punto de mover ",
                "PDF exportado com ": "PDF exportado con ",
                "Planilha exportada com ": "Hoja de cálculo exportada con ",
                "Relatório exportado com ": "Informe exportado con ",
                "Não foi possível gerar a planilha: ": "No se pudo crear la hoja de cálculo: ",
                "Não foi possível gerar o PDF: ": "No se pudo crear el PDF: ",
                "Não foi possível salvar o arquivo: ": "No se pudo guardar el archivo: ",
                "Não foi possível salvar as configurações: ": "No se pudo guardar la configuración: ",
            },
        }
        for origem, destino in prefixos[self.idioma].items():
            if texto.startswith(origem):
                texto = destino + texto[len(origem):]
                break

        if self.idioma == "English":
            texto = texto.replace(" anos  •  ", " years  •  ").replace(" anos • ", " years • ")
            if texto.endswith(" anos"):
                texto = texto[:-5] + " years"
            texto = texto.replace(" cadastro(s)", " registration(s)").replace(" cadastro(s).", " registration(s).")
            texto = texto.replace(" cadastro(s) • ", " registration(s) • ")
            texto = texto.replace(" excluído(s)", " deleted")
            texto = texto.replace("Masculino", "Male").replace("Feminino", "Female")
            texto = texto.replace(" com sucesso", " successfully")
            texto = texto.replace("Cadastro criado", "Registration created")
            texto = texto.replace("Cadastro atualizado", "Registration updated")
            texto = texto.replace("Cadastro excluído", "Registration deleted")
            texto = texto.replace(" excluído.", " deleted.")
            texto = texto.replace("Essa ação não poderá ser desfeita.", "This action cannot be undone.")
            texto = texto.replace("Eles poderão ser restaurados pela tela Lixeira.", "They can be restored from the Recycle bin screen.")
            texto = texto.replace("movido(s) para a lixeira", "moved to the recycle bin")
        else:
            texto = texto.replace(" anos  •  ", " años  •  ").replace(" anos • ", " años • ")
            if texto.endswith(" anos"):
                texto = texto[:-5] + " años"
            texto = texto.replace(" cadastro(s)", " registro(s)").replace(" cadastro(s).", " registro(s).")
            texto = texto.replace(" cadastro(s) • ", " registro(s) • ")
            texto = texto.replace(" excluído(s)", " eliminados")
            texto = texto.replace("Feminino", "Femenino")
            texto = texto.replace(" com sucesso", " correctamente")
            texto = texto.replace("Cadastro criado", "Registro creado")
            texto = texto.replace("Cadastro atualizado", "Registro actualizado")
            texto = texto.replace("Cadastro excluído", "Registro eliminado")
            texto = texto.replace(" excluído.", " eliminado.")
            texto = texto.replace("Essa ação não poderá ser desfeita.", "Esta acción no se puede deshacer.")
            texto = texto.replace("Eles poderão ser restaurados pela tela Lixeira.", "Se pueden restaurar desde la pantalla Papelera.")
            texto = texto.replace("movido(s) para a lixeira", "movidos a la papelera")
        return texto

    def traduzir_arvore(self, widget):
        """Traduz textos visíveis de uma tela já construída."""
        for filho in widget.winfo_children():
            try:
                if isinstance(filho, ctk.CTkComboBox):
                    valores = list(filho.cget("values"))
                    atual = filho.get()
                    filho.configure(values=[self.t(valor) for valor in valores])
                    if atual:
                        filho.set(self.t(atual))
                else:
                    texto = filho.cget("text")
                    if texto:
                        filho.configure(text=self.t(texto))
                    try:
                        placeholder = filho.cget("placeholder_text")
                        if placeholder:
                            filho.configure(placeholder_text=self.t(placeholder))
                    except Exception:
                        pass
            except Exception:
                pass
            self.traduzir_arvore(filho)

    def recriar_interface_no_idioma_atual(self):
        """Reconstrói widgets persistentes para permitir alternar entre idiomas."""
        self.title(self.t("Sistema de Cadastros"))

        self.sidebar.destroy()
        self.botoes_menu = {}
        self.criar_sidebar()
        self.traduzir_arvore(self.sidebar)

        if hasattr(self, "tela_cadastros"):
            self.tela_cadastros.destroy()
        self.criar_tela_cadastros()

        telas = {
            "dashboard": self.mostrar_dashboard,
            "cadastros": self.mostrar_cadastros,
            "relatorios": self.mostrar_relatorios,
            "lixeira": self.mostrar_lixeira,
            "historico": self.mostrar_historico,
            "configuracoes": self.mostrar_configuracoes,
        }
        telas.get(self.tela_ativa, self.mostrar_dashboard)()

    # ----------------------------
    # LAYOUT
    # ----------------------------

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=COR_SIDEBAR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="CADASTROS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COR_DESTAQUE
        )
        logo.pack(pady=(35, 4))

        subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Sistema de gerenciamento",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_SEC
        )
        subtitulo.pack(pady=(0, 35))

        self.btn_dashboard = self.botao_menu(
            "▣  Dashboard",
            self.mostrar_dashboard,
            "dashboard"
        )

        self.btn_cadastros = self.botao_menu(
            "☷  Cadastros",
            self.mostrar_cadastros,
            "cadastros"
        )

        self.btn_relatorios = self.botao_menu(
            "▤  Relatórios",
            self.mostrar_relatorios,
            "relatorios"
        )

        self.btn_lixeira = self.botao_menu(
            "▧  Lixeira",
            self.mostrar_lixeira,
            "lixeira"
        )

        self.btn_historico = self.botao_menu(
            "⟲  Histórico",
            self.mostrar_historico,
            "historico"
        )

        self.btn_configuracoes = self.botao_menu(
            "⛭  Configurações",
            self.mostrar_configuracoes,
            "configuracoes"
        )


    def botao_menu(self, texto, comando, chave):
        botao = ctk.CTkButton(
            self.sidebar,
            text=texto,
            command=comando,
            height=45,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            hover_color=COR_MENU_HOVER,
            text_color=COR_TEXTO_MENU,
            font=ctk.CTkFont(size=14)
        )
        botao.pack(fill="x", padx=15, pady=4)

        self.botoes_menu[chave] = botao
        return botao

    def marcar_menu(self, chave_ativa):
        for chave, botao in self.botoes_menu.items():
            if chave == chave_ativa:
                botao.configure(
                    fg_color=COR_MENU_ATIVO,
                    hover_color=COR_MENU_ATIVO,
                    text_color=COR_DESTAQUE
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    hover_color=COR_MENU_HOVER,
                    text_color=COR_TEXTO_MENU
                )

    def criar_conteudo(self):
        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COR_FUNDO
        )
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_rowconfigure(1, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            if widget is self.tela_cadastros:
                widget.grid_remove()
            else:
                widget.destroy()

    def titulo_pagina(self, titulo, descricao, parent=None):
        if parent is None:
            parent = self.conteudo

        topo = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        topo.grid(row=0, column=0, sticky="ew", padx=35, pady=(30, 20))

        ctk.CTkLabel(
            topo,
            text=titulo,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            topo,
            text=descricao,
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SEC
        ).pack(anchor="w", pady=(4, 0))

    def centralizar_janela(self, janela):
        """Centraliza uma janela modal em relação à janela principal."""
        janela.update_idletasks()
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        x = self.winfo_rootx() + (self.winfo_width() - largura) // 2
        y = self.winfo_rooty() + (self.winfo_height() - altura) // 2
        janela.geometry(f"+{x}+{y}")
        janela.lift()
        janela.focus_force()

    # ----------------------------
    # AVISOS (mensagens no canto)
    # ----------------------------

    def mostrar_aviso(self, mensagem, tipo="sucesso", titulo=None):
        mensagem = self.t(mensagem)
        titulo = self.t(titulo) if titulo else titulo
        cores = {
            "sucesso": COR_SUCESSO,
            "aviso": COR_AVISO,
            "erro": COR_ERRO,
        }
        icones = {
            "sucesso": "✓",
            "aviso": "!",
            "erro": "✕",
        }

        cor = cores.get(tipo, COR_SUCESSO)
        icone = icones.get(tipo, "✓")

        self.fechar_aviso()

        self._aviso = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=COR_CARD,
            border_width=1,
            border_color=cor
        )

        ctk.CTkLabel(
            self._aviso,
            text=icone,
            text_color=cor,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=(16, 10), pady=12)

        corpo = ctk.CTkFrame(self._aviso, fg_color="transparent")
        corpo.pack(side="left", padx=(0, 18), pady=12)

        if titulo:
            ctk.CTkLabel(
                corpo,
                text=titulo,
                text_color=COR_TEXTO,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w")

        ctk.CTkLabel(
            corpo,
            text=mensagem,
            text_color=COR_TEXTO_CORPO if titulo else COR_TEXTO,
            font=ctk.CTkFont(size=13),
            wraplength=280,
            justify="left"
        ).pack(anchor="w")

        # Calcula o tamanho real do aviso antes de exibi-lo. Isso evita que
        # o tamanho inicial padrão do CTkFrame apareça como um quadrado grande.
        self._aviso.update_idletasks()
        self._aviso.place(relx=1.0, rely=1.0, x=-25, y=-25, anchor="se")
        self._aviso.lift()

        self._aviso_job = self.after(TEMPO_AVISO_MS, self.fechar_aviso)

    def fechar_aviso(self):
        if self._aviso_job is not None:
            try:
                self.after_cancel(self._aviso_job)
            except Exception:
                pass
            self._aviso_job = None

        if self._aviso is not None:
            self._aviso.destroy()
            self._aviso = None

    # ----------------------------
    # DASHBOARD
    # ----------------------------

    def mostrar_dashboard(self):
        self.tela_ativa = "dashboard"
        self.limpar_conteudo()
        self.marcar_menu("dashboard")
        self.titulo_pagina(
            "Dashboard",
            "Visão geral e indicadores dos cadastros"
        )

        area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area.grid(row=1, column=0, sticky="nsew", padx=25, pady=(2, 12))
        area.grid_columnconfigure((0, 1, 2), weight=1, uniform="dashboard_cards")
        # Mantém as linhas do Dashboard com alturas previsíveis. A linha dos
        # gráficos não deve expandir/recalcular sua altura ao abrir a tela.
        area.grid_rowconfigure(0, weight=0)
        area.grid_rowconfigure(1, weight=0)
        area.grid_rowconfigure(2, weight=0)
        area.grid_rowconfigure(3, weight=0)

        stats = self.service.estatisticas()
        pessoas = self.service.listar()
        total = len(pessoas)

        # Seis indicadores em cards maiores, ocupando toda a largura disponível.
        cards = [
            ("Pessoas cadastradas", stats["total"], "#ff8a00"),
            ("Homens", stats["homens"], "#4da6ff"),
            ("Mulheres", stats["mulheres"], "#e879f9"),
            ("Maiores de idade", stats["maiores"], "#22c55e"),
            ("Menores de idade", stats["menores"], "#facc15"),
            ("60 anos ou mais", stats["idosos"], "#a78bfa"),
        ]

        for index, (titulo, valor, cor) in enumerate(cards):
            linha = index // 3
            coluna = index % 3

            card = ctk.CTkFrame(
                area,
                height=122,
                corner_radius=14,
                fg_color=COR_CARD
            )
            card.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=8,
                pady=8
            )
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=titulo,
                text_color=COR_TEXTO_SEC,
                font=ctk.CTkFont(size=14)
            ).pack(anchor="w", padx=20, pady=(19, 4))

            ctk.CTkLabel(
                card,
                text=str(valor),
                text_color=cor,
                font=ctk.CTkFont(size=36, weight="bold")
            ).pack(anchor="w", padx=20)

        # Dados usados nos painéis de distribuição.
        homens = sum(1 for pessoa in pessoas if pessoa["sexo"] == "M")
        mulheres = sum(1 for pessoa in pessoas if pessoa["sexo"] == "F")
        menores = sum(1 for pessoa in pessoas if pessoa["idade"] < 18)
        adultos = sum(1 for pessoa in pessoas if 18 <= pessoa["idade"] < 60)
        idosos = sum(1 for pessoa in pessoas if pessoa["idade"] >= 60)

        # Dois gráficos de rosca substituem os painéis antigos de barras.
        # As quantidades continuam visíveis nos cards superiores e também nas legendas.
        graficos = ctk.CTkFrame(
            area,
            height=235,
            fg_color="transparent"
        )
        graficos.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=8,
            pady=(10, 8)
        )
        graficos.grid_columnconfigure((0, 1), weight=1, uniform="graficos")
        graficos.grid_rowconfigure(0, weight=0)
        graficos.grid_propagate(False)

        painel_sexo = ctk.CTkFrame(
            graficos,
            height=235,
            corner_radius=14,
            fg_color=COR_CARD
        )
        painel_sexo.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        painel_sexo.grid_columnconfigure(0, weight=1)
        painel_sexo.grid_propagate(False)

        self.criar_grafico_rosca_dashboard(
            painel_sexo,
            "Proporção por sexo",
            [
                ("Homens", homens, "#4da6ff"),
                ("Mulheres", mulheres, "#e879f9"),
            ],
        )

        painel_idade = ctk.CTkFrame(
            graficos,
            height=235,
            corner_radius=14,
            fg_color=COR_CARD
        )
        painel_idade.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        painel_idade.grid_columnconfigure(0, weight=1)
        painel_idade.grid_propagate(False)

        self.criar_grafico_rosca_dashboard(
            painel_idade,
            "Proporção por faixa etária",
            [
                ("Menores de 18", menores, "#facc15"),
                ("18 a 59 anos", adultos, "#22c55e"),
                ("60 anos ou mais", idosos, "#a78bfa"),
            ],
        )

        # Dois mini-cards para destacar a pessoa mais velha e a mais nova.
        destaque = ctk.CTkFrame(area, fg_color="transparent")
        destaque.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=8,
            pady=(4, 2)
        )
        destaque.grid_columnconfigure((0, 1), weight=1, uniform="destaques")
        destaque.grid_rowconfigure(0, weight=1)

        velha = stats.get("mais_velha")
        nova = stats.get("mais_nova")

        def criar_card_destaque(parent, coluna, titulo, pessoa, cor):
            card = ctk.CTkFrame(
                parent,
                height=80,
                corner_radius=14,
                fg_color=COR_CARD,
                border_width=1,
                border_color=cor
            )
            card.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=(0, 7) if coluna == 0 else (7, 0)
            )
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=self.t(titulo),
                text_color=cor,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w", padx=13, pady=(5, 1))

            if pessoa:
                ctk.CTkLabel(
                    card,
                    text=pessoa["nome"],
                    text_color=COR_TEXTO,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    anchor="w",
                    justify="left",
                    wraplength=390
                ).pack(anchor="w", padx=13, pady=(0, 0))

                ctk.CTkLabel(
                    card,
                    text=f'{pessoa["idade"]} {self.t("anos")}',
                    text_color=COR_TEXTO_CORPO,
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(anchor="w", padx=13, pady=(0, 3))
            else:
                ctk.CTkLabel(
                    card,
                    text=self.t("Nenhum cadastro"),
                    text_color=COR_TEXTO_SEC,
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(anchor="w", padx=13, pady=(4, 4))

        criar_card_destaque(
            destaque, 0, "Pessoa mais velha", velha, "#a78bfa"
        )
        criar_card_destaque(
            destaque, 1, "Pessoa mais nova", nova, COR_DESTAQUE
        )

        self.traduzir_arvore(self.conteudo)

    def criar_grafico_rosca_dashboard(self, parent, titulo, dados):
        """Desenha um gráfico de rosca com quantidade e percentual por categoria."""
        # O gráfico de faixa etária possui três categorias; compactamos apenas
        # sua legenda para que a terceira linha (60 anos ou mais) não seja cortada.
        legenda_compacta = len(dados) >= 3

        ctk.CTkLabel(
            parent,
            text=self.t(titulo),
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_TEXTO
        ).pack(
            anchor="w",
            padx=18,
            pady=(13, 3) if legenda_compacta else (16, 5)
        )

        corpo = ctk.CTkFrame(parent, fg_color="transparent")
        corpo.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 4) if legenda_compacta else (0, 9)
        )

        total = sum(quantidade for _, quantidade, _ in dados)
        valores = [quantidade for _, quantidade, _ in dados]
        cores = [cor for _, _, cor in dados]

        # Quando não há cadastros, mostra uma rosca neutra em vez de um gráfico vazio.
        valores_grafico = valores if total > 0 else [1]
        cores_grafico = cores if total > 0 else [COR_BORDA]

        altura_figura = 1.48 if legenda_compacta else 1.65
        figura = Figure(figsize=(1.70, altura_figura), dpi=110, facecolor=COR_CARD)
        eixo = figura.add_axes([0.015, 0.025, 0.97, 0.95])
        eixo.set_facecolor(COR_CARD)
        eixo.set_aspect("equal")
        eixo.axis("off")

        eixo.pie(
            valores_grafico,
            colors=cores_grafico,
            startangle=90,
            counterclock=False,
            normalize=True,
            wedgeprops={
                "width": 0.29,
                "edgecolor": COR_CARD,
                "linewidth": 3.5,
                "antialiased": True,
            },
        )

        eixo.text(
            0, 0.08, str(total),
            ha="center", va="center",
            color=COR_TEXTO, fontsize=18, fontweight="bold"
        )
        eixo.text(
            0, -0.20, self.t("Pessoas").upper(),
            ha="center", va="center",
            color=COR_TEXTO_SEC, fontsize=6.7, fontweight="bold"
        )

        canvas = FigureCanvasTkAgg(figura, master=corpo)
        widget_grafico = canvas.get_tk_widget()
        widget_grafico.configure(
            bg=COR_CARD,
            highlightthickness=0,
            borderwidth=0,
        )
        # Desenha de forma síncrona para evitar que o Canvas seja reposicionado
        # visualmente após o primeiro ciclo de atualização do Tkinter.
        canvas.draw()
        widget_grafico.pack(side="left", padx=(0, 4), pady=0)

        legenda = ctk.CTkFrame(corpo, fg_color="transparent")
        legenda.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(2, 5),
            pady=(2, 1) if legenda_compacta else (7, 5)
        )

        for nome, quantidade, cor in dados:
            percentual = (quantidade / total * 100) if total else 0

            item = ctk.CTkFrame(legenda, fg_color="transparent")
            item.pack(
                fill="x",
                anchor="w",
                pady=(1, 1) if legenda_compacta else (3, 5)
            )

            marcador = ctk.CTkFrame(
                item,
                width=9,
                height=9,
                corner_radius=4,
                fg_color=cor,
            )
            marcador.pack(side="left", padx=(0, 7), pady=(2, 0))
            marcador.pack_propagate(False)

            ctk.CTkLabel(
                item,
                text=self.t(nome),
                text_color=COR_TEXTO,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
            ).pack(side="left", anchor="w")

            # A palavra "Quantidade:" acompanha a cor da categoria do gráfico.
            # Quantidade e percentual permanecem brancos para facilitar a leitura.
            linha_quantidade = ctk.CTkFrame(legenda, fg_color="transparent")
            linha_quantidade.pack(
                anchor="w",
                padx=(16, 0),
                pady=(0, 1) if legenda_compacta else (0, 3)
            )

            ctk.CTkLabel(
                linha_quantidade,
                text=self.t("Quantidade:"),
                text_color=cor,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
            ).pack(side="left")

            ctk.CTkLabel(
                linha_quantidade,
                text=f" {quantidade} / {percentual:.1f}%",
                text_color="#FFFFFF",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
            ).pack(side="left")

    # ----------------------------
    # CADASTROS
    # ----------------------------

    def mostrar_cadastros(self):
        self.tela_ativa = "cadastros"
        self.limpar_conteudo()
        self.marcar_menu("cadastros")
        self.tela_cadastros.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def criar_tela_cadastros(self):
        self.tela_cadastros = ctk.CTkFrame(
            self.conteudo,
            corner_radius=0,
            fg_color="transparent"
        )
        self.tela_cadastros.grid_rowconfigure(1, weight=1)
        self.tela_cadastros.grid_columnconfigure(0, weight=1)

        self.titulo_pagina(
            "Cadastros",
            "Adicione, pesquise, edite ou remova pessoas",
            parent=self.tela_cadastros
        )

        container = ctk.CTkFrame(
            self.tela_cadastros,
            fg_color="transparent"
        )
        container.grid(row=1, column=0, sticky="nsew", padx=35, pady=5)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(1, weight=1)

        formulario = ctk.CTkFrame(
            container,
            width=300,
            corner_radius=14,
            fg_color=COR_CARD
        )
        formulario.grid(row=1, column=0, sticky="nsw", padx=(0, 20))
        formulario.grid_propagate(False)

        ctk.CTkLabel(
            formulario,
            text="Novo cadastro",
            font=ctk.CTkFont(size=19, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 20))

        self.entry_nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Nome completo",
            height=40
        )
        self.entry_nome.pack(fill="x", padx=20, pady=7)

        ctk.CTkLabel(
            formulario,
            text=self.t("Data de nascimento"),
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=20, pady=(7, 2))

        self.entry_data_nascimento = ctk.CTkEntry(
            formulario,
            placeholder_text="DD/MM/AAAA",
            height=40
        )
        self.entry_data_nascimento.pack(fill="x", padx=20, pady=(0, 7))
        self.entry_data_nascimento.bind(
            "<KeyRelease>", self.aplicar_mascara_data_nascimento
        )
        self._data_nascimento_digitos_anteriores = ""

        self.combo_sexo = ctk.CTkComboBox(
            formulario,
            values=["Masculino", "Feminino"],
            height=40
        )
        self.combo_sexo.set(self.t("Masculino"))
        self.combo_sexo.pack(fill="x", padx=20, pady=7)

        self.btn_salvar = ctk.CTkButton(
            formulario,
            text="Cadastrar pessoa",
            height=42,
            corner_radius=8,
            fg_color=COR_DESTAQUE,
            hover_color=COR_DESTAQUE_HOVER,
            text_color=COR_TEXTO_NO_DESTAQUE,
            command=self.salvar_cadastro
        )
        self.btn_salvar.pack(fill="x", padx=20, pady=(20, 7))

        self.btn_cancelar = ctk.CTkButton(
            formulario,
            text="Limpar formulário",
            height=38,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=self.limpar_formulario
        )
        self.btn_cancelar.pack(fill="x", padx=20, pady=5)

        # Área separada para ações administrativas e potencialmente destrutivas.
        ctk.CTkFrame(
            formulario,
            height=1,
            fg_color=COR_BORDA
        ).pack(fill="x", padx=20, pady=(16, 10))

        ctk.CTkLabel(
            formulario,
            text="AÇÕES ADMINISTRATIVAS",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=20, pady=(0, 7))

        self.btn_excluir_todos = ctk.CTkButton(
            formulario,
            text="Excluir todos os cadastros",
            height=38,
            corner_radius=8,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            text_color="#ffffff",
            command=self.pedir_confirmacao_exclusao_todos
        )
        self.btn_excluir_todos.pack(fill="x", padx=20, pady=(0, 5))

        self.lbl_edicao = ctk.CTkLabel(
            formulario,
            text=self.t("Modo: novo cadastro"),
            text_color=COR_TEXTO_MUDO,
            font=ctk.CTkFont(size=11)
        )
        self.lbl_edicao.pack(anchor="w", padx=20, pady=(12, 0))

        area_lista = ctk.CTkFrame(
            container,
            corner_radius=14,
            fg_color=COR_CARD
        )
        area_lista.grid(row=1, column=1, sticky="nsew")
        area_lista.grid_columnconfigure(0, weight=1)
        area_lista.grid_rowconfigure(2, weight=1)

        filtros = ctk.CTkFrame(area_lista, fg_color="transparent")
        filtros.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        filtros.grid_columnconfigure(0, weight=1)

        self.entry_busca = ctk.CTkEntry(
            filtros,
            placeholder_text="Pesquisar por nome...",
            height=38
        )
        # Os rótulos ficam dentro dos próprios campos, junto da opção selecionada.
        self.entry_busca.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 12)
        )
        self.entry_busca.bind("<KeyRelease>", lambda event: self.agendar_busca())

        self.combo_filtro = ctk.CTkComboBox(
            filtros,
            values=[
                "Sexo: Todos",
                "Sexo: Masculino",
                "Sexo: Feminino"
            ],
            width=155,
            height=38,
            command=lambda _: self.alterar_filtros()
        )
        self.combo_filtro.set("Sexo: Todos")
        self.combo_filtro.grid(row=0, column=1, padx=8)

        self.combo_idade = ctk.CTkComboBox(
            filtros,
            values=[
                "Idade: Todas",
                "Idade: Menor de 18",
                "Idade: 18 ou mais",
                "Idade: 60 ou mais"
            ],
            width=180,
            height=38,
            command=lambda _: self.alterar_filtros()
        )
        self.combo_idade.set("Idade: Todas")
        self.combo_idade.grid(row=0, column=2, padx=(8, 0))

        self.combo_ordenacao = ctk.CTkComboBox(
            filtros,
            values=[
                "Ordenar: Padrão",
                "Ordenar: Mais recentes",
                "Ordenar: Nome A-Z",
                "Ordenar: Nome Z-A",
                "Ordenar: Menor idade",
                "Ordenar: Maior idade"
            ],
            width=185,
            height=38,
            command=lambda _: self.alterar_filtros()
        )
        self.combo_ordenacao.set("Ordenar: Padrão")
        self.combo_ordenacao.grid(row=0, column=3, padx=(8, 0))

        # Ferramentas ficam na área de cadastros, sem criar outro card separado.
        ferramentas = ctk.CTkFrame(area_lista, fg_color="transparent")
        ferramentas.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 7))

        ctk.CTkButton(
            ferramentas,
            text=self.t("Importar Excel/CSV"),
            width=145,
            height=32,
            fg_color=COR_BOTAO_VERDE,
            hover_color=COR_BOTAO_VERDE_HOVER,
            text_color="#080808",
            command=self.importar_cadastros
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            ferramentas,
            text=self.t("Fazer backup"),
            width=120,
            height=32,
            fg_color=COR_BOTAO_VERDE,
            hover_color=COR_BOTAO_VERDE_HOVER,
            text_color="#080808",
            command=self.fazer_backup
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            ferramentas,
            text=self.t("Restaurar backup"),
            width=135,
            height=32,
            fg_color=COR_BOTAO_VERDE,
            hover_color=COR_BOTAO_VERDE_HOVER,
            text_color="#080808",
            command=self.selecionar_backup_para_restaurar
        ).pack(side="left", padx=3)

        # Lista fixa de cards: mantém a paginação e evita a rolagem problemática.
        self.lista = ctk.CTkFrame(
            area_lista,
            fg_color="transparent"
        )
        self.lista.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 4))
        self.lista.grid_columnconfigure(0, weight=1)
        # A lista ocupa exatamente o espaço reservado pelo layout; os cards
        # ajustam sua altura ao tamanho real disponível, sem rolagem.
        self.lista.grid_propagate(False)
        self._cards_pagina = []
        self.lista.bind("<Configure>", self.ajustar_altura_cards, add="+")

        # Navegação entre páginas de cards.
        controles_pagina = ctk.CTkFrame(area_lista, fg_color="transparent")
        controles_pagina.grid(row=3, column=0, sticky="ew", padx=15, pady=(2, 12))
        controles_pagina.grid_columnconfigure(1, weight=1)

        self.btn_pagina_anterior = ctk.CTkButton(
            controles_pagina,
            text="← Anterior",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=self.pagina_anterior
        )
        self.btn_pagina_anterior.grid(row=0, column=0, sticky="w")

        self.lbl_pagina = ctk.CTkLabel(
            controles_pagina,
            text="Página 1 de 1",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=12)
        )
        self.lbl_pagina.grid(row=0, column=1)

        self.btn_proxima_pagina = ctk.CTkButton(
            controles_pagina,
            text="Próxima →",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=self.proxima_pagina
        )
        self.btn_proxima_pagina.grid(row=0, column=2, sticky="e")

        self.atualizar_lista()
        self.traduzir_arvore(self.tela_cadastros)

    def pessoa_filtrada(self):
        pessoas = self.service.listar()

        busca = self.entry_busca.get().strip().upper()
        # Remove o prefixo visual para comparar apenas o valor do filtro.
        filtro_sexo = self.combo_filtro.get().split(": ", 1)[-1]
        filtro_idade = self.combo_idade.get().split(": ", 1)[-1]

        resultado = []

        for pessoa in pessoas:
            if busca and busca not in pessoa["nome"].upper():
                continue

            if filtro_sexo == self.t("Masculino") and pessoa["sexo"] != "M":
                continue

            if filtro_sexo == self.t("Feminino") and pessoa["sexo"] != "F":
                continue

            if filtro_idade == self.t("Menor de 18") and pessoa["idade"] >= 18:
                continue

            if filtro_idade == self.t("18 ou mais") and pessoa["idade"] < 18:
                continue

            if filtro_idade == self.t("60 ou mais") and pessoa["idade"] < 60:
                continue

            resultado.append(pessoa)

        ordenacao = self.combo_ordenacao.get()
        if ordenacao == self.t("Ordenar: Mais recentes"):
            resultado.sort(key=lambda pessoa: pessoa.get("id", 0), reverse=True)
        elif ordenacao == self.t("Ordenar: Nome A-Z"):
            resultado.sort(key=lambda pessoa: pessoa["nome"].casefold())
        elif ordenacao == self.t("Ordenar: Nome Z-A"):
            resultado.sort(key=lambda pessoa: pessoa["nome"].casefold(), reverse=True)
        elif ordenacao == self.t("Ordenar: Menor idade"):
            resultado.sort(key=lambda pessoa: (pessoa["idade"], pessoa["nome"].casefold()))
        elif ordenacao == self.t("Ordenar: Maior idade"):
            resultado.sort(key=lambda pessoa: (pessoa["idade"], pessoa["nome"].casefold()), reverse=True)

        return resultado

    def agendar_busca(self):
        if self._busca_job is not None:
            self.after_cancel(self._busca_job)

        self._busca_job = self.after(250, self.executar_busca)

    def executar_busca(self):
        self._busca_job = None
        self.pagina_atual = 1
        self.atualizar_lista()

    def alterar_filtros(self):
        self.pagina_atual = 1
        self.atualizar_lista()

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.atualizar_lista()

    def proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa somente os cards da página atual; os controles ficam no rodapé.
        for widget in self.lista.winfo_children():
            widget.destroy()
        self._cards_pagina = []

        pessoas = self.pessoa_filtrada()
        total_registros = len(pessoas)

        self.total_paginas = max(
            1,
            (total_registros + self.itens_por_pagina - 1) // self.itens_por_pagina
        )
        self.pagina_atual = min(max(1, self.pagina_atual), self.total_paginas)

        inicio = (self.pagina_atual - 1) * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        pessoas_da_pagina = pessoas[inicio:fim]

        if not pessoas_da_pagina:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum cadastro encontrado.",
                text_color=COR_TEXTO_MUDO
            ).grid(row=0, column=0, pady=50)
        else:
            for linha, pessoa in enumerate(pessoas_da_pagina):
                self.criar_item_pessoa(pessoa, linha)

        self.lbl_pagina.configure(
            text=f"Página {self.pagina_atual} de {self.total_paginas}  •  {total_registros} cadastro(s)"
        )
        self.btn_pagina_anterior.configure(
            state="normal" if self.pagina_atual > 1 else "disabled"
        )
        self.btn_proxima_pagina.configure(
            state="normal" if self.pagina_atual < self.total_paginas else "disabled"
        )
        self.traduzir_arvore(self.lista)
        self.traduzir_arvore(self.lbl_pagina.master)
        # Aguarda o gerenciador geométrico calcular a altura real da lista.
        self.after_idle(self.ajustar_altura_cards)

    def ajustar_altura_cards(self, event=None):
        """Distribui o espaço vertical da lista igualmente entre os cards."""
        cards = getattr(self, "_cards_pagina", [])
        if not cards or not hasattr(self, "lista"):
            return

        altura_lista = event.height if event is not None else self.lista.winfo_height()
        if altura_lista <= 1:
            return

        # Cada card recebe a mesma altura. Os espaços entre eles são
        # descontados antes do cálculo para que o último não fique cortado.
        espacos = len(cards) * 8  # pady=(4, 4) em cada card
        margem_seguranca = 6
        altura_card = int((altura_lista - espacos - margem_seguranca) / len(cards))
        altura_card = max(64, min(92, altura_card))

        for card in cards:
            if card.winfo_exists():
                card.configure(height=altura_card)

    def criar_item_pessoa(self, pessoa, linha):
        # Cards em tamanho intermediário. A altura final é ajustada conforme
        # o espaço disponível, mantendo proporções confortáveis sem rolagem.
        card = ctk.CTkFrame(
            self.lista,
            height=68,
            corner_radius=10,
            fg_color=COR_ITEM
        )
        card.grid(row=linha, column=0, sticky="ew", padx=3, pady=4)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        self._cards_pagina.append(card)

        sexo = self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")

        nascimento = self.nascimento_da_pessoa(pessoa)
        texto_nascimento = (
            nascimento.strftime("%d/%m/%Y") if nascimento
            else self.t("Nascimento não informado")
        )

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.grid(row=0, column=0, sticky="w", padx=16, pady=7)

        ctk.CTkLabel(
            info,
            text=pessoa["nome"],
            height=22,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COR_TEXTO
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=(
                f"{pessoa['idade']} {self.t('anos')}  •  {sexo}  •  "
                f"{self.t('Data de nascimento: ')}{texto_nascimento}"
            ),
            height=19,
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_SEC
        ).pack(anchor="w")

        botoes = ctk.CTkFrame(card, fg_color="transparent")
        botoes.grid(row=0, column=1, padx=12, sticky="e")

        self.criar_botoes_pessoa(botoes, pessoa)

    def criar_botoes_pessoa(self, botoes, pessoa):
        for widget in botoes.winfo_children():
            widget.destroy()

        ctk.CTkButton(
            botoes,
            text="Editar",
            width=70,
            height=32,
            fg_color=COR_BOTAO_SEC,
            hover_color=COR_BOTAO_SEC_HOVER,
            command=lambda: self.editar_pessoa(pessoa)
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            width=70,
            height=32,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            command=lambda: self.pedir_confirmacao_exclusao(botoes, pessoa)
        ).pack(side="left", padx=3)

    def pedir_confirmacao_exclusao(self, botoes, pessoa):
        for widget in botoes.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            botoes,
            text="Excluir?",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text="Sim",
            width=60,
            height=32,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            command=lambda: self.excluir_pessoa(pessoa)
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            botoes,
            text="Não",
            width=60,
            height=32,
            fg_color=COR_BOTAO_SEC,
            hover_color=COR_BOTAO_SEC_HOVER,
            command=lambda: self.criar_botoes_pessoa(botoes, pessoa)
        ).pack(side="left", padx=3)

    def aplicar_mascara_data_nascimento(self, event=None):
        """Insere automaticamente as barras no formato DD/MM/AAAA."""
        if not hasattr(self, "entry_data_nascimento"):
            return

        tecla = getattr(event, "keysym", "") if event else ""
        teclas_de_navegacao = {
            "Left", "Right", "Up", "Down", "Home", "End", "Tab",
            "Shift_L", "Shift_R", "Control_L", "Control_R",
            "Alt_L", "Alt_R", "Caps_Lock", "Escape"
        }
        if tecla in teclas_de_navegacao:
            return

        # Ctrl+A deve manter a seleção; colar (Ctrl+V) continua sendo tratado.
        estado = getattr(event, "state", 0) if event else 0
        if tecla.lower() == "a" and estado & 0x4:
            return

        campo = self.entry_data_nascimento
        texto_atual = campo.get()
        try:
            posicao_atual = campo.index("insert")
        except Exception:
            posicao_atual = len(texto_atual)

        digitos_antes_cursor = sum(
            caractere.isdigit() for caractere in texto_atual[:posicao_atual]
        )
        digitos = re.sub(r"\D", "", texto_atual)[:8]
        digitos_anteriores = getattr(
            self, "_data_nascimento_digitos_anteriores", ""
        )

        # Ao apagar uma barra automática, apaga também o dígito correspondente.
        if tecla == "BackSpace" and digitos == digitos_anteriores and digitos:
            indice = min(max(digitos_antes_cursor - 1, 0), len(digitos) - 1)
            digitos = digitos[:indice] + digitos[indice + 1:]
            digitos_antes_cursor = max(0, digitos_antes_cursor - 1)
        elif tecla == "Delete" and digitos == digitos_anteriores:
            indice = digitos_antes_cursor
            if indice < len(digitos):
                digitos = digitos[:indice] + digitos[indice + 1:]

        if len(digitos) > 4:
            data_formatada = f"{digitos[:2]}/{digitos[2:4]}/{digitos[4:]}"
        elif len(digitos) > 2:
            data_formatada = f"{digitos[:2]}/{digitos[2:]}"
        else:
            data_formatada = digitos

        if data_formatada != texto_atual:
            campo.delete(0, "end")
            campo.insert(0, data_formatada)

        # Reposiciona o cursor após o mesmo número de dígitos, incluindo a barra.
        if digitos_antes_cursor <= 0:
            nova_posicao = 0
        else:
            vistos = 0
            nova_posicao = len(data_formatada)
            for indice, caractere in enumerate(data_formatada):
                if caractere.isdigit():
                    vistos += 1
                    if vistos == digitos_antes_cursor:
                        nova_posicao = indice + 1
                        if (nova_posicao < len(data_formatada)
                                and data_formatada[nova_posicao] == "/"):
                            nova_posicao += 1
                        break

        campo.icursor(nova_posicao)
        self._data_nascimento_digitos_anteriores = digitos

    def validar_formulario(self):
        nome = self.entry_nome.get().strip()
        nascimento_texto = self.entry_data_nascimento.get().strip()
        sexo_visivel = self.combo_sexo.get()
        sexo = "Masculino" if sexo_visivel == self.t("Masculino") else "Feminino"

        ok, mensagem = validar_nome(nome)
        if not ok:
            self.mostrar_aviso(mensagem, "aviso", titulo="Nome inválido")
            return None

        if not nascimento_texto:
            self.mostrar_aviso("A data de nascimento é obrigatória.", "aviso")
            return None
        try:
            nascimento = self.normalizar_data_nascimento(nascimento_texto)
        except ValueError as erro:
            self.mostrar_aviso(str(erro), "aviso")
            return None

        if nascimento > date.today():
            self.mostrar_aviso("A data de nascimento não pode estar no futuro.", "aviso")
            return None

        ok, mensagem = validar_sexo(sexo)
        if not ok:
            self.mostrar_aviso(mensagem, "aviso", titulo="Sexo inválido")
            return None

        return nome, nascimento, self.calcular_idade(nascimento), "M" if sexo == "Masculino" else "F"

    def salvar_cadastro(self):
        dados = self.validar_formulario()
        if not dados:
            return

        nome, nascimento, idade, sexo = dados

        try:
            if self.pessoa_selecionada is None:
                pessoa = self.adicionar_com_nascimento(nome, nascimento, sexo)
                self.registrar_atividade(
                    "Cadastro criado",
                    f"{nome} • {idade} anos • Nascimento: {nascimento.strftime('%d/%m/%Y')}"
                )
                mensagem = "Pessoa cadastrada com sucesso!"
                self.pagina_atual = 1
            else:
                id_pessoa = self.pessoa_selecionada["id"]
                self.service.atualizar(
                    id_pessoa, nome, idade, sexo,
                    data_nascimento=nascimento.isoformat()
                )
                self.dados_nascimento.pop(str(id_pessoa), None)
                self.salvar_dados_nascimento()
                self.registrar_atividade(
                    "Cadastro atualizado",
                    f"ID {id_pessoa} • {nome} • {idade} anos • Nascimento: {nascimento.strftime('%d/%m/%Y')}"
                )
                mensagem = "Cadastro atualizado com sucesso!"
        except Exception as erro:
            self.mostrar_aviso(
                f"Não foi possível salvar o cadastro: {erro}",
                "erro",
                titulo="Falha ao salvar"
            )
            return

        self.limpar_formulario()
        self.atualizar_lista()
        self.mostrar_aviso(mensagem, "sucesso")

    def editar_pessoa(self, pessoa):
        self.pessoa_selecionada = pessoa

        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, pessoa["nome"])

        self.entry_data_nascimento.delete(0, "end")
        nascimento = self.nascimento_da_pessoa(pessoa)
        if nascimento:
            self.entry_data_nascimento.insert(0, nascimento.strftime("%d/%m/%Y"))
        self._data_nascimento_digitos_anteriores = re.sub(
            r"\D", "", self.entry_data_nascimento.get()
        )

        self.combo_sexo.set(
            self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")
        )

        self.btn_salvar.configure(text=self.t("Salvar alterações"))
        self.lbl_edicao.configure(
            text=self.t("Modo: editando cadastro #") + str(pessoa['id']),
            text_color=COR_DESTAQUE
        )
        if not nascimento:
            self.mostrar_aviso(
                "Este cadastro antigo não tem data de nascimento. Informe-a para atualizar.",
                "aviso"
            )

    def excluir_pessoa(self, pessoa):
        try:
            self.mover_para_lixeira(pessoa)
        except Exception as erro:
            self.mostrar_aviso(
                f"Não foi possível mover o cadastro para a lixeira: {erro}",
                "erro"
            )
            return
        self.registrar_atividade(
            "Cadastro movido para a lixeira",
            f"ID {pessoa['id']} • {pessoa['nome']}"
        )
        self.limpar_formulario()
        self.atualizar_lista()
        self.mostrar_aviso(f"Cadastro de {pessoa['nome']} movido para a lixeira.", "sucesso")

    def pedir_confirmacao_exclusao_todos(self):
        pessoas = self.service.listar()

        if not pessoas:
            self.mostrar_aviso("Não há cadastros para excluir.", "aviso")
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Excluir todos os cadastros")
        janela.geometry("420x220")
        janela.resizable(False, False)
        janela.configure(fg_color=COR_CARD)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Mover todos para a lixeira?",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COR_TEXTO
        ).pack(padx=24, pady=(24, 8))

        ctk.CTkLabel(
            janela,
            text=(
                f"Você está prestes a mover {len(pessoas)} cadastro(s) para a lixeira.\n"
                "Eles poderão ser restaurados pela tela Lixeira."
            ),
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_CORPO,
            justify="center"
        ).pack(padx=24, pady=8)

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(fill="x", padx=24, pady=(12, 20))
        botoes.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            height=38,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=janela.destroy
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text="Mover todos para a lixeira",
            height=38,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            text_color="#ffffff",
            command=lambda: self.excluir_todos_cadastros(pessoas, janela)
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        janela.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - janela.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - janela.winfo_height()) // 2
        janela.geometry(f"+{x}+{y}")
        self.traduzir_arvore(janela)
        janela.title(self.t("Excluir todos os cadastros"))
        janela.focus_force()

    def excluir_todos_cadastros(self, pessoas, janela):
        janela.destroy()

        # Cancela uma busca agendada para evitar atualização durante a exclusão.
        if self._busca_job is not None:
            try:
                self.after_cancel(self._busca_job)
            except Exception:
                pass
            self._busca_job = None

        movidos = 0
        try:
            for pessoa in pessoas:
                self.mover_para_lixeira(pessoa)
                movidos += 1
        except Exception as erro:
            self.pagina_atual = 1
            self.limpar_formulario()
            self.atualizar_lista()
            self.mostrar_aviso(
                f"Foram movidos {movidos} cadastro(s). Ocorreu um erro: {erro}",
                "erro",
                titulo="Não foi possível concluir"
            )
            return

        self.registrar_atividade(
            "Exclusão em massa",
            f"{len(pessoas)} cadastro(s) movido(s) para a lixeira"
        )
        self.pagina_atual = 1
        self.limpar_formulario()
        self.entry_busca.delete(0, "end")
        self.combo_filtro.set(self.t("Sexo: Todos"))
        self.combo_idade.set(self.t("Idade: Todas"))
        self.atualizar_lista()
        self.mostrar_aviso(
            f"{len(pessoas)} cadastro(s) movido(s) para a lixeira com sucesso!",
            "sucesso"
        )

    def limpar_formulario(self):
        self.pessoa_selecionada = None

        self.entry_nome.delete(0, "end")
        self.entry_data_nascimento.delete(0, "end")
        self._data_nascimento_digitos_anteriores = ""
        self.combo_sexo.set(self.t("Masculino"))
        self.btn_salvar.configure(text=self.t("Cadastrar pessoa"))
        self.lbl_edicao.configure(
            text=self.t("Modo: novo cadastro"),
            text_color=COR_TEXTO_MUDO
        )

    # ----------------------------
    # RELATÓRIOS
    # ----------------------------

    def mostrar_relatorios(self):
        self.tela_ativa = "relatorios"
        self.limpar_conteudo()
        self.marcar_menu("relatorios")
        self.titulo_pagina(
            "Relatórios",
            "Consulte a relação completa de pessoas e exporte os dados"
        )

        self.pagina_relatorio = 1
        area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area.grid(row=1, column=0, sticky="nsew", padx=35, pady=5)
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(2, weight=1)

        pessoas = self.service.listar()

        # Cabeçalho do relatório: total de registros e exportação CSV.
        topo_relatorio = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        topo_relatorio.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        topo_relatorio.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topo_relatorio,
            text=f"{len(pessoas)} cadastro(s) encontrados",
            text_color=COR_TEXTO,
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=14)

        botoes_exportacao = ctk.CTkFrame(topo_relatorio, fg_color="transparent")
        botoes_exportacao.grid(row=0, column=1, sticky="e", padx=12, pady=9)

        ctk.CTkButton(
            botoes_exportacao,
            text="Exportar CSV",
            width=112,
            height=36,
            fg_color=COR_DESTAQUE,
            hover_color=COR_DESTAQUE_HOVER,
            text_color=COR_TEXTO_NO_DESTAQUE,
            command=self.exportar_relatorio_csv
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            botoes_exportacao,
            text="Exportar Excel",
            width=122,
            height=36,
            fg_color=COR_DESTAQUE,
            hover_color=COR_DESTAQUE_HOVER,
            text_color=COR_TEXTO_NO_DESTAQUE,
            command=self.exportar_relatorio_excel
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            botoes_exportacao,
            text="Exportar PDF",
            width=112,
            height=36,
            fg_color=COR_DESTAQUE,
            hover_color=COR_DESTAQUE_HOVER,
            text_color=COR_TEXTO_NO_DESTAQUE,
            command=self.exportar_relatorio_pdf
        ).pack(side="left", padx=3)

        ctk.CTkLabel(
            area,
            text="Relação detalhada de cadastros",
            text_color=COR_TEXTO,
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=1, column=0, sticky="w", pady=(2, 8))

        tabela = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        tabela.grid(row=2, column=0, sticky="nsew")
        tabela.grid_columnconfigure(0, weight=1)
        tabela.grid_rowconfigure(1, weight=1)

        cabecalho = ctk.CTkFrame(tabela, fg_color="#292929", corner_radius=8)
        cabecalho.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.configurar_colunas_relatorio(cabecalho)
        self.adicionar_celula_relatorio(cabecalho, "ID", 0, peso="bold")
        self.adicionar_celula_relatorio(cabecalho, "NOME", 1, peso="bold")
        self.adicionar_celula_relatorio(cabecalho, "IDADE", 2, peso="bold")
        self.adicionar_celula_relatorio(cabecalho, "SEXO", 3, peso="bold")
        self.adicionar_celula_relatorio(cabecalho, "NASCIMENTO", 4, peso="bold")

        self.corpo_relatorio = ctk.CTkFrame(tabela, fg_color="transparent")
        self.corpo_relatorio.grid(row=1, column=0, sticky="nsew", padx=10, pady=2)
        self.corpo_relatorio.grid_columnconfigure(0, weight=1)

        rodape = ctk.CTkFrame(tabela, fg_color="transparent")
        rodape.grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 10))
        rodape.grid_columnconfigure(1, weight=1)

        self.btn_relatorio_anterior = ctk.CTkButton(
            rodape,
            text="← Anterior",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_relatorio(-1)
        )
        self.btn_relatorio_anterior.grid(row=0, column=0, sticky="w")

        self.lbl_pagina_relatorio = ctk.CTkLabel(
            rodape,
            text="Página 1 de 1",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=12)
        )
        self.lbl_pagina_relatorio.grid(row=0, column=1)

        self.btn_relatorio_proxima = ctk.CTkButton(
            rodape,
            text="Próxima →",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_relatorio(1)
        )
        self.btn_relatorio_proxima.grid(row=0, column=2, sticky="e")

        self.atualizar_tabela_relatorio()
        self.traduzir_arvore(self.conteudo)

    def configurar_colunas_relatorio(self, parent):
        parent.grid_columnconfigure(0, weight=0, minsize=55)
        parent.grid_columnconfigure(1, weight=1, minsize=190)
        parent.grid_columnconfigure(2, weight=0, minsize=75)
        parent.grid_columnconfigure(3, weight=0, minsize=110)
        parent.grid_columnconfigure(4, weight=0, minsize=130)

    def adicionar_celula_relatorio(self, parent, texto, coluna, peso="normal"):
        label = ctk.CTkLabel(
            parent,
            text=str(texto),
            text_color=COR_TEXTO if peso == "bold" else COR_TEXTO_CORPO,
            font=ctk.CTkFont(size=12, weight=peso),
            anchor="w"
        )
        label.grid(
            row=0,
            column=coluna,
            sticky="ew",
            padx=(12 if coluna == 0 else 8, 8),
            pady=10
        )

    def atualizar_tabela_relatorio(self):
        for widget in self.corpo_relatorio.winfo_children():
            widget.destroy()

        pessoas = sorted(self.service.listar(), key=lambda pessoa: pessoa.get("id", 0))
        total = len(pessoas)
        total_paginas = max(
            1,
            (total + self.itens_por_pagina_relatorio - 1) // self.itens_por_pagina_relatorio
        )
        self.pagina_relatorio = min(max(1, self.pagina_relatorio), total_paginas)

        inicio = (self.pagina_relatorio - 1) * self.itens_por_pagina_relatorio
        fim = inicio + self.itens_por_pagina_relatorio
        pessoas_pagina = pessoas[inicio:fim]

        if not pessoas_pagina:
            ctk.CTkLabel(
                self.corpo_relatorio,
                text="Nenhum cadastro disponível para exibir.",
                text_color=COR_TEXTO_MUDO,
                font=ctk.CTkFont(size=13)
            ).grid(row=0, column=0, sticky="ew", pady=35)
        else:
            for indice, pessoa in enumerate(pessoas_pagina):
                linha = ctk.CTkFrame(
                    self.corpo_relatorio,
                    fg_color=COR_ITEM if indice % 2 == 0 else COR_CARD,
                    corner_radius=7
                )
                linha.grid(row=indice, column=0, sticky="ew", pady=2)
                self.configurar_colunas_relatorio(linha)

                sexo = self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")
                self.adicionar_celula_relatorio(linha, pessoa["id"], 0)
                self.adicionar_celula_relatorio(linha, pessoa["nome"], 1)
                self.adicionar_celula_relatorio(linha, f"{pessoa['idade']} anos", 2)
                self.adicionar_celula_relatorio(linha, sexo, 3)
                nascimento = self.nascimento_da_pessoa(pessoa)
                texto_nascimento = nascimento.strftime("%d/%m/%Y") if nascimento else "—"
                self.adicionar_celula_relatorio(linha, texto_nascimento, 4)

        self.lbl_pagina_relatorio.configure(
            text=f"Página {self.pagina_relatorio} de {total_paginas}  •  {total} cadastro(s)"
        )
        self.btn_relatorio_anterior.configure(
            state="normal" if self.pagina_relatorio > 1 else "disabled"
        )
        self.btn_relatorio_proxima.configure(
            state="normal" if self.pagina_relatorio < total_paginas else "disabled"
        )
        self.traduzir_arvore(self.corpo_relatorio)
        self.traduzir_arvore(self.lbl_pagina_relatorio.master)

    def mudar_pagina_relatorio(self, direcao):
        # Recalcula o limite antes de navegar, evitando avançar além da última página.
        total_registros = len(self.service.listar())
        total_paginas = max(
            1,
            (total_registros + self.itens_por_pagina_relatorio - 1)
            // self.itens_por_pagina_relatorio
        )

        nova_pagina = self.pagina_relatorio + direcao
        if 1 <= nova_pagina <= total_paginas:
            self.pagina_relatorio = nova_pagina
            self.atualizar_tabela_relatorio()

    def exportar_relatorio_csv(self):
        pessoas = sorted(self.service.listar(), key=lambda pessoa: pessoa.get("id", 0))
        if not pessoas:
            self.mostrar_aviso("Não há cadastros para exportar.", "aviso")
            return

        caminho = filedialog.asksaveasfilename(
            parent=self,
            title=self.t("Salvar relatório de cadastros"),
            initialfile="relatorio_cadastros.csv",
            defaultextension=".csv",
            filetypes=[(self.t("Arquivo CSV"), "*.csv")]
        )
        if not caminho:
            return

        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.writer(arquivo, delimiter=";")
                escritor.writerow([
                    self.t("ID"), self.t("Nome"), self.t("Idade"),
                    self.t("Sexo"), self.t("Data de nascimento")
                ])

                for pessoa in pessoas:
                    sexo = self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")
                    nascimento = self.nascimento_da_pessoa(pessoa)
                    escritor.writerow([
                        pessoa["id"], pessoa["nome"], pessoa["idade"], sexo,
                        nascimento.strftime("%d/%m/%Y") if nascimento else ""
                    ])
        except OSError as erro:
            self.mostrar_aviso(
                f"Não foi possível salvar o arquivo: {erro}",
                "erro",
                titulo="Falha na exportação"
            )
            return

        self.registrar_atividade(
            "Relatório CSV exportado",
            f"{len(pessoas)} cadastro(s) • {Path(caminho).name}"
        )
        self.mostrar_aviso(
            f"Relatório exportado com {len(pessoas)} cadastro(s).",
            "sucesso",
            titulo="Exportação concluída"
        )

    def exportar_relatorio_excel(self):
        """Gera uma planilha XLSX formatada com todos os cadastros."""
        pessoas = sorted(self.service.listar(), key=lambda pessoa: pessoa.get("id", 0))
        if not pessoas:
            self.mostrar_aviso("Não há cadastros para exportar.", "aviso")
            return

        caminho = filedialog.asksaveasfilename(
            parent=self,
            title=self.t("Salvar relatório em Excel"),
            initialfile="relatorio_cadastros.xlsx",
            defaultextension=".xlsx",
            filetypes=[(self.t("Planilha Excel"), "*.xlsx")]
        )
        if not caminho:
            return

        try:
            from openpyxl import Workbook
            from openpyxl.styles import Alignment, Font, PatternFill

            workbook = Workbook()
            planilha = workbook.active
            planilha.title = self.t("Cadastros")
            planilha.append([
                self.t("ID"), self.t("Nome"), self.t("Idade"),
                self.t("Sexo"), self.t("Data de nascimento")
            ])

            for pessoa in pessoas:
                sexo = self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")
                nascimento = self.nascimento_da_pessoa(pessoa)
                planilha.append([
                    pessoa["id"], pessoa["nome"], pessoa["idade"], sexo,
                    nascimento.strftime("%d/%m/%Y") if nascimento else ""
                ])

            preenchimento_cabecalho = PatternFill("solid", fgColor="166534")
            for celula in planilha[1]:
                celula.fill = preenchimento_cabecalho
                celula.font = Font(color="FFFFFF", bold=True)
                celula.alignment = Alignment(horizontal="center")

            planilha.column_dimensions["A"].width = 12
            planilha.column_dimensions["B"].width = 38
            planilha.column_dimensions["C"].width = 14
            planilha.column_dimensions["D"].width = 18
            planilha.column_dimensions["E"].width = 22
            planilha.freeze_panes = "A2"
            planilha.auto_filter.ref = planilha.dimensions

            workbook.save(caminho)
        except ImportError:
            self.mostrar_aviso(
                "Para exportar Excel, instale a dependência: python -m pip install openpyxl",
                "aviso",
                titulo="Biblioteca necessária"
            )
            return
        except (OSError, ValueError) as erro:
            self.mostrar_aviso(
                f"Não foi possível gerar a planilha: {erro}",
                "erro",
                titulo="Falha na exportação"
            )
            return

        self.registrar_atividade(
            "Relatório Excel exportado",
            f"{len(pessoas)} cadastro(s) • {Path(caminho).name}"
        )
        self.mostrar_aviso(
            f"Planilha exportada com {len(pessoas)} cadastro(s).",
            "sucesso",
            titulo="Exportação concluída"
        )

    def exportar_relatorio_pdf(self):
        """Gera um PDF em formato paisagem com a relação de cadastros."""
        pessoas = sorted(self.service.listar(), key=lambda pessoa: pessoa.get("id", 0))
        if not pessoas:
            self.mostrar_aviso("Não há cadastros para exportar.", "aviso")
            return

        caminho = filedialog.asksaveasfilename(
            parent=self,
            title=self.t("Salvar relatório em PDF"),
            initialfile="relatorio_cadastros.pdf",
            defaultextension=".pdf",
            filetypes=[(self.t("Arquivo PDF"), "*.pdf")]
        )
        if not caminho:
            return

        try:
            from xml.sax.saxutils import escape
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import mm
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

            documento = SimpleDocTemplate(
                caminho,
                pagesize=landscape(A4),
                rightMargin=15 * mm,
                leftMargin=15 * mm,
                topMargin=15 * mm,
                bottomMargin=15 * mm
            )
            estilos = getSampleStyleSheet()
            conteudo = [
                Paragraph(self.t("Relatório de Cadastros"), estilos["Title"]),
                Paragraph(self.t("Total de registros: ") + str(len(pessoas)), estilos["Normal"]),
                Spacer(1, 8 * mm)
            ]

            dados_tabela = [[
                self.t("ID"), self.t("Nome"), self.t("Idade"),
                self.t("Sexo"), self.t("Data de nascimento")
            ]]
            for pessoa in pessoas:
                sexo = self.t("Masculino") if pessoa["sexo"] == "M" else self.t("Feminino")
                nascimento = self.nascimento_da_pessoa(pessoa)
                dados_tabela.append([
                    str(pessoa["id"]),
                    Paragraph(escape(str(pessoa["nome"])), estilos["BodyText"]),
                    f"{pessoa['idade']} {self.t('anos')}",
                    sexo,
                    nascimento.strftime("%d/%m/%Y") if nascimento else "—"
                ])

            tabela = Table(
                dados_tabela,
                colWidths=[20 * mm, 115 * mm, 25 * mm, 35 * mm, 40 * mm],
                repeatRows=1
            )
            tabela.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#166534")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ]))
            conteudo.append(tabela)
            documento.build(conteudo)
        except ImportError:
            self.mostrar_aviso(
                "Para exportar PDF, instale a dependência: python -m pip install reportlab",
                "aviso",
                titulo="Biblioteca necessária"
            )
            return
        except (OSError, ValueError) as erro:
            self.mostrar_aviso(
                f"Não foi possível gerar o PDF: {erro}",
                "erro",
                titulo="Falha na exportação"
            )
            return

        self.registrar_atividade(
            "Relatório PDF exportado",
            f"{len(pessoas)} cadastro(s) • {Path(caminho).name}"
        )
        self.mostrar_aviso(
            f"PDF exportado com {len(pessoas)} cadastro(s).",
            "sucesso",
            titulo="Exportação concluída"
        )

    # ----------------------------
    # IMPORTAÇÃO EXCEL / CSV
    # ----------------------------

    @staticmethod
    def normalizar_cabecalho(valor):
        texto = unicodedata.normalize("NFKD", str(valor or ""))
        texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
        return re.sub(r"[^a-z0-9]", "", texto.lower())

    def ler_arquivo_importacao(self, caminho):
        extensao = Path(caminho).suffix.lower()
        if extensao == ".csv":
            try:
                with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
                    amostra = arquivo.read(4096)
                    arquivo.seek(0)
                    try:
                        delimitador = csv.Sniffer().sniff(amostra, delimiters=";,\t").delimiter
                    except csv.Error:
                        delimitador = ";"
                    return list(csv.DictReader(arquivo, delimiter=delimitador))
            except UnicodeDecodeError:
                with open(caminho, "r", encoding="latin-1", newline="") as arquivo:
                    amostra = arquivo.read(4096)
                    arquivo.seek(0)
                    try:
                        delimitador = csv.Sniffer().sniff(amostra, delimiters=";,\t").delimiter
                    except csv.Error:
                        delimitador = ";"
                    return list(csv.DictReader(arquivo, delimiter=delimitador))

        if extensao in {".xlsx", ".xlsm"}:
            from openpyxl import load_workbook
            workbook = load_workbook(caminho, read_only=True, data_only=True)
            planilha = workbook.active
            linhas = planilha.iter_rows(values_only=True)
            cabecalhos = next(linhas, None)
            if not cabecalhos:
                workbook.close()
                return []
            resultado = []
            for valores in linhas:
                if not any(valor is not None and str(valor).strip() for valor in valores):
                    continue
                resultado.append(dict(zip(cabecalhos, valores)))
            workbook.close()
            return resultado

        raise ValueError("Formato não suportado. Escolha CSV ou Excel (.xlsx).")

    def obter_valor_coluna(self, linha, nomes_aceitos):
        procurados = {self.normalizar_cabecalho(nome) for nome in nomes_aceitos}
        for chave, valor in linha.items():
            if self.normalizar_cabecalho(chave) in procurados:
                return valor
        return None

    def normalizar_sexo_importado(self, valor):
        texto = self.normalizar_cabecalho(valor)
        if texto in {"m", "masculino", "male", "hombre", "homem"}:
            return "M"
        if texto in {"f", "feminino", "female", "mujer", "mulher"}:
            return "F"
        raise ValueError("Sexo inválido. Use Masculino/Feminino ou M/F.")

    def importar_cadastros(self):
        caminho = filedialog.askopenfilename(
            parent=self,
            title=self.t("Selecione um arquivo Excel ou CSV"),
            filetypes=[
                (self.t("Arquivo CSV ou Excel"), "*.csv *.xlsx *.xlsm"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx *.xlsm"),
            ]
        )
        if not caminho:
            return

        try:
            linhas = self.ler_arquivo_importacao(caminho)
        except ImportError:
            self.mostrar_aviso(
                "Para importar Excel, instale: python -m pip install openpyxl",
                "aviso",
                titulo="Biblioteca necessária"
            )
            return
        except Exception as erro:
            self.mostrar_aviso(str(erro), "erro", titulo="Falha na importação")
            return

        if not linhas:
            self.mostrar_aviso("Nenhum registro válido foi encontrado no arquivo.", "aviso")
            return

        colunas = {self.normalizar_cabecalho(k) for k in linhas[0].keys()}
        aliases_nome = {"nome", "nomecompleto", "name", "fullname"}
        aliases_data = {"datanascimento", "datadenascimento", "nascimento", "birthdate", "dateofbirth", "fechadenacimiento"}
        aliases_idade = {"idade", "age", "edad"}
        aliases_sexo = {"sexo", "gender", "genero"}
        if not (colunas & aliases_nome and colunas & aliases_sexo and (colunas & aliases_data or colunas & aliases_idade)):
            self.mostrar_aviso(
                "O arquivo precisa conter as colunas Nome, Data de nascimento e Sexo.",
                "aviso"
            )
            return

        importados = 0
        erros = []
        for numero_linha, linha in enumerate(linhas, start=2):
            try:
                nome = str(self.obter_valor_coluna(
                    linha, ("Nome", "Nome completo", "Name", "Full name")
                ) or "").strip()
                nascimento_valor = self.obter_valor_coluna(
                    linha, ("Data de nascimento", "Nascimento", "Birth date", "Date of birth", "Fecha de nacimiento")
                )
                idade_valor = self.obter_valor_coluna(linha, ("Idade", "Age", "Edad"))
                sexo = self.normalizar_sexo_importado(
                    self.obter_valor_coluna(linha, ("Sexo", "Gender", "Gênero"))
                )
                ok, mensagem = validar_nome(nome)
                if not ok:
                    raise ValueError(mensagem)

                if nascimento_valor not in (None, ""):
                    # O openpyxl normalmente converte datas com formatação de data;
                    # também aceitamos números seriais do Excel para planilhas simples.
                    if isinstance(nascimento_valor, (int, float)) and not isinstance(nascimento_valor, bool):
                        from openpyxl.utils.datetime import from_excel
                        nascimento_valor = from_excel(nascimento_valor).date()
                    nascimento = self.normalizar_data_nascimento(nascimento_valor)
                    if nascimento > date.today():
                        raise ValueError("A data de nascimento não pode estar no futuro.")
                    self.adicionar_com_nascimento(nome, nascimento, sexo)
                else:
                    # Compatibilidade com planilhas antigas exportadas antes do campo de nascimento.
                    if idade_valor in (None, ""):
                        raise ValueError("Informe a data de nascimento ou a idade na planilha.")
                    idade_numerica = float(str(idade_valor).replace(",", "."))
                    if not idade_numerica.is_integer():
                        raise ValueError("A idade precisa ser um número inteiro.")
                    idade = int(idade_numerica)
                    ok, mensagem = validar_idade(str(idade))
                    if not ok:
                        raise ValueError(mensagem)
                    self.service.adicionar(nome, idade, sexo)
                importados += 1
            except Exception as erro:
                erros.append(f"Linha {numero_linha}: {erro}")

        if importados:
            self.registrar_atividade(
                "Importação de cadastros",
                f"{importados} cadastro(s) importado(s) • {Path(caminho).name}"
            )
            self.pagina_atual = 1
            self.atualizar_lista()
            resumo = f"Importados: {importados}  •  Ignorados: {len(erros)}"
            if erros:
                resumo += "\n" + "\n".join(erros[:5])
            self.mostrar_aviso(resumo, "sucesso" if not erros else "aviso", titulo="Importação concluída")
        else:
            resumo = "\n".join(erros[:6]) if erros else "Nenhum registro válido foi encontrado no arquivo."
            self.mostrar_aviso(resumo, "erro", titulo="Falha na importação")

    # ----------------------------
    # LIXEIRA
    # ----------------------------

    def mostrar_lixeira(self):
        self.tela_ativa = "lixeira"
        self.limpar_conteudo()
        self.marcar_menu("lixeira")
        self.titulo_pagina(
            "Lixeira",
            "Cadastros excluídos ficam disponíveis aqui para restauração ou exclusão permanente"
        )

        area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area.grid(row=1, column=0, sticky="nsew", padx=35, pady=5)
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        topo.grid_columnconfigure(0, weight=1)
        self.lbl_total_lixeira = ctk.CTkLabel(
            topo, text="0 cadastro(s) na lixeira", text_color=COR_TEXTO,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_total_lixeira.grid(row=0, column=0, sticky="w", padx=18, pady=14)
        self.btn_esvaziar_lixeira = ctk.CTkButton(
            topo, text="Esvaziar lixeira", width=145, height=36,
            fg_color=COR_PERIGO, hover_color=COR_PERIGO_HOVER,
            text_color="#ffffff", command=self.confirmar_esvaziar_lixeira
        )
        self.btn_esvaziar_lixeira.grid(row=0, column=1, sticky="e", padx=14, pady=9)

        self.area_itens_lixeira = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        self.area_itens_lixeira.grid(row=1, column=0, sticky="nsew")
        self.area_itens_lixeira.grid_columnconfigure(0, weight=1)
        self.corpo_lixeira = ctk.CTkFrame(self.area_itens_lixeira, fg_color="transparent")
        self.corpo_lixeira.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.corpo_lixeira.grid_columnconfigure(0, weight=1)

        rodape = ctk.CTkFrame(self.area_itens_lixeira, fg_color="transparent")
        rodape.grid(row=1, column=0, sticky="ew", padx=15, pady=(2, 12))
        rodape.grid_columnconfigure(1, weight=1)
        self.btn_lixeira_anterior = ctk.CTkButton(
            rodape, text="← Anterior", width=105, height=32,
            fg_color=COR_BOTAO_NEUTRO, hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_lixeira(-1)
        )
        self.btn_lixeira_anterior.grid(row=0, column=0, sticky="w")
        self.lbl_pagina_lixeira = ctk.CTkLabel(
            rodape, text="Página 1 de 1", text_color=COR_TEXTO_SEC
        )
        self.lbl_pagina_lixeira.grid(row=0, column=1)
        self.btn_lixeira_proxima = ctk.CTkButton(
            rodape, text="Próxima →", width=105, height=32,
            fg_color=COR_BOTAO_NEUTRO, hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_lixeira(1)
        )
        self.btn_lixeira_proxima.grid(row=0, column=2, sticky="e")

        self.atualizar_lista_lixeira()
        self.traduzir_arvore(self.conteudo)

    def atualizar_lista_lixeira(self):
        if not hasattr(self, "corpo_lixeira") or not self.corpo_lixeira.winfo_exists():
            return
        for widget in self.corpo_lixeira.winfo_children():
            widget.destroy()

        total = len(self.lixeira_cadastros)
        paginas = max(1, (total + self.itens_por_pagina_lixeira - 1) // self.itens_por_pagina_lixeira)
        self.pagina_lixeira = min(max(1, self.pagina_lixeira), paginas)
        inicio = (self.pagina_lixeira - 1) * self.itens_por_pagina_lixeira
        registros = self.lixeira_cadastros[inicio:inicio + self.itens_por_pagina_lixeira]

        if not registros:
            ctk.CTkLabel(
                self.corpo_lixeira, text="A lixeira está vazia.",
                text_color=COR_TEXTO_MUDO, font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, pady=55)
        else:
            for indice, registro in enumerate(registros):
                card = ctk.CTkFrame(
                    self.corpo_lixeira, corner_radius=10,
                    fg_color=COR_ITEM if indice % 2 == 0 else COR_CARD
                )
                card.grid(row=indice, column=0, sticky="ew", padx=3, pady=5)
                card.grid_columnconfigure(0, weight=1)
                info = ctk.CTkFrame(card, fg_color="transparent")
                info.grid(row=0, column=0, sticky="w", padx=15, pady=10)
                ctk.CTkLabel(
                    info, text=registro.get("nome", ""),
                    font=ctk.CTkFont(size=14, weight="bold"), text_color=COR_TEXTO
                ).pack(anchor="w")
                sexo = self.t("Masculino") if registro.get("sexo") == "M" else self.t("Feminino")
                nascimento_valor = registro.get("data_nascimento")
                try:
                    nascimento = self.normalizar_data_nascimento(nascimento_valor).strftime("%d/%m/%Y") if nascimento_valor else self.t("Nascimento não informado")
                except ValueError:
                    nascimento = self.t("Nascimento não informado")
                detalhe = f"{registro.get('idade', '—')} anos • {sexo} • {nascimento}"
                ctk.CTkLabel(
                    info, text=detalhe, font=ctk.CTkFont(size=11), text_color=COR_TEXTO_SEC
                ).pack(anchor="w", pady=(3, 0))
                botoes = ctk.CTkFrame(card, fg_color="transparent")
                botoes.grid(row=0, column=1, padx=10)
                ctk.CTkButton(
                    botoes, text="Restaurar", width=82, height=31,
                    fg_color=COR_DESTAQUE, hover_color=COR_DESTAQUE_HOVER,
                    text_color=COR_TEXTO_NO_DESTAQUE,
                    command=lambda r=registro: self.restaurar_cadastro_lixeira(r)
                ).pack(side="left", padx=3)
                ctk.CTkButton(
                    botoes, text="Excluir permanentemente", width=150, height=31,
                    fg_color=COR_PERIGO, hover_color=COR_PERIGO_HOVER,
                    text_color="#ffffff",
                    command=lambda r=registro: self.confirmar_exclusao_permanente(r)
                ).pack(side="left", padx=3)

        self.lbl_total_lixeira.configure(text=f"{total} cadastro(s) na lixeira")
        self.lbl_pagina_lixeira.configure(text=f"Página {self.pagina_lixeira} de {paginas}")
        self.btn_lixeira_anterior.configure(state="normal" if self.pagina_lixeira > 1 else "disabled")
        self.btn_lixeira_proxima.configure(state="normal" if self.pagina_lixeira < paginas else "disabled")
        self.btn_esvaziar_lixeira.configure(state="normal" if total else "disabled")
        self.traduzir_arvore(self.corpo_lixeira)
        self.traduzir_arvore(self.lbl_pagina_lixeira.master)

    def mudar_pagina_lixeira(self, direcao):
        paginas = max(1, (len(self.lixeira_cadastros) + self.itens_por_pagina_lixeira - 1) // self.itens_por_pagina_lixeira)
        nova = self.pagina_lixeira + direcao
        if 1 <= nova <= paginas:
            self.pagina_lixeira = nova
            self.atualizar_lista_lixeira()

    def restaurar_cadastro_lixeira(self, registro):
        try:
            nascimento = self.normalizar_data_nascimento(registro["data_nascimento"]) if registro.get("data_nascimento") else None
            sexo = registro.get("sexo")
            if sexo not in {"M", "F"}:
                raise ValueError("Sexo salvo na lixeira é inválido.")
            idade = self.calcular_idade(nascimento) if nascimento else int(registro.get("idade", 0))
            nome = str(registro.get("nome", "")).strip()
            self.adicionar_com_nascimento(nome, nascimento, sexo) if nascimento else self.service.adicionar(nome, idade, sexo)
            # Sem data de nascimento, preserva a idade que já estava salva no registro.
            self.lixeira_cadastros = [
                item for item in self.lixeira_cadastros
                if item.get("chave_lixeira") != registro.get("chave_lixeira")
            ]
            self.salvar_lixeira()
        except Exception as erro:
            self.mostrar_aviso(f"Não foi possível restaurar: {erro}", "erro")
            return

        self.registrar_atividade("Cadastro restaurado", nome)
        self.pagina_lixeira = 1
        self.atualizar_lista_lixeira()
        self.atualizar_lista()
        self.mostrar_aviso("Cadastro restaurado com sucesso.", "sucesso")

    def confirmar_exclusao_permanente(self, registro):
        janela = ctk.CTkToplevel(self)
        janela.title(self.t("Excluir permanentemente"))
        janela.geometry("420x190")
        janela.resizable(False, False)
        janela.configure(fg_color=COR_CARD)
        janela.transient(self)
        janela.grab_set()
        ctk.CTkLabel(
            janela, text=f"Excluir permanentemente {registro.get('nome', '')}?",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO
        ).pack(padx=20, pady=(25, 15))
        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(fill="x", padx=22, pady=15)
        ctk.CTkButton(
            botoes, text="Cancelar", fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER, command=janela.destroy
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(
            botoes, text="Excluir permanentemente", fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            command=lambda: self.excluir_permanentemente(registro, janela)
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))
        self.traduzir_arvore(janela)
        self.centralizar_janela(janela)

    def excluir_permanentemente(self, registro, janela):
        lixeira_anterior = list(self.lixeira_cadastros)
        self.lixeira_cadastros = [
            item for item in self.lixeira_cadastros
            if item.get("chave_lixeira") != registro.get("chave_lixeira")
        ]
        try:
            self.salvar_lixeira()
        except OSError as erro:
            self.lixeira_cadastros = lixeira_anterior
            self.mostrar_aviso(str(erro), "erro")
            return
        janela.destroy()
        self.registrar_atividade("Cadastro excluído permanentemente", registro.get("nome", ""))
        self.atualizar_lista_lixeira()
        self.mostrar_aviso("Cadastro removido permanentemente.", "sucesso")

    def confirmar_esvaziar_lixeira(self):
        if not self.lixeira_cadastros:
            self.mostrar_aviso("A lixeira está vazia.", "aviso")
            return
        janela = ctk.CTkToplevel(self)
        janela.title(self.t("Esvaziar lixeira"))
        janela.geometry("420x190")
        janela.resizable(False, False)
        janela.configure(fg_color=COR_CARD)
        janela.transient(self)
        janela.grab_set()
        ctk.CTkLabel(
            janela, text="Deseja esvaziar a lixeira? Essa ação é permanente.",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=COR_TEXTO,
            wraplength=360
        ).pack(padx=20, pady=(25, 15))
        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(fill="x", padx=22, pady=15)
        ctk.CTkButton(
            botoes, text="Cancelar", fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER, command=janela.destroy
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(
            botoes, text="Esvaziar lixeira", fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            command=lambda: self.esvaziar_lixeira(janela)
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))
        self.traduzir_arvore(janela)
        self.centralizar_janela(janela)

    def esvaziar_lixeira(self, janela):
        lixeira_anterior = list(self.lixeira_cadastros)
        self.lixeira_cadastros.clear()
        try:
            self.salvar_lixeira()
        except OSError as erro:
            self.lixeira_cadastros = lixeira_anterior
            self.mostrar_aviso(str(erro), "erro")
            return
        janela.destroy()
        self.registrar_atividade("Lixeira esvaziada", "Todos os itens removidos permanentemente")
        self.pagina_lixeira = 1
        self.atualizar_lista_lixeira()
        self.mostrar_aviso("Lixeira esvaziada com sucesso.", "sucesso")

    # ----------------------------
    # BACKUP E RESTAURAÇÃO
    # ----------------------------

    def fazer_backup(self):
        pessoas = []
        for pessoa in self.service.listar():
            copia = dict(pessoa)
            nascimento = self.nascimento_da_pessoa(pessoa)
            copia["data_nascimento"] = nascimento.isoformat() if nascimento else None
            pessoas.append(copia)

        payload = {
            "formato": "sistema_cadastros_backup",
            "versao": 1,
            "criado_em": datetime.now().isoformat(timespec="seconds"),
            "cadastros": pessoas,
            "lixeira": self.lixeira_cadastros,
        }
        caminho = filedialog.asksaveasfilename(
            parent=self,
            title=self.t("Fazer backup dos cadastros"),
            initialfile=f"backup_cadastros_{datetime.now():%Y%m%d_%H%M%S}.json",
            defaultextension=".json",
            filetypes=[("Backup JSON", "*.json")]
        )
        if not caminho:
            return
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(payload, arquivo, ensure_ascii=False, indent=4)
        except OSError as erro:
            self.mostrar_aviso(f"Não foi possível criar o backup: {erro}", "erro")
            return
        self.registrar_atividade("Backup criado", Path(caminho).name)
        self.mostrar_aviso("Backup criado com sucesso.", "sucesso")

    def selecionar_backup_para_restaurar(self):
        caminho = filedialog.askopenfilename(
            parent=self,
            title=self.t("Selecione o arquivo de backup"),
            filetypes=[("Backup JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                payload = json.load(arquivo)
            if (
                not isinstance(payload, dict)
                or payload.get("formato") != "sistema_cadastros_backup"
                or not isinstance(payload.get("cadastros"), list)
                or not isinstance(payload.get("lixeira", []), list)
                or not all(isinstance(item, dict) for item in payload.get("lixeira", []))
            ):
                raise ValueError
            # Valida todos os registros antes de abrir a confirmação/destruir dados atuais.
            for registro in payload["cadastros"]:
                if not isinstance(registro, dict) or not registro.get("nome") or registro.get("sexo") not in {"M", "F"}:
                    raise ValueError
                if registro.get("data_nascimento"):
                    data_validada = self.normalizar_data_nascimento(registro["data_nascimento"])
                    if data_validada > date.today():
                        raise ValueError
                else:
                    int(registro["idade"])
            for item_lixeira in payload.get("lixeira", []):
                if item_lixeira.get("data_nascimento"):
                    self.normalizar_data_nascimento(item_lixeira["data_nascimento"])
        except Exception:
            self.mostrar_aviso("Arquivo de backup inválido ou incompatível.", "erro")
            return

        janela = ctk.CTkToplevel(self)
        janela.title(self.t("Restaurar backup?"))
        janela.geometry("460x230")
        janela.resizable(False, False)
        janela.configure(fg_color=COR_CARD)
        janela.transient(self)
        janela.grab_set()
        ctk.CTkLabel(
            janela,
            text="Os cadastros atuais serão substituídos pelos dados do backup.\nEssa ação não poderá ser desfeita.",
            font=ctk.CTkFont(size=14), text_color=COR_TEXTO_CORPO,
            justify="center", wraplength=400
        ).pack(padx=25, pady=(25, 15))
        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(fill="x", padx=22, pady=15)
        ctk.CTkButton(
            botoes, text="Cancelar", fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER, command=janela.destroy
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(
            botoes, text="Restaurar backup", fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            command=lambda: self.confirmar_restauracao_backup(payload, janela)
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))
        self.traduzir_arvore(janela)

    def confirmar_restauracao_backup(self, payload, janela):
        janela.destroy()
        anteriores = [dict(pessoa) for pessoa in self.service.listar()]
        lixeira_anterior = [dict(item) for item in self.lixeira_cadastros]

        try:
            for pessoa in anteriores:
                self.service.excluir(pessoa["id"])
            self.dados_nascimento = {}
            self.salvar_dados_nascimento()

            for registro in payload["cadastros"]:
                nome = str(registro["nome"]).strip()
                sexo = registro["sexo"]
                if registro.get("data_nascimento"):
                    nascimento = self.normalizar_data_nascimento(registro["data_nascimento"])
                    self.adicionar_com_nascimento(nome, nascimento, sexo)
                else:
                    idade = int(registro["idade"])
                    self.service.adicionar(nome, idade, sexo)

            nova_lixeira = []
            for item in payload.get("lixeira", []):
                copia = dict(item)
                copia.setdefault("chave_lixeira", str(uuid4()))
                nova_lixeira.append(copia)
            self.lixeira_cadastros = nova_lixeira
            self.salvar_lixeira()
        except Exception as erro:
            # Tenta devolver os dados que estavam ativos antes da restauração.
            try:
                for pessoa in self.service.listar():
                    self.service.excluir(pessoa["id"])
                self.dados_nascimento = {}
                for pessoa in anteriores:
                    nascimento_txt = pessoa.get("data_nascimento")
                    if nascimento_txt:
                        self.adicionar_com_nascimento(
                            pessoa["nome"], self.normalizar_data_nascimento(nascimento_txt), pessoa["sexo"]
                        )
                    else:
                        self.service.adicionar(
                            pessoa["nome"], int(pessoa["idade"]), pessoa["sexo"]
                        )
                self.salvar_dados_nascimento()
                self.lixeira_cadastros = lixeira_anterior
                self.salvar_lixeira()
            except Exception:
                pass
            self.mostrar_aviso(
                f"Falha ao restaurar backup: {erro}. Foi tentada a recuperação dos dados anteriores.",
                "erro", titulo="Falha ao restaurar backup"
            )
            return

        self.registrar_atividade("Backup restaurado", f"{len(payload['cadastros'])} cadastro(s)")
        self.pagina_atual = 1
        self.pagina_lixeira = 1
        self.recarregar_tela_atual()
        self.mostrar_aviso("Backup restaurado com sucesso.", "sucesso")

    # ----------------------------
    # HISTÓRICO DE ATIVIDADES
    # ----------------------------

    def mostrar_historico(self):
        self.tela_ativa = "historico"
        self.limpar_conteudo()
        self.marcar_menu("historico")
        self.titulo_pagina(
            "Histórico de atividades",
            "Acompanhe os cadastros, alterações, exclusões e exportações"
        )

        self.pagina_historico = 1
        self.itens_por_pagina_historico = 5

        area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area.grid(row=1, column=0, sticky="nsew", padx=35, pady=5)
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        topo.grid_columnconfigure(0, weight=1)
        self.lbl_total_historico = ctk.CTkLabel(
            topo,
            text=f"{len(self.historico_atividades)} atividade(s) registrada(s)",
            text_color=COR_TEXTO,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_total_historico.grid(row=0, column=0, sticky="w", padx=18, pady=14)

        self.btn_limpar_historico = ctk.CTkButton(
            topo,
            text="Limpar histórico",
            width=155,
            height=34,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            text_color="#ffffff",
            command=self.pedir_confirmacao_limpar_historico
        )
        self.btn_limpar_historico.grid(row=0, column=1, sticky="e", padx=18, pady=10)

        painel = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=12)
        painel.grid(row=1, column=0, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(0, weight=1)

        self.corpo_historico = ctk.CTkFrame(painel, fg_color="transparent")
        self.corpo_historico.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.corpo_historico.grid_columnconfigure(0, weight=1)

        rodape = ctk.CTkFrame(painel, fg_color="transparent")
        rodape.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        rodape.grid_columnconfigure(1, weight=1)

        self.btn_historico_anterior = ctk.CTkButton(
            rodape,
            text="← Anterior",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_historico(-1)
        )
        self.btn_historico_anterior.grid(row=0, column=0, sticky="w")

        self.lbl_pagina_historico = ctk.CTkLabel(
            rodape,
            text="Página 1 de 1",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=12)
        )
        self.lbl_pagina_historico.grid(row=0, column=1)

        self.btn_historico_proxima = ctk.CTkButton(
            rodape,
            text="Próxima →",
            width=105,
            height=32,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=lambda: self.mudar_pagina_historico(1)
        )
        self.btn_historico_proxima.grid(row=0, column=2, sticky="e")

        self.atualizar_lista_historico()
        self.traduzir_arvore(self.conteudo)

    def total_paginas_historico(self):
        """Calcula o total de páginas do histórico com pelo menos uma página."""
        total = len(self.historico_atividades)
        por_pagina = max(1, self.itens_por_pagina_historico)
        return max(1, (total + por_pagina - 1) // por_pagina)

    def atualizar_lista_historico(self):
        """Atualiza os registros da página atual e o estado dos controles."""
        for widget in self.corpo_historico.winfo_children():
            widget.destroy()

        total = len(self.historico_atividades)
        total_paginas = self.total_paginas_historico()
        self.pagina_historico = min(max(1, self.pagina_historico), total_paginas)

        inicio = (self.pagina_historico - 1) * self.itens_por_pagina_historico
        fim = inicio + self.itens_por_pagina_historico
        registros = self.historico_atividades[inicio:fim]

        if not registros:
            ctk.CTkLabel(
                self.corpo_historico,
                text="Nenhuma atividade registrada ainda.",
                text_color=COR_TEXTO_MUDO,
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, pady=45)
        else:
            for indice, registro in enumerate(registros):
                linha = ctk.CTkFrame(
                    self.corpo_historico,
                    fg_color=COR_ITEM if indice % 2 == 0 else COR_CARD,
                    corner_radius=8
                )
                linha.grid(row=indice, column=0, sticky="ew", pady=3)
                linha.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(
                    linha,
                    text=self.t(registro.get("acao", "Atividade")),
                    text_color=COR_DESTAQUE,
                    font=ctk.CTkFont(size=13, weight="bold")
                ).grid(row=0, column=0, sticky="w", padx=14, pady=(9, 1))
                ctk.CTkLabel(
                    linha,
                    text=self.t(registro.get("detalhes", "")),
                    text_color=COR_TEXTO_CORPO,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                ).grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 9))
                ctk.CTkLabel(
                    linha,
                    text=registro.get("data_hora", ""),
                    text_color=COR_TEXTO_MUDO,
                    font=ctk.CTkFont(size=11)
                ).grid(row=0, column=1, rowspan=2, sticky="e", padx=14)

        self.lbl_total_historico.configure(
            text=f"{total} atividade(s) registrada(s)"
        )
        self.lbl_pagina_historico.configure(
            text=f"Página {self.pagina_historico} de {total_paginas}"
        )
        self.btn_historico_anterior.configure(
            state="normal" if self.pagina_historico > 1 else "disabled"
        )
        self.btn_historico_proxima.configure(
            state="normal" if self.pagina_historico < total_paginas else "disabled"
        )

        self.traduzir_arvore(self.corpo_historico)
        self.traduzir_arvore(self.lbl_total_historico.master)
        self.traduzir_arvore(self.lbl_pagina_historico.master)

    def pedir_confirmacao_limpar_historico(self):
        """Solicita confirmação antes de apagar todo o histórico de atividades."""
        if not self.historico_atividades:
            self.mostrar_aviso("Não há atividades para limpar.", "aviso")
            return

        janela = ctk.CTkToplevel(self)
        janela.title(self.t("Limpar histórico"))
        janela.geometry("420x220")
        janela.resizable(False, False)
        janela.configure(fg_color=COR_CARD)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text=self.t("Deseja apagar todo o histórico?"),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COR_TEXTO
        ).pack(padx=24, pady=(24, 8))

        ctk.CTkLabel(
            janela,
            text=self.t("Essa ação não poderá ser desfeita."),
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_CORPO,
            justify="center"
        ).pack(padx=24, pady=8)

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(fill="x", padx=24, pady=(12, 20))
        botoes.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            botoes,
            text=self.t("Cancelar"),
            height=38,
            fg_color=COR_BOTAO_NEUTRO,
            hover_color=COR_BOTAO_NEUTRO_HOVER,
            command=janela.destroy
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text=self.t("Sim, limpar histórico"),
            height=38,
            fg_color=COR_PERIGO,
            hover_color=COR_PERIGO_HOVER,
            text_color="#ffffff",
            command=lambda: self.limpar_historico(janela)
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        janela.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - janela.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - janela.winfo_height()) // 2
        janela.geometry(f"+{x}+{y}")
        janela.focus_force()

    def limpar_historico(self, janela):
        """Apaga o histórico da memória e do arquivo JSON."""
        try:
            with self.caminho_historico.open("w", encoding="utf-8") as arquivo:
                json.dump([], arquivo, ensure_ascii=False, indent=4)
        except OSError as erro:
            janela.destroy()
            self.mostrar_aviso(
                f"Não foi possível apagar o histórico: {erro}",
                "erro",
                titulo="Falha ao limpar histórico"
            )
            return

        janela.destroy()
        self.historico_atividades.clear()
        self.pagina_historico = 1
        self.atualizar_lista_historico()
        self.mostrar_aviso("Histórico apagado com sucesso.", "sucesso")

    def mudar_pagina_historico(self, direcao):
        """Avança ou retorna uma página, respeitando os limites do histórico."""
        if direcao not in (-1, 1):
            return

        total_paginas = self.total_paginas_historico()
        nova_pagina = self.pagina_historico + direcao

        if not 1 <= nova_pagina <= total_paginas:
            return

        self.pagina_historico = nova_pagina
        self.atualizar_lista_historico()

    # ----------------------------
    # CONFIGURAÇÕES
    # ----------------------------

    def mostrar_configuracoes(self):
        self.tela_ativa = "configuracoes"
        self.limpar_conteudo()
        self.marcar_menu("configuracoes")
        self.titulo_pagina(
            "Configurações",
            "Escolha o idioma da interface do sistema"
        )

        area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area.grid(row=1, column=0, sticky="new", padx=35, pady=5)
        area.grid_columnconfigure(0, weight=1)

        painel = ctk.CTkFrame(area, fg_color=COR_CARD, corner_radius=14)
        painel.grid(row=0, column=0, sticky="ew")
        painel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            painel,
            text="Idioma",
            text_color=COR_TEXTO,
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(22, 6))

        ctk.CTkLabel(
            painel,
            text="Escolha o idioma da interface.",
            text_color=COR_TEXTO_SEC,
            font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 18))

        ctk.CTkLabel(
            painel,
            text="Idioma",
            text_color=COR_TEXTO_CORPO,
            font=ctk.CTkFont(size=13)
        ).grid(row=2, column=0, sticky="w", padx=22, pady=10)

        self.combo_idioma = ctk.CTkComboBox(
            painel,
            values=["Português", "English", "Español"],
            width=180,
            height=38,
            state="readonly"
        )
        self.combo_idioma.set(self.idioma)
        self.combo_idioma.grid(row=2, column=1, sticky="e", padx=22, pady=10)

        ctk.CTkButton(
            painel,
            text="Aplicar idioma",
            height=40,
            width=180,
            fg_color=COR_DESTAQUE,
            hover_color=COR_DESTAQUE_HOVER,
            text_color=COR_TEXTO_NO_DESTAQUE,
            command=self.salvar_configuracoes
        ).grid(row=3, column=0, columnspan=2, sticky="e", padx=22, pady=(20, 22))

        self.traduzir_arvore(self.conteudo)

    def salvar_configuracoes(self):
        """Salva somente o idioma escolhido e atualiza a interface inteira."""
        novo_idioma = self.combo_idioma.get()
        if novo_idioma not in {"Português", "English", "Español"}:
            self.mostrar_aviso("Selecione um idioma válido.", "aviso")
            return

        idioma_anterior = self.idioma
        configuracoes_anteriores = self.configuracoes.copy()
        self.configuracoes["idioma"] = novo_idioma

        try:
            self.salvar_arquivo_configuracoes()
        except OSError as erro:
            self.configuracoes = configuracoes_anteriores
            self.mostrar_aviso(
                f"Não foi possível salvar as configurações: {erro}",
                "erro",
                titulo="Falha ao salvar"
            )
            return

        self.idioma = novo_idioma
        self.registrar_atividade("Idioma alterado", novo_idioma)
        self.recriar_interface_no_idioma_atual()

        if idioma_anterior == novo_idioma:
            self.mostrar_aviso("Idioma atualizado com sucesso!", "sucesso")
        else:
            self.mostrar_aviso("Idioma atualizado com sucesso!", "sucesso")

