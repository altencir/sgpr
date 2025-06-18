import re

def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Validação dígitos verificadores
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    if len(cnpj) != 14:
        return False
    
    # CNPJ validation logic
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    for i in range(2):
        sum_digits = sum(int(cnpj[j]) * weights[j] for j in range(len(weights)))
        digit = 11 - (sum_digits % 11)
        if digit > 9:
            digit = 0
        if digit != int(cnpj[12 + i]):
            return False
        weights.insert(0, 6)
    
    return True

def validate_cpf_cnpj(document: str) -> bool:
    document = re.sub(r'[^0-9]', '', document)
    
    if len(document) == 11:
        return validate_cpf(document)
    elif len(document) == 14:
        return validate_cnpj(document)
    
    return False