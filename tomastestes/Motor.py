import json

class MotorDeSimulacao:
    def __init__(self, ambiente , agentes):
        self.ambiente = ambiente
        self.agentes = agentes

#O método executa() faz um ciclo completo: todos os agentes observam, 
# processam, decidem ação e o ambiente executa. Depois atualiza o ambiente
    def executa(self):
        for agente in self.agentes:
            observacao = self.ambiente.observacaoPara(agente)
            agente.observacao(observacao)
            accao = agente.age()
            self.ambiente.agir(accao, agente)
        self.ambiente.atualizacao()




    def cria(nome_do_ficheiro_parametros: str) -> MotorDeSimulacao: 
        with open(nome_do_ficheiro_parametros, 'r') as f: 
            linhas = json.load(f)

        tipo = params["tipo"]
        ambiente = None
        agentes = []

        if tipo == "farol":
            ambiente = AmbienteFarol(params["ambiente"])
            for agente_info in params["agentes"]:
                agente = AgenteFarol(**agente_info)
                agentes.append(agente)
        elif tipo == "labirinto":
            ambiente = AmbienteLabirinto(params["ambiente"])
            for agente_info in params["agentes"]:
                agente = AgenteLabirinto(**agente_info)
                agentes.append(agente) 
        
        return MotorDeSimulacao(ambiente, agentes)
            