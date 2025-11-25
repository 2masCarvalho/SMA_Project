from typing import List
from .interfaces import Ambiente, Agente

class MotorDeSimulacao:
    """Orquestrador do ciclo de simulação."""
    def __init__(self, ambiente: Ambiente, agentes: List[Agente]):
        self.ambiente = ambiente
        self.agentes = agentes
        
        # Adicionar agentes ao ambiente (específico para AmbienteFarol e Labirinto)
        # Esta lógica será movida para o main.py ou para um factory, mas mantemos aqui
        # a chamada para o método de adicionar agente do ambiente.
        for agente in agentes:
            # Assumimos que o ambiente tem um método para adicionar agentes
            if hasattr(ambiente, 'adicionar_agente'):
                ambiente.adicionar_agente(agente)

    def executa(self, max_episodios: int = 1):
        """Executa a simulação por um número de episódios."""
        for episodio in range(1, max_episodios + 1):
            print(f"\n--- EPISÓDIO {episodio} ---")
            self.ambiente.reset()
            
            # Resetar recompensas dos agentes
            for agente in self.agentes:
                agente.recompensa_total = 0.0
                agente.passos = 0
            
            while not self.ambiente.terminou():
                self.passo()
                
            print(f"--- EPISÓDIO {episodio} TERMINADO ---")
            self.ambiente.visualizar()
            for agente in self.agentes:
                print(f"Agente {agente.nome}: Recompensa Total = {agente.recompensa_total:.2f}, Passos = {agente.passos}")

    def passo(self):
        """Executa um único passo de tempo (síncrono/sequencial)."""
        self.ambiente.atualizacao()
        
        for agente in self.agentes:
            # 1. Observação
            obs = self.ambiente.observacao_para(agente)
            agente.observacao(obs)
            
            # 2. Decisão
            accao = agente.age()
            
            # 3. Ação e Recompensa
            recompensa = self.ambiente.agir(accao, agente)
            
            # 4. Avaliação (Aprendizagem)
            agente.avaliacao_estado_atual(recompensa)
            
        # 5. Visualização (a cada passo)
        # self.ambiente.visualizar() # Descomentar para ver passo a passo
