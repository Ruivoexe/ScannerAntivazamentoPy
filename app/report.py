"""monta resumo de capturas e salva relatorio em json"""
import json
from pathlib import Path
from typing import List, Dict, Any

def sumario(resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
    arq_total = len(resultados)
    total_capturas = sum(item["total_capturas"] for item in resultados)
    tipo_captura = {}

    for item in resultados:
        for captura in item["capturas"]:
            tipo = captura["tipo"]
            tipo_captura[tipo]=tipo_captura.get(tipo,0)+1

    return{
        "arq_total_scan": arq_total,
        "total_capturas": total_capturas,
        "tipo_captura": tipo_captura,
    }

def save_report(resultados: List[Dict[str, Any]],output_path:Path) -> None:
    report = {
        "sumario": sumario(resultados),
        "files":resultados
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w",encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

"""percorre cada arquivo, depois cada captura do arquivo e conta por categoria"""
"""salva tudo em json e monta relatorio com resumo geral e dados detalhados do arquivo"""
