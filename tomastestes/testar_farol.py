import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AmbienteFarol import AmbienteFarol
from AgenteRL import AgenteRL
from Politica import PoliticaQLearning
from Motor import MotorDeSimulacao
from Modelos import Observacao # Necessário para o passo final

def treinar_farol():
    print("=== Treino: Problema do Farol (Q-Learning Otimizado) ===")
    
    # === CORREÇÃO 1: Aumentar drasticamente o treino ===
    NUM_EPISODIOS = 3000      # De 100 para 3000
    MAX_PASSOS = 100          # Dar mais tempo para ele errar no início
    Q_TABLE_FILE = "qtable_farol.pkl"
    
    accoes_possiveis = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    # === CORREÇÃO 2: Epsilon começa em 1.0 (100% aleatório) ===
    politica = PoliticaQLearning(accoes_possiveis, alpha=0.1, gamma=0.9, epsilon=1.0)
    
    if os.path.exists(Q_TABLE_FILE):
        print("A carregar política existente...")
        politica.carregar(Q_TABLE_FILE)
        # Se carregamos, começamos com epsilon mais baixo para refinar
        politica.epsilon = 0.3 

    for episodio in range(NUM_EPISODIOS):
        
        # === CORREÇÃO 3: Limpar a memória de curto prazo da política ===
        # Para não misturar o fim do episódio anterior com o início deste
        politica.ultimo_estado = None 
        politica.ultima_accao = None
        politica.ultima_recompensa = 0.0

        pos_inicial = (0, 0)
        # Randomizar ligeiramente o início ajuda a generalizar (opcional)
        if random.random() < 0.1: 
             pos_inicial = (random.randint(0,2), random.randint(0,2))

        ambiente = AmbienteFarol(
            farol_pos=(8, 8), 
            dimensoes=(10, 10),
            obstaculos=[(5, 5), (2, 2)]
        )
        
        agente = AgenteRL("AgenteAprendiz", politica)
        ambiente.adicionar_agente(agente, pos_inicial)
        motor = MotorDeSimulacao(ambiente, [agente])
        
        # Decaimento do Epsilon (Exploration Decay)
        # Reduz até 0.01 (1% aleatório)
        if politica.epsilon > 0.01:
            politica.epsilon *= 0.998 
        
        passos = 0
        chegou = False
        
        while passos < MAX_PASSOS:
            motor.executa()
            passos += 1
            
            obs = ambiente.observacaoPara(agente)
            dist = obs.dados['distancia']
            
            # Condição de Vitória
            if dist < 1.0:
                chegou = True
                
                # === CORREÇÃO 4 (CRUCIAL): Forçar o update do passo vencedor ===
                # O loop vai quebrar, então temos de dizer à política:
                # "Olha, a última ação que fizeste levou-te a ESTE estado final e ganhaste X"
                
                # Criamos uma 'observação final' artificial para fechar a conta matemática
                estado_final = politica.get_estado_key(obs)
                
                # Acedemos à função interna de update (batota permitida no treino)
                # Q(S_ant, A_ant) = R + ...
                if politica.ultimo_estado and politica.ultima_accao:
                    politica._atualizar_q_table(
                        politica.ultimo_estado, 
                        politica.ultima_accao, 
                        agente.recompensa_total, # Ou a recompensa instantânea do passo
                        estado_final
                    )
                break
        
        # Logs de progresso
        if (episodio + 1) % 100 == 0:
            status = "SUCESSO" if chegou else "FALHA"
            print(f"Episódio {episodio+1} | {status} | Passos: {passos} | Epsilon: {politica.epsilon:.3f}")

        agente.running = False
        agente.start_step_event.set()
        # Não precisamos do join() estrito aqui se o motor gerir bem as threads, 
        # mas ajuda a limpar

    print("\n=== Treino Concluído ===")
    politica.salvar(Q_TABLE_FILE)
    print(f"Tabela Q salva com sucesso em {Q_TABLE_FILE}")

if __name__ == "__main__":
    treinar_farol()