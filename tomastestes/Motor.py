import json
from AmbienteFarol import AmbienteFarol
# Assuming AgenteFarol is AgenteDirecional for now, or we need to import it if it exists separately.
# Based on previous context, AgenteDirecional is the one used for Farol.
from agente import AgenteDirecional as AgenteFarol
# Placeholder for Labirinto classes if they don't exist yet, or import if they do.
# We will just comment them out or assume they exist if the user asks for Labirinto later.
# For now, let's import what we have.
from agente import AgenteExplorador as AgenteLabirinto
# We need a placeholder for AmbienteLabirinto or import it if it exists.
# It doesn't exist in tomastestes yet, so we'll define a dummy or import if created.
# I'll assume AmbienteLabirinto is not yet created in tomastestes, so I will leave it as is but it might fail if called.
# Actually, let's just fix the Farol part which is requested.

class MotorDeSimulacao:
    def __init__(self, ambiente , agentes):
        self.ambiente = ambiente
        self.agentes = agentes
        for agente in self.agentes:
            agente.set_ambiente(self.ambiente)
            agente.start()

    #O método executa() faz um ciclo completo: todos os agentes observam, 
    # processam, decidem ação e o ambiente executa. Depois atualiza o ambiente
    def executa(self):
        # 1. Trigger all agents to start their step
        for agente in self.agentes:
            agente.end_step_event.clear()
            agente.start_step_event.set()
        
        # 2. Wait for all agents to finish their step
        for agente in self.agentes:
            agente.end_step_event.wait()
            
        # 3. Update environment
        self.ambiente.atualizacao()

    @staticmethod
    def cria(nome_do_ficheiro_parametros: str) -> 'MotorDeSimulacao': 
        with open(nome_do_ficheiro_parametros, 'r') as f: 
            params = json.load(f)

        tipo = params["tipo"]
        ambiente = None
        agentes = []

        if tipo == "farol":
            # Extract environment params
            env_params = params["ambiente"]
            ambiente = AmbienteFarol(
                farol_pos=tuple(env_params["pos_farol"]),
                dimensoes=tuple(env_params["dimensao"]),
                obstaculos=[tuple(o) for o in env_params.get("obstaculos", [])]
            )
            
            for agente_info in params["agentes"]:
                # Map JSON keys to constructor args
                agente = AgenteFarol(
                    nome=agente_info.get("nome", "Agente"),
                    posicao=tuple(agente_info.get("posicao", [0,0])),
                    energia=agente_info.get("energia", 100)
                )
                ambiente.adicionar_agente(agente, agente.posicao)
                agentes.append(agente)
                
        elif tipo == "labirinto":
            # Placeholder implementation
            pass
            # ambiente = AmbienteLabirinto(params["ambiente"])
            # for agente_info in params["agentes"]:
            #     agente = AgenteLabirinto(**agente_info)
            #     agentes.append(agente) 
        
        return MotorDeSimulacao(ambiente, agentes)