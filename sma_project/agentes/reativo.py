from ..core.interfaces import Agente, Observacao, Accao
from ..core.politica import PoliticaReativaFarol

class AgenteReativoFarol(Agente):
    """Agente com política fixa para o problema do Farol."""
    def __init__(self, nome: str):
        super().__init__(nome)
        self.politica = PoliticaReativaFarol()
        self.ultima_observacao: Observacao = None

    def observacao(self, obs: Observacao):
        self.ultima_observacao = obs

    def age(self) -> Accao:
        if self.ultima_observacao is None:
            return Accao("parar", {})
        return self.politica.selecionar_accao(self.ultima_observacao)

    def avaliacao_estado_atual(self, recompensa: float):
        super().avaliacao_estado_atual(recompensa)
        # Não há atualização de política, apenas registo da recompensa
