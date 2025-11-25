import math
import random
from typing import Dict, Any, Tuple
from ..core.interfaces import Ambiente, Agente, Observacao, Accao

class AmbienteFarol(Ambiente):
    """Ambiente 2D para o problema do Farol."""
    def __init__(self, farol_posicao: Tuple[float, float], tamanho_grelha: int = 10):
        self.farol_posicao = farol_posicao
        self.tamanho_grelha = tamanho_grelha
        self.agentes_posicoes: Dict[str, Tuple[float, float]] = {}
        self.passos_maximos = 100
        self.passos_atuais = 0
        self.terminou_flag = False
 # mudar isto yufdp
    def adicionar_agente(self, agente: Agente):
        """Adiciona um agente ao ambiente em uma posição inicial aleatória (exceto no farol)."""
        while True:
            x = random.randint(0, self.tamanho_grelha - 1)
            y = random.randint(0, self.tamanho_grelha - 1)
            if (x, y) != self.farol_posicao:
                self.agentes_posicoes[agente.nome] = (x, y)
                break

    def reset(self):
        """Reinicia o ambiente, colocando os agentes em posições aleatórias (exceto no farol)."""
        self.passos_atuais = 0
        self.terminou_flag = False
        
        # Reposiciona os agentes
        for nome in self.agentes_posicoes.keys():
            while True:
                x = random.randint(0, self.tamanho_grelha - 1)
                y = random.randint(0, self.tamanho_grelha - 1)
                if (x, y) != self.farol_posicao:
                    self.agentes_posicoes[nome] = (x, y)
                    break

    def observacao_para(self, agente: Agente) -> Observacao:
        """
        Gera a observação: apenas a direção do farol.
        A observação é um vetor unitário (dx, dy) que aponta para o farol.
        """
        pos_agente = self.agentes_posicoes[agente.nome]
        dx = self.farol_posicao[0] - pos_agente[0]
        dy = self.farol_posicao[1] - pos_agente[1]

        distancia = math.sqrt(dx**2 + dy**2)
        
        # Se a distância for zero, o agente está no farol.
        if distancia < 1e-6:
            self.terminou_flag = True
            return Observacao({"direcao_farol": (0.0, 0.0), "no_farol": True})
        
        # Vetor unitário de direção
        direcao_unit = (dx / distancia, dy / distancia)
        
        return Observacao({"direcao_farol": direcao_unit, "no_farol": False})

    def agir(self, accao: Accao, agente: Agente) -> float:
        """Processa a ação de movimento e calcula a recompensa."""
        if accao.tipo != "mover":
            return -0.1 # Penalidade por ação inválida

        pos_atual = self.agentes_posicoes[agente.nome]
        dx, dy = accao.parametros.get("dx", 0), accao.parametros.get("dy", 0)
        
        # Novo cálculo de posição, garantindo que fica dentro da grelha
        nova_x = max(0, min(self.tamanho_grelha - 1, pos_atual[0] + dx))
        nova_y = max(0, min(self.tamanho_grelha - 1, pos_atual[1] + dy))
        
        nova_pos = (nova_x, nova_y)
        self.agentes_posicoes[agente.nome] = nova_pos

        # Recompensa Extrínseca:
        recompensa = -0.01 # Custo de energia por passo
        
        if nova_pos == self.farol_posicao:
            recompensa += 10.0 # Recompensa alta por atingir o objetivo
            self.terminou_flag = True
        
        return recompensa

    def atualizacao(self):
        """Atualização do ambiente (apenas incrementa o contador de passos)."""
        self.passos_atuais += 1

    def terminou(self) -> bool:
        """O episódio termina se algum agente atingir o farol ou se exceder o limite de passos."""
        if self.passos_atuais >= self.passos_maximos:
            return True
        return self.terminou_flag

    def visualizar(self):
        """Visualização simples do ambiente (grelha de texto)."""
        grelha = [["." for _ in range(self.tamanho_grelha)] for _ in range(self.tamanho_grelha)]
        
        # Farol
        fx, fy = map(int, self.farol_posicao)
        grelha[fy][fx] = "F"
        
        # Agentes
        for nome, pos in self.agentes_posicoes.items():
            ax, ay = map(int, pos)
            if grelha[ay][ax] == ".":
                grelha[ay][ax] = nome[0].upper() # Usa a primeira letra do nome
            elif grelha[ay][ax] != "F":
                grelha[ay][ax] = "X" # Colisão ou múltiplos agentes
        
        print("-" * (self.tamanho_grelha * 2 + 1))
        for linha in grelha:
            print("|" + "|".join(linha) + "|")
        print("-" * (self.tamanho_grelha * 2 + 1))
        print(f"Passo: {self.passos_atuais}/{self.passos_maximos}")
        
        for nome, pos in self.agentes_posicoes.items():
            print(f"Agente {nome}: {pos}")
        print(f"Farol: {self.farol_posicao}")
