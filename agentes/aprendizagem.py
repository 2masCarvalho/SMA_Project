from typing import List, Tuple
import random
from ..core.interfaces import Agente, Observacao, Accao
from ..core.politica import PoliticaQlearning

class AgenteAprendizagemLabirinto(Agente):
    """Agente de Aprendizagem (Q-Learning) para o Labirinto."""
    def __init__(self, nome: str, acoes: List[str]):
        super().__init__(nome)
        self.politica = PoliticaQlearning(acoes)
        self.ultima_observacao: Observacao = None
        self.ultima_acao: Accao = None
        self.estado_anterior: Tuple[int, int] = None

    def observacao(self, obs: Observacao):
        # O estado anterior é a posição da observação anterior
        self.estado_anterior = self.ultima_observacao.dados["posicao"] if self.ultima_observacao else obs.dados["posicao"]
        self.ultima_observacao = obs

    def age(self) -> Accao:
        if self.ultima_observacao is None:
            # Ação inicial aleatória (deve ser tratada pelo motor de simulação)
            self.ultima_acao = Accao("mover", {"direcao": random.choice(self.politica.acoes)})
        else:
            self.ultima_acao = self.politica.selecionar_accao(self.ultima_observacao)
        return self.ultima_acao

    def avaliacao_estado_atual(self, recompensa: float):
        super().avaliacao_estado_atual(recompensa)
        
        # Se tivermos estado anterior, ação e recompensa, podemos aprender
        if self.estado_anterior is not None and self.ultima_acao is not None:
            estado_atual = self.ultima_observacao.dados["posicao"]
            self.politica.aprender(self.estado_anterior, self.ultima_acao, recompensa, estado_atual)
