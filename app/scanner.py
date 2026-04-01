"""scanner de arquivos"""
from pathlib import Path
from typing import List,Dict,Any
from app.patterns import PATTERNS

extensoes = {".txt",".csv",".json"}

def arquivo_suportado(file_path:Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in extensoes
"""Garante que não é diretorio e tem extensão suportada"""

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

def capturas_feitas(content:str)->List[Dict[str,Any]]:
    capturas = []

    for tipo_dado, pattern in PATTERNS.items():
        for conteudo in pattern.finditer(content):
            capturas.append({
                "tipo": tipo_dado,
                "conteudo": conteudo.group(0),
                "inicio": conteudo.start(),
                "fim": conteudo.end()
            })
    return capturas
"recebe o texto inteiro do arquivo e busca trechos sensiveis, e captura em uma lista para relatprio"

def scan_arquivo(file_path:Path)->Dict[str,Any]:
    conteudo = ler_arquivo(file_path)
    if not conteudo:
        return {
            "arquivo:" : str(file_path),
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
    for arquivo in directory.rglob("*"):
        if arquivo_suportado(arquivo):
            resultados.append(scan_arquivo(arquivo))
    return resultados
"""buscar todos arquivos suportados em pastas e subpastas"""
