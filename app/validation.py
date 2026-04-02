"""validar e mascarar dados sensiveis como cpf"""
import re
regex = re
def somente_digitos(texto:str)->str:
    return regex.sub(r"\D","",texto)
    """remove tudo que nao for numero"""

def validar_cpf(cpf:str)->bool:
    cpf = somente_digitos(cpf)
    if len(cpf) !=11:
        return False
    #rejeita cpf com todos digitos iguais
    if cpf==cpf[0]*11:
        return False
    #calcula 1o do digito verificador
    soma_1 = sum(int(cpf[i])*(10-i) for i in range(9))
    digito_1 = (soma_1 * 10) % 11
    if digito_1 == 10:
        digito_1 = 0

    #calcula 2o digito verificado
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma_2 * 10) % 11
    if digito_2 == 10:
        digito_2 = 0

    return cpf[9]==str(digito_1) and cpf[10] == str(digito_2)
    """valida cpf pelos digitos e aceita cpf com ou sem pontuaçao"""

def mascarar_cpf(cpf:str)->str:
    cpf_numerico = somente_digitos(cpf)
    if len(cpf_numerico) != 11:
        return cpf
    return f"{cpf_numerico[:3]}.***.***-{cpf_numerico[-2:]}"
    """mascara cpf para evitar expor dado no relatorio"""

def severidade(tipo:str)->str:
   """define severidade basica por tipo de dado"""
   mapa = {
       "cpf":"alta",
       "email": "media",
       "telefone_br": "media",
       "cartao": "critica",
       "credencial_exposta": "critica",
       "campo_financeiro": "alta",
   }
   return mapa.get(tipo,"baixa")

