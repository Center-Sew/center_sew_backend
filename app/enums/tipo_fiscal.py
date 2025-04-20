from enum import Enum

class TipoFiscal(str, Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"