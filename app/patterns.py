import re
regex = re

PATTERNS = {
    "cpf": regex.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
}