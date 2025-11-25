import math
import random
from typing import List, Dict, Any, Tuple
from .interfaces import Politica, Observacao, Accao

# ==============================================================================
# 1. POLÍTICA REATIVA PARA O FAROL
# ==============================================================================

class PoliticaReativaFarol(Politica):
    """Política fixa: move-se na direção do farol."""
    def selecionar_accao(self, observacao: Observacao) -> Accao:
        direcao_farol = observacao.dados["direcao_farol"]
        
        if observacao.dados["no_farol"]:
            return Accao("parar", {})

        # Ação: Mover 1 unidade na direção mais próxima dos eixos (N, S, E, O)
        dx_unit, dy_unit = direcao_farol
        
        # Escolhe o movimento mais forte (o mais próximo de 1 ou -1)
        if abs(dx_unit) > abs(dy_unit):
            # Movimento horizontal
            dx = 1 if dx_unit > 0 else -1
            dy = 0
        else:
            # Movimento vertical
            dx = 0
            dy = 1 if dy_unit > 0 else -1
            
        return Accao("mover", {"dx": dx, "dy": dy})

    def aprender(self, estado_anterior, accao, recompensa, estado_atual):
        """Agente reativo não aprende."""
        pass

# ==============================================================================
# 2. POLÍTICA DE APRENDIZAGEM (Q-LEARNING) - Será usada no Labirinto
# ==============================================================================

class PoliticaQlearning(Politica):
    """Política de Q-Learning (Epsilon-Greedy)."""
    def __init__(self, acoes: List[str], alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_tabela: Dict[Tuple[Tuple[int, int], str], float] = {}
        self.acoes = acoes
        self.alpha = alpha # Taxa de aprendizagem
        self.gamma = gamma # Fator de desconto
        self.epsilon = epsilon # Fator de exploração

    def _get_q(self, estado: Tuple[int, int], acao: str) -> float:
        """Obtém o valor Q para um par estado-ação."""
        return self.q_tabela.get((estado, acao), 0.0)

    def selecionar_accao(self, observacao: Observacao) -> Accao:
        estado = observacao.dados["posicao"]
        
        # Epsilon-Greedy: Exploração vs Explotação
        if random.random() < self.epsilon:
            # Exploração: Escolhe uma ação aleatória
            acao_str = random.choice(self.acoes)
        else:
            # Explotação: Escolhe a melhor ação (greedy)
            q_valores = {acao: self._get_q(estado, acao) for acao in self.acoes}
            melhor_q = max(q_valores.values())
            melhores_acoes = [acao for acao, q in q_valores.items() if q == melhor_q]
            acao_str = random.choice(melhores_acoes)
            
        # Mapear a string da ação para a estrutura Accao
        return Accao("mover", {"direcao": acao_str})

    def aprender(self, estado_anterior: Tuple[int, int], acao: Accao, recompensa: float, estado_atual: Tuple[int, int]):
        acao_str = acao.parametros["direcao"]
        
        # Q-Learning Update Rule:
        # Q(s, a) = Q(s, a) + alpha * [recompensa + gamma * max(Q(s', a')) - Q(s, a)]
        
        q_antigo = self._get_q(estado_anterior, acao_str)
        
        # Encontrar o Q máximo para o estado atual (s')
        q_max_atual = max([self._get_q(estado_atual, a) for a in self.acoes])
        
        novo_q = q_antigo + self.alpha * (recompensa + self.gamma * q_max_atual - q_antigo)
        
        self.q_tabela[(estado_anterior, acao_str)] = novo_q
