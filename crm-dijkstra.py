"""
RafaLink CRM — Sprint 4
Autores: Felipe Lima, Luís Crivellaro, Rafael Mandel
"""

#
#  ESTRUTURA DO GRAFO
# 
# Representado como dicionário de adjacência:
# { nó_origem: [(nó_destino, custo), ...] }
#
# Épicos cobertos:
#   Épico 1 — Gestão de Usuários e Acesso
#   Épico 2 — Gestão de Leads e Funil de Vendas
#   Épico 3 — Comunicação e Agendamentos
#   Épico 4 — Relatórios e Inteligência de Dados

CRM_GRAPH: dict[str, list[tuple[str, int]]] = {
    # Épico 1: Gestão de Usuários
    "Lead": [
        ("Cadastro_Usuario", 1),    
        ("Qualificacao", 3),         
    ],
    "Cadastro_Usuario": [
        ("Definicao_Acesso", 1),     
    ],
    "Definicao_Acesso": [
        ("Qualificacao", 2),         
    ],

    # Épico 2: Gestão de Leads e Funil de Vendas 
    "Qualificacao": [
        ("Em_Contato", 2),           
        ("Lead_Perdido", 5),         
    ],
    "Em_Contato": [
        ("Proposta_Enviada", 2),     
        ("Lead_Perdido", 4),
    ],
    "Proposta_Enviada": [
        ("Negociacao", 2),           
        ("Lead_Perdido", 3),
    ],
    "Negociacao": [
        ("Agendamento", 1),          
        ("Lead_Perdido", 3),
    ],

    # Épico 3: Comunicação e Agendamentos
    "Agendamento": [
        ("Notificacao_Enviada", 1),  
    ],
    "Notificacao_Enviada": [
        ("Sincronizacao_Agenda", 1), 
        ("Confirmacao", 3),          
    ],
    "Sincronizacao_Agenda": [
        ("Confirmacao", 1),          
    ],

    # Épico 4: Relatórios e Inteligência de Dados 
    "Confirmacao": [
        ("Dashboard_Atualizado", 1), 
    ],
    "Dashboard_Atualizado": [
        ("Relatorio_Gerado", 1),     
    ],
    "Relatorio_Gerado": [
        ("Previsao_IA", 2),          
    ],
    "Previsao_IA": [],               
    
    # Nó de descarte (sem saída)
    "Lead_Perdido": [],
}


#  ALGORITMO DE DIJKSTRA

def dijkstra(graph: dict, origem: str, destino: str) -> tuple[list[str], int]:
    """
    Encontra o menor caminho entre dois nós em um grafo ponderado
    direcionado usando o algoritmo de Dijkstra.

    Implementação manual com lista de prioridade,
    """

    if origem not in graph:
        raise ValueError(f"Nó de origem '{origem}' não encontrado no grafo.")
    if destino not in graph:
        raise ValueError(f"Nó de destino '{destino}' não encontrado no grafo.")

    distancias: dict[str, float] = {no: float("inf") for no in graph}
    distancias[origem] = 0
    predecessores: dict[str, str | None] = {no: None for no in graph}
    visitados: set[str] = set()

    while True:
        # Seleciona o nó não visitado com menor distância acumulada
        no_atual = None
        menor_dist = float("inf")
        for no in graph:
            if no not in visitados and distancias[no] < menor_dist:
                menor_dist = distancias[no]
                no_atual = no

        # Nenhum nó alcançável restante
        if no_atual is None:
            break

        # Destino alcançado
        if no_atual == destino:
            break

        visitados.add(no_atual)

        # Relaxamento das arestas
        for vizinho, peso in graph[no_atual]:
            if vizinho not in visitados:
                nova_dist = distancias[no_atual] + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    predecessores[vizinho] = no_atual

    # Verifica se o destino foi alcançado
    if distancias[destino] == float("inf"):
        raise ValueError(
            f"Não existe caminho entre '{origem}' e '{destino}'."
        )

    # Reconstrói o caminho percorrendo os predecessores de trás pra frente
    caminho = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = predecessores[no]
    caminho.reverse()

    return caminho, int(distancias[destino])


#  EXIBIÇÃO DO GRAFO

def exibir_grafo(graph: dict) -> None:
    """Imprime todas as arestas do grafo"""
    print("=" * 60)
    print("  GRAFO DO FLUXO CRM — RafaLink")
    print("=" * 60)

    epicos = {
        "── Épico 1: Gestão de Usuários e Acesso": [
            "Lead", "Cadastro_Usuario", "Definicao_Acesso"
        ],
        "── Épico 2: Gestão de Leads e Funil de Vendas": [
            "Qualificacao", "Em_Contato", "Proposta_Enviada", "Negociacao"
        ],
        "── Épico 3: Comunicação e Agendamentos": [
            "Agendamento", "Notificacao_Enviada", "Sincronizacao_Agenda"
        ],
        "── Épico 4: Relatórios e Inteligência de Dados": [
            "Confirmacao", "Dashboard_Atualizado", "Relatorio_Gerado", "Previsao_IA"
        ],
        "── Nó de Descarte": ["Lead_Perdido"],
    }

    for titulo, nos in epicos.items():
        print(f"\n{titulo}")
        for no in nos:
            arestas = graph.get(no, [])
            if arestas:
                for vizinho, custo in arestas:
                    print(f"   {no:25s} ──({custo})──▶  {vizinho}")
            else:
                print(f"   {no:25s} [nó terminal]")

    total_nos = len(graph)
    total_arestas = sum(len(v) for v in graph.values())
    print(f"\n  Total: {total_nos} nós | {total_arestas} arestas")
    print("=" * 60)



#  EXIBIÇÃO DO RESULTADO

def exibir_resultado(caminho: list[str], custo: int) -> None:
    """Imprime o menor caminho encontrado com análise interpretativa."""

    print("\n" + "=" * 60)
    print("  RESULTADO — MENOR CAMINHO: Lead → Confirmação")
    print("=" * 60)

    # Caminho passo a passo com custos individuais
    print("\n  Caminho encontrado:\n")
    custo_acumulado = 0
    for i, no in enumerate(caminho):
        if i == 0:
            print(f"  ->  {no} (início)")
        else:
            # Busca o custo da aresta anterior -> atual
            origem_no = caminho[i - 1]
            for vizinho, peso in CRM_GRAPH[origem_no]:
                if vizinho == no:
                    custo_acumulado += peso
                    print(f"     │  custo: {peso}")
                    print(f"  ▶  {no}  [acumulado: {custo_acumulado}]")
                    break

    print(f"\n  Custo total do caminho: {custo}")


# ─────────────────────────────────────────────
#  PONTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    #Exibe o grafo completo
    exibir_grafo(CRM_GRAPH)

    #Executa Dijkstra de Lead → Confirmacao
    try:
        caminho, custo = dijkstra(CRM_GRAPH, "Lead", "Confirmacao")
        exibir_resultado(caminho, custo)
    except ValueError as e:
        print(f"\n[ERRO] {e}")