from agente import Agente
from Modelos import Accao, Observacao
from Politica import Politica

class AgenteRL(Agente):
    """Agente que usa uma política (ex: Q-Learning) para tomar decisões."""
    def __init__(self, nome: str, politica: Politica):
        super().__init__(nome)
        self.politica = politica

    def observacao(self, obs: Observacao):
        super().observacao(obs)
        # A política pode precisar da observação, mas a decisão é feita em age()
        # Aqui apenas guardamos se necessário, mas o Agente base já guarda self.ultima_observacao

    def age(self) -> Accao:
        if self.ultima_observacao:
            return self.politica.selecionar_accao(self.ultima_observacao)
        return Accao("parar")

    def avaliacao_estado_atual(self, recompensa: float):
        super().avaliacao_estado_atual(recompensa)
        self.politica.atualizar(recompensa)
    
    def comunica(self, mensagem: str, de_agente: Agente):
        pass
