# RafaLink CRM — Sprint 4: Grafos e Dijkstra

> **Disciplina:** Engenharia de Software — 4° Semestre | FIAP  
> **Autores:** Felipe Lima (RM559848) - Luís Crivellaro (RM560877) - Rafael Mandel (RM560333)  
> **Versão:** 1.0

---

## Objetivo

Modelar o fluxo completo do **RafaLink CRM** como um grafo direcionado e aplicar o **algoritmo de Dijkstra** implementado manualmente para encontrar o caminho de menor custo entre as etapas **Lead → Confirmação**.

---

## Estrutura do Projeto

```
rafalink-crm-sprint4/
│
├── crm_dijkstra.py     # Código principal (grafo + Dijkstra + interpretação)
├── exibicao-grafo.dot  # Arquivo .dot para visualizacao ilustrativo do grafo 
└── README.md           # Documentação do projeto
```

---

## Representação do Fluxo como Grafo

O fluxo do CRM foi modelado como um **grafo direcionado e ponderado**.

Cada **nó** representa uma etapa do processo. Cada **aresta** possui um peso (custo) que representa o esforço relativo para transitar entre etapas — quanto menor o custo, mais eficiente a transição.

### Nós e Épicos

| Épico | Nós |
|-------|-----|
| **Épico 1** — Gestão de Usuários e Acesso | `Lead`, `Cadastro_Usuario`, `Definicao_Acesso` |
| **Épico 2** — Gestão de Leads e Funil de Vendas | `Qualificacao`, `Em_Contato`, `Proposta_Enviada`, `Negociacao` |
| **Épico 3** — Comunicação e Agendamentos | `Agendamento`, `Notificacao_Enviada`, `Sincronizacao_Agenda`, `Confirmacao` |
| **Épico 4** — Relatórios e Inteligência de Dados | `Dashboard_Atualizado`, `Relatorio_Gerado`, `Previsao_IA` |
| **Descarte** | `Lead_Perdido` |

> **Total:** 15 nós · 19 arestas

### Representação das Arestas

```
Lead ──(1)──▶ Cadastro_Usuario ──(1)──▶ Definicao_Acesso ──(2)──▶ Qualificacao
Lead ──(3)──▶ Qualificacao
Qualificacao ──(2)──▶ Em_Contato ──(2)──▶ Proposta_Enviada ──(2)──▶ Negociacao
Negociacao ──(1)──▶ Agendamento ──(1)──▶ Notificacao_Enviada
Notificacao_Enviada ──(1)──▶ Sincronizacao_Agenda ──(1)──▶ Confirmacao
Notificacao_Enviada ──(3)──▶ Confirmacao  (atalho, porém mais custoso)
[nós de descarte possuem arestas com custo alto: 3–5]
```

---

## Implementação do Algoritmo de Dijkstra

### Funcionamento

```python
def dijkstra(graph, origem, destino):
    ...
```

**Passos do algoritmo:**

1. Inicializa todas as distâncias como `infinito`, exceto a origem (distância `0`).
2. A cada iteração, seleciona o nó não visitado com **menor distância acumulada**.
3. Para cada vizinho do nó atual, **relaxa a aresta**: se o novo caminho for mais curto, atualiza a distância e registra o predecessor.
4. Repete até chegar ao nó destino ou esgotar os nós alcançáveis.
5. Reconstrói o caminho percorrendo os predecessores de trás para frente.

### Complexidade

| Aspecto | Valor |
|---------|-------|
| Temporal | O(V²) |
| Espacial | O(V)  |

> Para o tamanho do grafo do CRM (15 nós), O(V²) é plenamente adequado, porem pode se aprimorar o codigo para obter um aspecto temporal de O(n log(n)).

---

## Interpretação do Resultado

### Menor caminho encontrado

```
Lead → Qualificacao → Em_Contato → Proposta_Enviada
     → Negociacao → Agendamento → Notificacao_Enviada
     → Sincronizacao_Agenda → Confirmacao
```

### Custo total: **13**

| Aresta | Custo |
|--------|-------|
| Lead → Qualificacao | 3 |
| Qualificacao → Em_Contato | 2 |
| Em_Contato → Proposta_Enviada | 2 |
| Proposta_Enviada → Negociacao | 2 |
| Negociacao → Agendamento | 1 |
| Agendamento → Notificacao_Enviada | 1 |
| Notificacao_Enviada → Sincronizacao_Agenda | 1 |
| Sincronizacao_Agenda → Confirmacao | 1 |
| **Total** | **13** |

### Por que esse caminho é mais eficiente?

**1. Atalho na qualificação (custo 3 vs 1+1+2=4)**  
O algoritmo identificou que ir diretamente de `Lead → Qualificacao` (custo 3) é mais rápido do que passar pelo ciclo de cadastro `Lead → Cadastro → Definicao_Acesso → Qualificacao` (custo 4). Isso reflete um cenário onde o lead já é conhecido ou veio de uma integração externa.

**2. Funil comercial sem desvios**  
O caminho percorre `Qualificacao → Em_Contato → Proposta → Negociacao` sem desviar para `Lead_Perdido`, cujas arestas têm custos entre 3 e 5, representando o custo real de retrabalho e perda comercial.

**3. Automação de comunicação completa**  
O trajeto passa por `Notificacao_Enviada → Sincronizacao_Agenda → Confirmacao` (custo 1+1), em vez de usar o atalho direto `Notificacao_Enviada → Confirmacao` (custo 3). Isso demonstra que **usar a sincronização de agenda externa** — recurso de automação do Épico 3 — é mais eficiente do que ignorá-la.

**Conclusão:** o menor caminho é aquele que usa as automações e integrações do CRM de forma completa, evitando retrabalho, descarte de leads e transições manuais.

---

## Como Executar

**Requisito:** Python 3.10 ou superior

```bash
# Clone o repositório
git clone https://github.com/rflmandell/rafalink-crm-sprint4.git
cd rafalink-crm-sprint4

# Execute
python crm_dijkstra.py
```

### Saída esperada

```
============================================================
  GRAFO DO FLUXO CRM — RafaLink
============================================================
...
  Total: 15 nós | 19 arestas
============================================================

============================================================
  RESULTADO — MENOR CAMINHO: Lead → Confirmação
============================================================
  ->  Lead (início)
     │  custo: 3
  ->  Qualificacao  [acumulado: 3]
  ...
  ->  Confirmacao  [acumulado: 13]

  Custo total do caminho: 13
```

---