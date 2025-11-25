class Sensor:
    """
    Representa um sensor simples usado por agentes.
    Pode ser estendido para tipos diferentes (direção do alvo, deteção de parede, etc.).
    
    sensor_parede = Sensor("detetor_parede", {"alcance": 1})
    agente.instala(sensor_parede)
    """
    def __init__(self, tipo, parametros=None):
        self.tipo = tipo            # Ex: 'direcao_farol', 'detetor_parede'
        self.parametros = parametros or {}  # Ex: {"alcance": 2}

    def __repr__(self):
        return f"Sensor(tipo={self.tipo}, parametros={self.parametros})"