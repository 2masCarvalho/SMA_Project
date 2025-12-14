from abc import ABC, abstractmethod
import math
from Modelos import Observacao

class Sensor(ABC):
    """Interface base para todos os sensores."""
    
    @abstractmethod
    def detetar(self, ambiente, agente) -> Observacao:
        """
        Recolhe informação do ambiente relativa ao agente e retorna uma Observacao.
        """
        pass

class SensorVisao(Sensor):
    """Sensor que deteta obstáculos ou objetos num determinado raio."""
    def __init__(self, raio_visao: float):
        self.raio_visao = raio_visao

    def detetar(self, ambiente, agente) -> Observacao:
        # Aqui implementaria a lógica de ver o que está à volta
        # Depende da implementação específica do ambiente
        # Por exemplo, verificar paredes no Labirinto ou obstáculos no Farol
        return Observacao({"tipo": "visao", "raio": self.raio_visao, "objetos_vistos": []})

class SensorDirecao(Sensor):
    """Sensor que deteta a direção para um alvo (ex: Farol)."""
    def detetar(self, ambiente, agente) -> Observacao:
        # Tenta obter a posição do alvo e do agente
        # Esta lógica assume que o ambiente tem 'farol_pos' e 'agentes_posicoes'
        # Em um sistema real, o sensor teria de consultar uma interface do ambiente
        
        if hasattr(ambiente, 'farol_pos') and hasattr(ambiente, 'agentes_posicoes'):
            pos_agente = ambiente.agentes_posicoes.get(agente)
            if pos_agente:
                dx = ambiente.farol_pos[0] - pos_agente[0]
                dy = ambiente.farol_pos[1] - pos_agente[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0:
                    direcao = (dx / dist, dy / dist)
                else:
                    direcao = (0, 0)
                return Observacao({"direcao": direcao, "distancia": dist})
        
        return Observacao({"direcao": (0, 0), "erro": "alvo_nao_encontrado"})