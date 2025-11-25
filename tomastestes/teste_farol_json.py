import sys
import os
import time
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Motor import MotorDeSimulacao

def teste_cenario_farol_json():
    print("=== Cenário de Teste: Problema do Farol (via JSON) ===")
    
    # Criar ficheiro JSON de configuração
    config = {
        "tipo": "farol",
        "ambiente": {
            "dimensao": [20, 20],
            "pos_farol": [18, 18],
            "obstaculos": [[5, 5], [10, 10]]
        },
        "agentes": [
            {"nome": "NavegadorJSON1", "posicao": [0, 0], "energia": 100},
            {"nome": "NavegadorJSON2", "posicao": [10, 0], "energia": 100}
        ]
    }
    
    json_file = "config_farol_temp.json"
    with open(json_file, "w") as f:
        json.dump(config, f)
    
    # 1. Criar Motor via Factory
    motor = MotorDeSimulacao.cria(json_file)
    
    print("Iniciando simulação com Threads...")
    
    # Executar X passos
    MAX_PASSOS = 20
    for i in range(MAX_PASSOS):
        print(f"\n--- Passo {i+1} ---")
        motor.executa()
        
        # Mostrar estado
        for a in motor.agentes:
            pos = motor.ambiente.agentes_posicoes[a]
            dist = motor.ambiente.observacaoPara(a).dados['distancia']
            print(f"{a.nome}: Pos={tuple(map(lambda x: round(x, 2), pos))} Dist={dist:.2f}")
            
        time.sleep(0.1)
        
    print("\n=== Fim do Teste ===")
    
    # Parar threads
    for a in motor.agentes:
        a.running = False
        a.start_step_event.set()
        
    # Limpeza
    if os.path.exists(json_file):
        os.remove(json_file)

if __name__ == "__main__":
    teste_cenario_farol_json()
