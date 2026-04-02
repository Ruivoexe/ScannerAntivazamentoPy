"""dicionario de dados sensiveis"""
import re
regex = re

PATTERNS = {
    "cpf": regex.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "email": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
    "telefone_br": re.compile(r"\b(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})-?\d{4}\b"),
    "cartao": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "credencial_exposta": re.compile(r"(?i)\b(?:senha|password|passwd|token|api[_-]?key|secret)\b\s*[:=]\s*[^\s]+"),
    "campo_financeiro": re.compile(r"(?i)\b(?:salario|salary|renda|income|valor|amount|balance|saldo)\b\s*[:=]\s*[^\s]+"),
}
