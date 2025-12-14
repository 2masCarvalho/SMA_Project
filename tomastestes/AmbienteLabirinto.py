import threading
from typing import Tuple, List
from Ambiente import Ambiente
from Modelos import Observacao, Accao
from agente import Agente

class AmbienteLabirinto(Ambiente):
    """Ambiente de Labirinto com paredes e uma saída."""
    def __init__(self, dimensoes: Tuple[int, int], paredes: List[Tuple[int, int]], saida: Tuple[int, int], inicio: Tuple[int, int] = (0,0)):
        super().__init__()
        self.largura, self.altura = dimensoes
        self.paredes = set(tuple(p) for p in paredes) # Usar set para busca rápida
        self.saida = tuple(saida)
        self.inicio = tuple(inicio)
        self.agentes_posicoes = {} # {agente: (x, y)}

    def adicionar_agente(self, agente: Agente, pos_inicial: Tuple[int, int]):
        self.agentes_posicoes[agente] = tuple(pos_inicial)

    def observacaoPara(self, agente: Agente) -> Observacao:
        """
        Retorna as direções possíveis de movimento (N, S, E, O) que não têm paredes.
        """
        if agente not in self.agentes_posicoes:
            return Observacao({})
        
        x, y = self.agentes_posicoes[agente]
        caminhos_possiveis = []
        
        # Verificar 4 direções: (dx, dy)
        direcoes = {
            "norte": (0, -1),
            "sul": (0, 1),
            "este": (1, 0),
            "oeste": (-1, 0)
        }
        
        for dir_nome, (dx, dy) in direcoes.items():
            nx, ny = x + dx, y + dy
            # Verificar limites
            if 0 <= nx < self.largura and 0 <= ny < self.altura:
                # Verificar paredes
                if (nx, ny) not in self.paredes:
                    caminhos_possiveis.append(dir_nome)
                    
        return Observacao({
            "posicao": (x, y),
            "caminhos": caminhos_possiveis,
            "saida": self.saida
        })

    def atualizacao(self):
        pass

    def _agir_safe(self, accao: Accao, agente: Agente) -> float:
        if accao.tipo != "mover":
            return 0.0
            
        direcao_nome = accao.parametros.get("direcao")
        if not direcao_nome:
            return 0.0
            
        # Mapear nome da direção para vetor
        mapa_dir = {
            "norte": (0, -1),
            "sul": (0, 1),
            "este": (1, 0),
            "oeste": (-1, 0)
        }
        
        # Se a direção for uma tupla (como no farol), tentar adaptar ou ignorar
        # O AgenteExplorador usa nomes ("norte", etc) ou vetores?
        # Vamos verificar o AgenteExplorador depois. Se ele usar vetores, temos de adaptar.
        # Por agora assumo que o AgenteExplorador recebe "caminhos" como strings e devolve uma string.
        
        dx, dy = 0, 0
        if isinstance(direcao_nome, str) and direcao_nome in mapa_dir:
            dx, dy = mapa_dir[direcao_nome]
        elif isinstance(direcao_nome, (list, tuple)):
            # Caso o agente envie vetor direto
            dx, dy = direcao_nome
        else:
            return 0.0

        pos_atual = self.agentes_posicoes[agente]
        novo_x = pos_atual[0] + dx
        novo_y = pos_atual[1] + dy
        
        # Validar movimento
        if not (0 <= novo_x < self.largura and 0 <= novo_y < self.altura):
            return -1.0 # Parede do mundo
            
        if (novo_x, novo_y) in self.paredes:
            return -1.0 # Parede interna
            
        # Atualizar
        self.agentes_posicoes[agente] = (novo_x, novo_y)
        
        # Recompensa
        if (novo_x, novo_y) == self.saida:
            print(f"!!! Agente {agente.nome} encontrou a SAÍDA !!!")
            recompensa = 100.0
        else:
            recompensa = -0.1 # Custo de movimento
            
        agente.avaliacao_estado_atual(recompensa)
        return recompensa
