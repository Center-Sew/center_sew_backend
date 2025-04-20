from enum import Enum

class TipoLocalizacaoAlvo(str, Enum):
    RAIO = "raio"
    CIDADE = "cidade"
    ESTADO = "estado"