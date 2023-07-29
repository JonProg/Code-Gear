#Validador de CPF

def valida_cpf(cpf):
    #---Primeiro Digito---

    mod_cpf = cpf.replace('.','').replace('-','')
    nove_digitos = mod_cpf[:9]
    contador_regressivo_1 = 10
    resultado_digito_1 = 0

    for digito in nove_digitos:
        resultado_digito_1 += int(digito)*contador_regressivo_1
        contador_regressivo_1-=1

    digito_1 = (resultado_digito_1*10)%11 if (resultado_digito_1*10)%11 <=9 else 0

    #---Segundo Digito---

    dez_digitos = mod_cpf[:9]+str(digito_1)
    contador_regressivo_2 = 11
    resultado_digito_2 = 0

    for digito in dez_digitos:
        resultado_digito_2 += int(digito)*contador_regressivo_2
        contador_regressivo_2-=1

    digito_2 = (resultado_digito_2*10)%11 if (resultado_digito_2*10)%11 <=9 else 0

    new_cpf=f'{nove_digitos}{digito_1}{digito_2}'

    if mod_cpf == new_cpf:
        return True
    else:
        return False

    #---------------------------------------