import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AmbienteFarol import AmbienteFarol
from AgenteRL import AgenteRL
from Politica import PoliticaQLearning
from Motor import MotorDeSimulacao
from Monitorizacao import MonitorDesempenho

def executar_experiencia(monitor, alpha, gamma, epsilon_inicial, num_episodios, nome_experiencia):
    print(f"--- Iniciando Experiência: {nome_experiencia} (Alpha={alpha}, Gamma={gamma}) ---")
    
    # Configurar Política
    accoes_possiveis = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    politica = PoliticaQLearning(accoes_possiveis, alpha=alpha, gamma=gamma, epsilon=epsilon_inicial)
    
    MAX_PASSOS = 500
    
    for episodio in range(num_episodios):
        # Configurar Ambiente e Agente
        ambiente = AmbienteFarol(
            farol_pos=(8, 8), 
            dimensoes=(10, 10),
            obstaculos=[(5, 5), (2, 2)]
        )
        
        agente = AgenteRL(nome_experiencia, politica)
        ambiente.adicionar_agente(agente, (0, 0))
        
        motor = MotorDeSimulacao(ambiente, [agente])
        
        # Decay Epsilon
        politica.epsilon = max(0.01, politica.epsilon * 0.95)
        
        passos = 0
        while passos < MAX_PASSOS:
            motor.executa()
            passos += 1
            
            obs = ambiente.observacaoPara(agente)
            if obs.dados['distancia'] < 1.0:
                break
        
        # Registar dados
        monitor.registar_episodio(nome_experiencia, agente.recompensa_total, passos)
        
        # Limpeza da thread
        agente.running = False
        agente.start_step_event.set()
        agente.join()
        
    print(f"Experiência {nome_experiencia} concluída.\n")

def main():
    monitor = MonitorDesempenho()
    
    # Definir parâmetros a testar
    # Exemplo: Testar diferentes Learning Rates (Alpha)
    experiencias = [
        {"alpha": 0.1, "gamma": 0.9, "nome": "Alpha=0.1 (Lento)"},
        {"alpha": 0.5, "gamma": 0.9, "nome": "Alpha=0.5 (Medio)"},
        {"alpha": 0.9, "gamma": 0.9, "nome": "Alpha=0.9 (Rapido)"}
    ]
    
    NUM_EPISODIOS = 50
    
    for exp in experiencias:
        executar_experiencia(
            monitor, 
            alpha=exp["alpha"], 
            gamma=exp["gamma"], 
            epsilon_inicial=0.5, 
            num_episodios=NUM_EPISODIOS, 
            nome_experiencia=exp["nome"]
        )
        
    # Gerar Gráfico
    print("Gerando gráfico comparativo...")
    monitor.plot_curva_aprendizagem("comparacao_alphas.png")
    monitor.gerar_relatorio_csv("comparacao_alphas.csv")

if __name__ == "__main__":
    main()
