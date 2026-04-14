"""monta resumo de capturas e salva relatorio em json"""
import csv
import json
from pathlib import Path
from typing import List, Dict, Any

def sumario(resultados: List[Dict[str, Any]]) -> Dict[str, Any]:
    arq_total = len(resultados)
    total_capturas = sum(item["total_capturas"] for item in resultados)

    tipo_captura = {}
    severidade_captura = {}
    cpfs_validos = 0
    cpfs_invalidos = 0
    cartoes_validos = 0
    cartoes_invalidos = 0

    for item in resultados:
        for captura in item["capturas"]:
            tipo = captura["tipo"]
            severidade = captura["severidade"]
            tipo_captura[tipo]=tipo_captura.get(tipo,0)+1
            severidade_captura[severidade]=severidade_captura.get(severidade,0)+1

            if tipo == "cpf":
                if captura["valido"] is True:
                    cpfs_validos += 1
                elif captura["valido"] is False:
                    cpfs_invalidos += 1

            if tipo == "cartao":
                if captura["valido"] is True:
                    cartoes_validos += 1
                elif captura["valido"] is False:
                    cartoes_invalidos += 1

    return{
        "arq_total_scan": arq_total,
        "total_capturas": total_capturas,
        "tipo_captura": tipo_captura,
        "severidade_captura": severidade_captura,
        "cpfs_validos": cpfs_validos,
        "cpfs_invalidos": cpfs_invalidos,
        "cartoes_validos": cartoes_validos,
        "cartoes_invalidos": cartoes_invalidos,
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

def save_csv(resultados: List[Dict[str,any]],output_path:Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w",encoding="utf-8",newline="")as f:
        writer = csv.writer(f)
        writer.writerows([
            "arquivo",
            "tipo",
            "conteudo",
            "mascarado",
            "valido",
            "severidade",
            "linha",
            "contexto",
            "inicio",
            "fim",
            "status_arquivo",
        ])

        for item in resultados:
            arquivo = item.get("arquivo","")
            status_arquivo = item.get("status","")

            for captura in item.get("capturas",[]):
                writer.writerow([
                    arquivo,
                    captura.get("tipo", ""),
                    captura.get("conteudo", ""),
                    captura.get("mascarado", ""),
                    captura.get("valido", ""),
                    captura.get("severidade", ""),
                    captura.get("linha", ""),
                    captura.get("contexto", ""),
                    captura.get("inicio", ""),
                    captura.get("fim", ""),
                    status_arquivo,
                ])