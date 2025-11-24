import random
import sys, pathlib
if __package__ is None and __name__ == "__main__":
    sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from .core.motor import MotorDeSimulacao
from .ambientes.farol import AmbienteFarol
from .agentes.reativo import AgenteReativoFarol
from .ambientes.labirinto import AmbienteLabirinto
from .agentes.aprendizagem import AgenteAprendizagemLabirinto

def exemplo_farol():
    """Demonstração do Problema do Farol com Agentes Reativos."""
    print("==================================================")
    print("EXEMPLO 1: PROBLEMA DO FAROL (Agentes Reativos)")
    print("==================================================")
    
    # Configuração do Ambiente
    farol_pos = (8, 8)
    ambiente_farol = AmbienteFarol(farol_pos, tamanho_grelha=10)

    # Configuração dos Agentes
    agente1 = AgenteReativoFarol("A1")
    agente2 = AgenteReativoFarol("A2")
    
    agentes_lista_farol = [agente1, agente2]

    # Configuração e Execução do Motor de Simulação
    motor_farol = MotorDeSimulacao(ambiente_farol, agentes_lista_farol)
    motor_farol.executa(max_episodios=1)

def exemplo_labirinto():
    """Demonstração do Problema do Labirinto com Agentes de Aprendizagem (Q-Learning)."""
    print("\n==================================================")
    print("EXEMPLO 2: PROBLEMA DO LABIRINTO (Agentes de Aprendizagem)")
    print("==================================================")
    
    # Mapa do Labirinto (S: Start, E: End, #: Parede, .: Caminho)
    mapa_labirinto = [
        "#########",
        "#S  #   #",
        "# # # # #",
        "# #   # #",
        "# ##### #",
        "#       E",
        "#########"
    ]
    start = (1, 1)
    end = (7, 5)
    
    ambiente_labirinto = AmbienteLabirinto(mapa_labirinto, start, end)
    
    acoes_labirinto = ["N", "S", "E", "O"]
    agente_q1 = AgenteAprendizagemLabirinto("Q1", acoes_labirinto)
    agente_q2 = AgenteAprendizagemLabirinto("Q2", acoes_labirinto)
    
    agentes_lista_labirinto = [agente_q1, agente_q2]
    
    motor_labirinto = MotorDeSimulacao(ambiente_labirinto, agentes_lista_labirinto)
    
    # Executar múltiplos episódios para que o Q-Learning aprenda
    print("A iniciar a fase de aprendizagem (100 episódios)...")
    
    # Aumentar o epsilon para garantir a exploração durante a aprendizagem
    agente_q1.politica.epsilon = 0.5
    agente_q2.politica.epsilon = 0.5
    
    motor_labirinto.executa(max_episodios=100)
    
    # Reduzir o epsilon para testar a política aprendida (Modo de Teste)
    agente_q1.politica.epsilon = 0.0
    agente_q2.politica.epsilon = 0.0
    
    print("\nA iniciar a fase de teste (1 episódio com política aprendida)...")
    motor_labirinto.executa(max_episodios=1)

if __name__ == "__main__":
    # Definir uma seed para reprodutibilidade
    random.seed(42)
    
    exemplo_farol()
    exemplo_labirinto()
