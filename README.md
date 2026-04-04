Personal Data Exposure Scanner

Projeto em Python para identificar exposição de dados sensíveis em arquivos locais.
O sistema percorre diretórios, analisa arquivos suportados e gera um relatório com possíveis ocorrências de informações sensíveis.

Objetivo
O projeto foi desenvolvido para fins de estudo e portfólio, com foco em segurança da informação e análise de exposição indevida de dados.

Funcionalidades atuais
- Varredura recursiva de diretórios
- Suporte a arquivos .txt, .csv e .json
- Detecção de dados sensíveis por expressões regulares
- Validação de CPF
- Validação de cartão com algoritmo de Luhn
- Mascaramento de dados encontrados
- Classificação por severidade
- Resumo no terminal
- Geração de relatório em JSON
- Contexto e linha aproximada da captura

Tipos de dados detectados
- CPF
- E-mail
- Telefone brasileiro
- Número de cartão
- Credenciais expostas em texto
- Campos financeiros

Estrutura do projeto
app/
- main.py -> ponto de entrada do sistema
- scanner.py -> leitura e varredura dos arquivos
- patterns.py -> padrões regex usados na detecção
- validation.py -> validação, mascaramento e severidade
- report.py -> geração de resumo e relatório JSON

samples/
- arquivos de teste

output/
- relatórios gerados pelo sistema

Como executar
1. Abra o terminal na raiz do projeto
2. Execute o comando:

python -m app.main samples

Se quiser definir outro arquivo de saída:

python -m app.main samples -o output/report.json

Saída esperada
O sistema exibe um resumo no terminal com:
- quantidade de arquivos escaneados
- total de capturas
- quantidade por tipo
- severidade
- CPFs válidos e inválidos
- cartões válidos e inválidos

Também é gerado um arquivo JSON com os detalhes de cada captura encontrada.

Exemplo de uso
O scanner pode ser usado para analisar arquivos de teste, documentos simulados e bases locais em busca de:
- documentos pessoais expostos
- credenciais em texto puro
- dados financeiros
- padrões que indiquem risco de vazamento

Observações
- O projeto é voltado para fins educacionais e de portfólio
- Nem toda ocorrência encontrada representa um dado real, pois parte da detecção é baseada em padrões
- A validação real atualmente está implementada para CPF e cartão

Possíveis melhorias futuras
- Ignorar diretórios irrelevantes como .venv e __pycache__
- Exportação adicional em CSV
- Suporte a mais formatos de arquivo
- Interface web
- Testes automatizados
- Regras adicionais de validação e contexto

Autor
Projeto desenvolvido para estudo, prática e composição de portfólio em Python e segurança da informação.
