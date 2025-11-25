import math
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

# ==============================================================================
# 1. CLASSES DE DADOS (Observacao, Accao)
# ==============================================================================

class Observacao:
    """Estrutura de dados para a observação do ambiente pelo agente."""
    def __init__(self, dados: Dict[str, Any]):
        self.dados = dados

    def __repr__(self):
        return f"Observacao({self.dados})"

class Accao:
    """Estrutura de dados para a ação do agente."""
    def __init__(self, tipo: str, parametros: Dict[str, Any]):
        self.tipo = tipo
        self.parametros = parametros

    def __repr__(self):
        return f"Accao(tipo='{self.tipo}', params={self.parametros})"

# ==============================================================================
# 2. INTERFACES BASE (Agente, Ambiente, Politica)
# ==============================================================================

class Politica(ABC):
    """Interface para a lógica de decisão e aprendizagem do agente."""
    @abstractmethod
    def selecionar_accao(self, observacao: Observacao) -> Accao:
        """Decide a próxima ação com base na observação."""
        pass

    @abstractmethod
    def aprender(self, estado_anterior, accao, recompensa, estado_atual):
        """Atualiza a política com base na experiência (apenas para agentes de aprendizagem)."""
        pass

class Agente(ABC):
    """Interface base para todos os agentes."""
    def __init__(self, nome: str):
        self.nome = nome
        self.recompensa_total = 0.0
        self.passos = 0

    @abstractmethod
    def observacao(self, obs: Observacao):
        """Recebe a observação do ambiente."""
        pass

    @abstractmethod
    def age(self) -> Accao:
        """Decide e retorna a ação a ser executada."""
        pass

    @abstractmethod
    def avaliacao_estado_atual(self, recompensa: float):
        """Recebe a recompensa e atualiza o estado interno/política."""
        self.recompensa_total += recompensa
        self.passos += 1

class Ambiente(ABC):
    """Interface base para todos os ambientes de simulação."""
    @abstractmethod
    def observacao_para(self, agente: Agente) -> Observacao:
        """Gera a observação específica para um agente."""
        pass

    @abstractmethod
    def agir(self, accao: Accao, agente: Agente) -> float:
        """Processa a ação do agente e retorna a recompensa."""
        pass

    @abstractmethod
    def atualizacao(self):
        """Atualiza o estado do ambiente (e.g., movimento de recursos, tempo)."""
        pass

    @abstractmethod
    def terminou(self) -> bool:
        """Verifica se o episódio de simulação terminou."""
        pass

    @abstractmethod
    def reset(self):
        """Reinicia o ambiente para um novo episódio."""
        pass

    @abstractmethod
    def visualizar(self):
        """Apresenta o estado atual do ambiente (visualização simples)."""
        pass
