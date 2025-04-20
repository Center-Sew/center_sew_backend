from enum import Enum

class TipoServico(str, Enum):
    AJUSTE_UNIFORME = "Ajuste de uniforme"
    REPARO_JALECO = "Reparo de jaleco"
    BORDADO_LOGO = "Bordado de logotipo"
    CONFECCAO_AVENTAIS = "Confecção de aventais"
    COSTURA_CORTINA = "Costura de cortina"
    BAINHA_CALCA = "Bainha de calça"
    TROCA_ZIPER = "Troca de zíper"
    PATCHES = "Aplicação de patches"
    UNIFORMES_HOSPITALARES = "Uniformes hospitalares"
    CAPA_MAQUINA = "Costura de capa para máquina"
