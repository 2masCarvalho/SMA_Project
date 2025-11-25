from typing import List, Dict, Any, Tuple
import random
from ..core.interfaces import Ambiente, Agente, Observacao, Accao

class AmbienteLabirinto(Ambiente):
    """Ambiente 2D para o problema do Labirinto (Grelha com paredes)."""
    def __init__(self, mapa: List[str], start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        self.mapa = [list(row) for row in mapa]
        self.altura = len(self.mapa)
        self.largura = len(self.mapa[0])
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.agentes_posicoes: Dict[str, Tuple[int, int]] = {}
        self.passos_maximos = 200
        self.passos_atuais = 0
        self.terminou_flag = False

    def adicionar_agente(self, agente: Agente):
        """Adiciona um agente ao ambiente na posição inicial."""
        self.agentes_posicoes[agente.nome] = self.start_pos

    def reset(self):
        """Reinicia o ambiente, colocando os agentes na posição inicial."""
        for nome in self.agentes_posicoes.keys():
            self.agentes_posicoes[nome] = self.start_pos
        self.passos_atuais = 0
        self.terminou_flag = False

    def observacao_para(self, agente: Agente) -> Observacao:
        """
        Gera a observação: Posição atual do agente e proximidade de paredes.
        Para o Q-Learning, a observação principal é a posição (x, y).
        """
        pos_agente = self.agentes_posicoes[agente.nome]
        
        # Sensores de Proximidade (Norte, Sul, Este, Oeste)
        x, y = pos_agente
        sensores = {
            "N": self._is_wall(x, y - 1),
            "S": self._is_wall(x, y + 1),
            "E": self._is_wall(x + 1, y),
            "O": self._is_wall(x - 1, y),
        }
        
        return Observacao({
            "posicao": pos_agente,
            "sensores_proximidade": sensores,
            "objetivo_atingido": pos_agente == self.end_pos
        })

    def _is_wall(self, x, y):
        """Verifica se a posição é uma parede ou fora dos limites."""
        if 0 <= y < self.altura and 0 <= x < self.largura:
            return self.mapa[y][x] == '#'
        return True # Fora dos limites é considerado parede

    def agir(self, accao: Accao, agente: Agente) -> float:
        """Processa a ação de movimento e calcula a recompensa."""
        if accao.tipo != "mover":
            return -1.0 # Penalidade por ação inválida

        pos_atual = self.agentes_posicoes[agente.nome]
        x, y = pos_atual
        
        direcao = accao.parametros.get("direcao")
        
        dx, dy = 0, 0
        if direcao == "N": dy = -1
        elif direcao == "S": dy = 1
        elif direcao == "E": dx = 1
        elif direcao == "O": dx = -1
        
        nova_x, nova_y = x + dx, y + dy
        
        recompensa = -0.1 # Custo de energia por passo (Extrínseca)
        
        if self._is_wall(nova_x, nova_y):
            # Bateu na parede, não se move
            nova_pos = pos_atual
            recompensa -= 0.5 # Penalidade extra por bater
        else:
            nova_pos = (nova_x, nova_y)
            
        self.agentes_posicoes[agente.nome] = nova_pos

        if nova_pos == self.end_pos:
            recompensa += 10.0 # Recompensa alta por atingir o objetivo
            self.terminou_flag = True # Termina o episódio

        # TODO: Implementar Recompensa Intrínseca para cooperação
        
        return recompensa

    def atualizacao(self):
        """Atualização do ambiente (apenas incrementa o contador de passos)."""
        self.passos_atuais += 1

    def terminou(self) -> bool:
        """O episódio termina se o objetivo for atingido ou se exceder o limite de passos."""
        if self.passos_atuais >= self.passos_maximos:
            return True
        return self.terminou_flag

    def visualizar(self):
        """Visualização simples do ambiente (grelha de texto)."""
        mapa_visual = [list(row) for row in self.mapa]
        
        # Ponto de Partida e Chegada
        mapa_visual[self.start_pos[1]][self.start_pos[0]] = 'S'
        mapa_visual[self.end_pos[1]][self.end_pos[0]] = 'E'
        
        # Agentes
        for nome, pos in self.agentes_posicoes.items():
            x, y = pos
            if mapa_visual[y][x] not in ('S', 'E'):
                mapa_visual[y][x] = nome[0].upper()
        
        print("-" * (self.largura + 2))
        for linha in mapa_visual:
            print("|" + "".join(linha) + "|")
        print("-" * (self.largura + 2))
        print(f"Passo: {self.passos_atuais}/{self.passos_maximos}")
        
        for nome, pos in self.agentes_posicoes.items():
            print(f"Agente {nome}: {pos}")
        print(f"Objetivo: {self.end_pos}")
