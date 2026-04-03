"""centro de comando do sistema onde usuario executa no terminal"""
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from app.report import save_report,sumario
from app.scanner import scan_diretorio

app = typer.Typer(help="Scanner de exposição de dados sensíveis em arquivos locais")
console = Console()

@app.command()
def scan(
        target: str = typer.Argument(..., help="Diretorio"),
        output: str = typer.Option("output/report.json","--output","-o",help="Arquivo de saida"),
):
    target_path = Path(target)
    output_path = Path(output)

    if not target_path.exists():
        console.print(f"[red]Erro:[/red] Caminho '{target}' Não existe")
        raise typer.Exit(code=1)

    if not target_path.is_dir():
        console.print(f"[red]Erro:[/red] Caminho '{target}' Não é diretorio")
        raise typer.Exit(code=1)

    resultado = scan_diretorio(target_path)
    sumario_main = sumario(resultado)
    save_report(resultado,output_path)

    table = Table(title="Resumo do Scan")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="magenta")

    table.add_row("Escaneados", str(sumario_main["arq_total_scan"]))
    table.add_row("Capturas",str(sumario_main["total_capturas"]))
    table.add_row("CPF válidos", str(sumario_main["cpfs_validos"]))
    table.add_row("CPF inválidos", str(sumario_main["cpfs_invalidos"]))
    table.add_row("Cartoes validos", str(sumario_main["cartoes_validos"]))
    table.add_row("Cartoes invalidos", str(sumario_main["cartoes_invalidos"]))


    for tipo,count in sumario_main["tipo_captura"].items():
        table.add_row(f"Tipo:{tipo}",str(count))

    for severidade, count in sumario_main["severidade_captura"].items():
        table.add_row(f"Severidade: {severidade}", str(count))

    console.print(table)
    console.print(f"\n[green]Relatório salvo em:[/green] {output_path}")

if __name__ == "__main__":
    app()
