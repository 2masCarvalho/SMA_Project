import sys
import os
import time
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Motor import MotorDeSimulacao
from visualizador import VisualizadorTk

def teste_cenario_labirinto_visual():
    print("=== Cenário de Teste Visual: Labirinto ===")
    
    # Criar ficheiro JSON de configuração
    config = {
        "tipo": "labirinto",
        "ambiente": {
            "dimensao": [10, 10],
            "paredes": [[1, 1], [1, 2], [2, 1], [3, 3], [3, 4], [4, 3], [5, 5], [5, 6], [6, 5], [7, 7], [7, 8], [8, 7]],
            "inicio": [0, 0],
            "saida": [9, 9]
        },
        "agentes": [
            {
                "nome": "Explorador1", 
                "subtipo": "explorador", 
                "posicao": [0, 0]
            },
            {
                "nome": "Inteligente1", 
                "subtipo": "inteligente", 
                "posicao": [0, 1]
            }
        ]
    }
    
    json_file = "config_labirinto_visual.json"
    with open(json_file, "w") as f:
        json.dump(config, f)
    
    # 1. Criar Motor via Factory
    motor = MotorDeSimulacao.cria(json_file)
    
    # 2. Inicializar Visualizador
    largura, altura = config["ambiente"]["dimensao"]
    viz = VisualizadorTk(largura, altura, tamanho_celula=40)
    
    print("Iniciando simulação com Visualização...")
    
    # Executar X passos
    MAX_PASSOS = 100
    try:
        for i in range(MAX_PASSOS):
            motor.executa()
            
            # Atualizar Visualização
            viz.desenhar(motor.ambiente, motor.agentes)
            
            time.sleep(0.2) # Pausa para animação
            
    except KeyboardInterrupt:
        print("Interrompido pelo utilizador.")
    finally:
        print("\n=== Fim do Teste ===")
        # Parar threads
        for a in motor.agentes:
            a.running = False
            a.start_step_event.set()
        
        # Limpeza
        if os.path.exists(json_file):
            os.remove(json_file)
            
        # Manter janela aberta por uns segundos ou fechar
        # viz.fechar() 
        # viz.root.mainloop() # Se quiséssemos manter aberta

if __name__ == "__main__":
    teste_cenario_labirinto_visual()
