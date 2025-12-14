import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AmbienteFarol import AmbienteFarol
from AgenteRL import AgenteRL
from Politica import PoliticaQLearning
from Motor import MotorDeSimulacao

def testar_farol():
    print("=== Teste: Problema do Farol (Agente Treinado) ===")
    
    Q_TABLE_FILE = "qtable_farol.pkl"
    if not os.path.exists(Q_TABLE_FILE):
        print(f"ERRO: Ficheiro de política {Q_TABLE_FILE} não encontrado. Execute treinar_farol.py primeiro.")
        return

    # 1. Configurar Política (Epsilon=0 para exploração nula, apenas exploração)
    accoes_possiveis = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    politica = PoliticaQLearning(accoes_possiveis, epsilon=0.0) 
    politica.carregar(Q_TABLE_FILE)
    
    # 2. Configurar Ambiente
    ambiente = AmbienteFarol(
        farol_pos=(8, 8), 
        dimensoes=(10, 10),
        obstaculos=[(5, 5), (2, 2)]
    )
    
    # 3. Configurar Agente
    agente = AgenteRL("AgenteTreinado", politica)
    ambiente.adicionar_agente(agente, (0, 0))
    
    motor = MotorDeSimulacao(ambiente, [agente])
    
    print("Iniciando teste...")
    MAX_PASSOS = 50
    for i in range(MAX_PASSOS):
        print(f"\n--- Passo {i+1} ---")
        motor.executa()
        
        pos = ambiente.agentes_posicoes[agente]
        dist = ambiente.observacaoPara(agente).dados['distancia']
        ambiente.display()
        # print(f"Pos={tuple(map(lambda x: round(x, 2), pos))} Dist={dist:.2f}")
        
        if dist < 1.0:
            print("!!! SUCESSO: O agente chegou ao farol! !!!")
            break
            
        time.sleep(0.1)
        
    # Parar threads
    agente.running = False
    agente.start_step_event.set()

if __name__ == "__main__":
    testar_farol()
