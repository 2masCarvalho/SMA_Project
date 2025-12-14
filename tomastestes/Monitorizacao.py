import matplotlib.pyplot as plt
import csv
from typing import List, Dict

class MonitorDesempenho:
    """
    Classe responsável por recolher, armazenar e visualizar métricas de desempenho dos agentes.
    """
    def __init__(self):
        # Estrutura: {nome_agente: {'recompensas': [], 'passos': []}}
        self.dados_agentes: Dict[str, Dict[str, List[float]]] = {}

    def registar_episodio(self, nome_agente: str, recompensa_total: float, num_passos: int):
        """Regista os dados de um episódio (ou execução) para um agente."""
        if nome_agente not in self.dados_agentes:
            self.dados_agentes[nome_agente] = {'recompensas': [], 'passos': []}
        
        self.dados_agentes[nome_agente]['recompensas'].append(recompensa_total)
        self.dados_agentes[nome_agente]['passos'].append(num_passos)

    def gerar_relatorio_csv(self, nome_ficheiro: str = "relatorio_desempenho.csv"):
        """Exporta os dados recolhidos para um ficheiro CSV."""
        with open(nome_ficheiro, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Agente", "Episodio", "Recompensa", "Passos"])
            
            for nome, dados in self.dados_agentes.items():
                recompensas = dados['recompensas']
                passos = dados['passos']
                for i in range(len(recompensas)):
                    writer.writerow([nome, i+1, recompensas[i], passos[i]])
        print(f"Relatório guardado em {nome_ficheiro}")

    def plot_curva_aprendizagem(self, nome_ficheiro: str = "curva_aprendizagem.png"):
        """Gera e guarda um gráfico com a evolução das recompensas."""
        plt.figure(figsize=(10, 6))
        
        for nome, dados in self.dados_agentes.items():
            recompensas = dados['recompensas']
            plt.plot(recompensas, label=f"Agente: {nome}")
            
        plt.title("Curva de Aprendizagem (Recompensa por Episódio)")
        plt.xlabel("Episódio")
        plt.ylabel("Recompensa Total")
        plt.legend()
        plt.grid(True)
        plt.savefig(nome_ficheiro)
        print(f"Gráfico guardado em {nome_ficheiro}")
        plt.close()

    def get_media_recompensas(self, nome_agente: str = None) -> float:
        """
        Retorna a média das recompensas.
        Se nome_agente for fornecido, retorna a média desse agente.
        Caso contrário, retorna a média global de todos os registos.
        """
        todas_recompensas = []
        
        if nome_agente:
            if nome_agente in self.dados_agentes:
                todas_recompensas = self.dados_agentes[nome_agente]['recompensas']
        else:
            for dados in self.dados_agentes.values():
                todas_recompensas.extend(dados['recompensas'])
                
        if not todas_recompensas:
            return 0.0
            
        return sum(todas_recompensas) / len(todas_recompensas)
