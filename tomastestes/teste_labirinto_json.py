import sys
import os
import time
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Motor import MotorDeSimulacao

def teste_cenario_labirinto_json():
    print("=== Cenário de Teste: Labirinto (via JSON) ===")
    
    # Criar ficheiro JSON de configuração
    config = {
        "tipo": "labirinto",
        "ambiente": {
            "dimensao": [10, 10],
            "paredes": [[1, 1], [1, 2], [2, 1], [5, 5], [5, 6], [6, 5]],
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
    
    json_file = "config_labirinto_temp.json"
    with open(json_file, "w") as f:
        json.dump(config, f)
    
    # 1. Criar Motor via Factory
    try:
        motor = MotorDeSimulacao.cria(json_file)
    except Exception as e:
        print(f"Erro ao criar motor: {e}")
        print("Verifique se o suporte a 'labirinto' está implementado no Motor.py")
        if os.path.exists(json_file):
            os.remove(json_file)
        return

    if not motor.ambiente:
        print("Ambiente não foi inicializado (provavelmente não implementado no Motor).")
        if os.path.exists(json_file):
            os.remove(json_file)
        return

    print("Iniciando simulação com Threads...")
    
    # Executar X passos
    MAX_PASSOS = 20
    for i in range(MAX_PASSOS):
        print(f"\n--- Passo {i+1} ---")
        motor.executa()
        
        # Mostrar estado
        for a in motor.agentes:
            # Assumindo que o ambiente tem um mapa de posições ou o agente sabe sua posição
            # No caso do AmbienteFarol, usamos motor.ambiente.agentes_posicoes[a]
            # Vamos tentar acessar de forma segura
            pos = getattr(a, "posicao", None)
            if hasattr(motor.ambiente, "agentes_posicoes") and a in motor.ambiente.agentes_posicoes:
                pos = motor.ambiente.agentes_posicoes[a]
            
            print(f"{a.nome}: Pos={pos}")
            
            # Mostrar observação se possível
            if a.ultima_observacao:
                print(f"   Obs: {a.ultima_observacao.dados}")

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
    teste_cenario_labirinto_json()
