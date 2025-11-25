import sys
import os
import json
import threading

# Add current directory to path to allow imports from local files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente import Agente, AgenteDirecional, AgenteExplorador, AgenteInteligente
from Ambiente import Ambiente
from Modelos import Observacao, Accao
from Motor import MotorDeSimulacao
from Sensor import Sensor

# Mock classes for testing since Ambiente is abstract and Motor expects specific implementations
class AmbienteMock(Ambiente):
    def __init__(self):
        super().__init__()
        self.passos = 0
    
    def observacaoPara(self, agente):
        if isinstance(agente, AgenteDirecional):
            return Observacao({"direcao": (1, 0)})
        elif isinstance(agente, AgenteExplorador):
            return Observacao({"caminhos": ["N", "S"]})
        return Observacao({})

    def atualizacao(self):
        self.passos += 1
        print(f"Ambiente atualizado. Passo: {self.passos}")

    def _agir_safe(self, accao, agente):
        print(f"Agente {agente.nome} (Thread {threading.get_ident()}) realizou acao: {accao}")
        agente.avaliacao_estado_atual(1.0)
        return 1.0

def teste_manual():
    print("=== Iniciando Teste Manual ===")
    
    # 1. Testar Criação de Agentes via Factory
    print("\n--- Teste Factory de Agentes ---")
    # Criar um JSON temporário para teste
    dados_farol = {
        "tipo": "farol",
        "agentes": [
            {"nome": "AgenteFarol1", "posicao": [0, 0], "energia": 100},
            {"nome": "AgenteFarol2", "posicao": [10, 10], "energia": 80}
        ]
    }
    
    with open("temp_farol.json", "w") as f:
        json.dump(dados_farol, f)
        
    agentes = Agente.cria("temp_farol.json")
    print(f"Agentes criados: {len(agentes)}")
    for a in agentes:
        print(f" - {a.nome} ({type(a).__name__})")
        
    # 2. Testar Sensores
    print("\n--- Teste Sensores ---")
    sensor = Sensor("proximidade", {"alcance": 5})
    agentes[0].instala(sensor)
    print(f"Sensor instalado em {agentes[0].nome}: {agentes[0].sensores}")

    # 3. Testar Motor de Simulação
    print("\n--- Teste Motor de Simulação ---")
    ambiente = AmbienteMock()
    motor = MotorDeSimulacao(ambiente, agentes)
    
    print("Executando 1 passo de simulação...")
    motor.executa()
    
    # Verificar estado dos agentes
    print("\nEstado dos Agentes após execução:")
    for a in agentes:
        print(f"Agente {a.nome}: Recompensa Total={a.recompensa_total}, Passos={a.passos}")
        if a.ultima_observacao:
            print(f"  Última Observação: {a.ultima_observacao}")

    # Limpeza
    if os.path.exists("temp_farol.json"):
        os.remove("temp_farol.json")
        
    print("\n=== Teste Concluído ===")

if __name__ == "__main__":
    teste_manual()
