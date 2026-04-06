"""scanner de arquivos"""
import os
from pathlib import Path
from typing import List,Dict,Any
from app.patterns import PATTERNS
from app.validation import (
    validar_cpf,
    mascarar_cpf,
    validar_card,
    mascarar_card,
    severidade,
)

extensoes = {".txt",".csv",".json"}
diretorios_ignorados = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "output",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
    "dist",
    "build",
    ".tox",
    ".coverage",
    "htmlcov",
    ".eggs",
}

arquivos_ignorados = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
}

def arquivo_suportado(file_path:Path) -> bool:
    if not file_path.is_file():
        return False

    if arquivo_ignorado(file_path.name):
        return False

    return file_path.suffix.lower() in extensoes
"""Garante que não é diretorio e tem extensão suportada"""

def diretorio_ignorado(nome_diretorio: str) -> bool:
    return nome_diretorio.lower() in {item.lower() for item in diretorios_ignorados}
"""verifica se o nome do diretorio esta na lista de exclusao"""

def arquivo_ignorado(nome_arquivo: str) -> bool:
    return nome_arquivo.lower() in {item.lower() for item in arquivos_ignorados}
"""verifica se o nome do arquivo esta na lista de exclusao"""

def ler_arquivo(file_path:Path)->str:
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return Path(file_path).read_text(encoding="latin-1")
        except Exception:
            return "" #adicionar log de erro
    except Exception:
        return "" #adicionar log de erro
"""tenta ler o arquivo sem quebrar o programa, formato utf-8 e latin-1"""

#bloco de checagem de linhas
# contar quebra de linha;
def numero_linha(content: str, posicao:int)->int:
    return content.count("\n",0,posicao)+1

#retornar o texto da linha onde houve a captura
def linha_texto(content:str, posicao:int)->str:
    linhas = content.splitlines()

    if not linhas:
        return ""

    linha = numero_linha(content,posicao)
    if 1 <= linha <= len(linhas):
        return linhas[linha-1]
    return ""

#gera um resumo da linha onde a captura foi feita
def contexto(content: str, posicao: int, limite: int=120):
    texto_linha = linha_texto(content, posicao).strip()
    if len(texto_linha) <= limite:
        return texto_linha

    return texto_linha[:limite]+"..."

def captura_refinada(content: str, tipo_dado: str, valor_encontrado: str, inicio: int, fim: int) -> Dict[str, Any]:
    captura = {
        "tipo": tipo_dado,
        "conteudo": valor_encontrado,
        "mascarado": valor_encontrado,
        "inicio": inicio,
        "fim": fim,
        "linha": numero_linha(content,inicio),
        "contexto": contexto(content,inicio),
        "valido": None,
        "severidade": severidade(tipo_dado),
    }

    if tipo_dado == "cpf":
        captura["valido"] = validar_cpf(valor_encontrado)
        captura["mascarado"] = mascarar_cpf(valor_encontrado)

    if tipo_dado == "cartao":
        captura["valido"] = validar_card(valor_encontrado)
        captura["mascarado"] = mascarar_card(valor_encontrado)

    return captura
    "adiciona refinamento validação,mascara e severidade"


def capturas_feitas(content:str)->List[Dict[str,Any]]:
    capturas = []

    for tipo_dado, pattern in PATTERNS.items():
        for conteudo in pattern.finditer(content):
            valor_encontrado = conteudo.group(0)

            captura = captura_refinada(
                content=content,
                tipo_dado=tipo_dado,
                valor_encontrado=valor_encontrado,
                inicio=conteudo.start(),
                fim=conteudo.end()
            )
            capturas.append(captura)
    return capturas
"recebe o texto inteiro do arquivo e busca trechos sensiveis, e captura em uma lista para relatprio"

def scan_arquivo(file_path:Path)->Dict[str,Any]:
    conteudo = ler_arquivo(file_path)
    if not conteudo:
        return {
            "arquivo" : str(file_path),
            "capturas" : [],
            "total_capturas" : 0,
            "status": "ilegivel_vazio",
        }
    capturas = capturas_feitas(conteudo)
    return {
        "arquivo": str(file_path),
        "capturas": capturas,
        "total_capturas": len(capturas),
        "status": "funcional",
    }
"""le um unico arquivo por vez e faz a busca"""

def scan_diretorio(directory:Path)->list[Dict[str,Any]]:
    resultados = []

    for raiz,diretorios,arquivos in os.walk(directory):
        diretorios[:]=[
            nome for nome in diretorios
            if not diretorio_ignorado(nome)
        ]
        #remove do caminho os diretorios que devem ser ignorados

        for nome_arquivo in arquivos:
            caminho_arquivo = Path(raiz) / nome_arquivo
            if arquivo_suportado(caminho_arquivo):
                resultados.append(scan_arquivo(caminho_arquivo))

    return resultados
"""buscar todos arquivos suportados em pastas e subpastas"""
