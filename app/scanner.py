"""scanner de arquivos"""
from pathlib import Path
from typing import List,Dict,Any
from app.patterns import PATTERNS
from app.validation import validar_cpf,mascarar_cpf,severidade

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

def captura_refinada(tipo_dado: str, valor_encontrado: str, inicio: int, fim: int) -> Dict[str, Any]:
    captura = {
        "tipo": tipo_dado,
        "conteudo": valor_encontrado,
        "conteudo_mascarado": valor_encontrado,
        "inicio": inicio,
        "fim": fim,
        "valido": None,
        "severidade": severidade(tipo_dado),
    }

    if tipo_dado == "cpf":
        captura["valido"] = validar_cpf(valor_encontrado)
        captura["mascarado"] = mascarar_cpf(valor_encontrado)
    return captura

    "adiciona refinamento validação,mascara e severidade"

def capturas_feitas(content:str)->List[Dict[str,Any]]:
    capturas = []

    for tipo_dado, pattern in PATTERNS.items():
        for conteudo in pattern.finditer(content):
            valor_encontrado = conteudo.group(0)

            captura = captura_refinada(
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
