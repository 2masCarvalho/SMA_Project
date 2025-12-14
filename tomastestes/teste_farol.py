import sys
import os
import time
import threading

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente import AgenteDirecional
from AmbienteFarol import AmbienteFarol
from Motor import MotorDeSimulacao

def teste_cenario_farol():
    print("=== Cenário de Teste: Problema do Farol ===")
    
    # 1. Configurar Ambiente
    # Grelha 20x20, Farol em (18, 18)
    # Obstáculos em (5,5) e (10,10)
    ambiente = AmbienteFarol(
        farol_pos=(8, 8), 
        dimensoes=(10, 10),
        obstaculos=[(5, 5), (2, 2)]
    )
    
    # 2. Configurar Agentes
    # Agente 1 começa longe (0,0)
    # Agente 2 começa mais perto (10, 0)
    agente1 = AgenteDirecional("Navegador1", posicao=(0, 0), energia=100)
    agente2 = AgenteDirecional("Navegador2", posicao=(10, 0), energia=100)
    
    # Registar agentes no ambiente (para o ambiente saber onde eles estão)
    ambiente.adicionar_agente(agente1, (0, 0))
    ambiente.adicionar_agente(agente2, (10, 0))
    
    agentes = [agente1, agente2]
    
    # 3. Inicializar Motor
    motor = MotorDeSimulacao(ambiente, agentes)
    
    print("Iniciando simulação com Threads...")
    
    # Executar X passos
    MAX_PASSOS = 20
    for i in range(MAX_PASSOS):
        print(f"\n--- Passo {i+1} ---")
        motor.executa()
        
        # Mostrar estado
        for a in agentes:
            pos = ambiente.agentes_posicoes[a]
            dist = ambiente.observacaoPara(a).dados['distancia']
            # print(f"{a.nome}: Pos={tuple(map(lambda x: round(x, 2), pos))} Dist={dist:.2f}")
        
        ambiente.display()
            
        time.sleep(0.1) # Pequena pausa para visualização
        
    print("\n=== Fim do Teste ===")
    
    # Parar threads dos agentes (hack simples para teste)
    for a in agentes:
        a.running = False
        a.start_step_event.set() # Desbloquear se estiverem à espera

if __name__ == "__main__":
    teste_cenario_farol()
