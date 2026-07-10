## Indicadores Monitorados

O sistema acompanha indicadores financeiros, de clientes, produto, vendas, aquisição e retenção. Cada indicador é comparado com benchmarks esperados para o setor da empresa (`saas`, `marketplace`, `hardware`, `fintech` ou `ecommerce`).

Os benchmarks são usados para classificar o desempenho do indicador como:

- **Good**: desempenho acima ou dentro de uma faixa saudável.
- **Warning**: desempenho aceitável, mas que merece atenção.
- **Bad**: desempenho abaixo do esperado.

---

### Indicadores Financeiros

| Indicador | Significado |
|---|---|
| **MRR Growth** | Crescimento percentual da receita recorrente mensal em relação ao mês anterior. Mede a velocidade de crescimento da receita previsível. |
| **ARR (Annual Recurring Revenue)** | Receita recorrente anualizada. Representa a projeção anual da receita recorrente atual, calculada como MRR × 12. É uma métrica de escala e crescimento da empresa. |
| **Net Revenue Retention (NRR)** | Mede quanto da receita dos clientes existentes permaneceu após considerar churn e expansão. NRR acima de 100% indica crescimento da base sem novas vendas. |
| **CAC Payback** | Quantidade de meses necessários para recuperar o custo de aquisição de um cliente. Quanto menor, melhor. |
| **LTV:CAC Ratio** | Relação entre o valor gerado por um cliente durante sua vida útil (LTV) e o custo para adquirir esse cliente (CAC). |
| **Burn Multiple** | Relação entre o dinheiro consumido pela empresa e o crescimento de receita gerado. Mede eficiência de capital. |
| **Runway** | Estimativa de quantos meses a empresa consegue operar considerando o caixa atual e o burn mensal. |
| **Burn Rate** | Valor gasto pela empresa por mês para manter a operação. |
| **Rule of 40** | Soma da taxa de crescimento da receita com a margem EBITDA. Usado para avaliar equilíbrio entre crescimento e rentabilidade. |

---

|Métrica	| Significado |
|---|---|
|**MRR**	|Receita recorrente gerada em um único mês. Mostra a situação atual da receita.
|**ARR**	|Receita recorrente projetada para um ano inteiro baseada no MRR atual. Mostra a escala anualizada do negócio.

---


---

### Indicadores de Clientes

| Indicador | Significado |
|---|---|
| **Active Customers** | Número de clientes ativos atualmente. |
| **Retention Rate** | Percentual de clientes que continuam ativos após determinado período. |
| **Net Revenue Retention (NRR)** | Mede retenção considerando expansão de receita e perda de clientes existentes. |
| **DAU/MAU Ratio** | Relação entre usuários ativos diariamente e usuários ativos mensalmente. Mede frequência de uso do produto. |

---

### Indicadores de Produto

| Indicador | Significado |
|---|---|
| **Activation Rate** | Percentual de novos usuários que atingem um evento considerado como ativação do produto. |
| **Trial Conversion Rate** | Percentual de usuários em teste que se tornam clientes pagantes. |
| **Time To Value (TTV)** | Tempo necessário para o usuário perceber valor inicial no produto. Quanto menor, melhor. |

---

### Indicadores de Vendas

| Indicador | Significado |
|---|---|
| **Win Rate** | Percentual de oportunidades comerciais convertidas em vendas. |
| **Sales Cycle Length** | Tempo médio necessário para fechar uma venda. |
| **Funnel Conversion Rate** | Percentual de conversão entre etapas do funil comercial. |

---

### Indicadores de Aquisição

| Indicador | Significado |
|---|---|
| **CAC por Canal** | Custo para adquirir clientes através de cada canal de marketing. |
| **Google Ads CAC** | Custo médio dos clientes adquiridos via Google Ads. |
| **Meta Ads CAC** | Custo médio dos clientes adquiridos via Meta Ads. |
| **Outbound CAC** | Custo médio dos clientes adquiridos através de vendas outbound. |

---

## Benchmark por Setor

Os benchmarks são adaptados ao modelo de negócio.

Exemplos:

| Indicador | SaaS saudável |
|---|---|
| Burn Multiple | < 1.5 |
| NRR | > 108% |
| CAC Payback | < 18 meses |
| Runway | > 18 meses |
| LTV:CAC | > 3 |
| Rule of 40 | > 40 |

Os valores mudam conforme o setor cadastrado da empresa.

---

# Análise de Coortes

O sistema possui uma análise de retenção por coortes.

Uma **coorte** é um grupo de clientes que iniciou relacionamento com a empresa no mesmo período.

Exemplo:

Clientes cadastrados em janeiro de 2024 formam a coorte de janeiro/2024.

O heatmap acompanha esse grupo ao longo do tempo:

| Coluna | Significado |
|---|---|
| M0 | Primeiro mês após aquisição |
| M1 | Um mês depois da aquisição |
| M2 | Dois meses depois |
| M12 | Doze meses depois |

A porcentagem representa quantos clientes daquela coorte continuam ativos.

Exemplo:

| Coorte | M0 | M1 | M2 |
|-|-|-|-|
| Jan/2024 | 100% | 90% | 85% |

Significa que:

- 100% dos clientes adquiridos em janeiro começaram ativos.
- Após um mês, 90% continuavam ativos.
- Após dois meses, 85% continuavam ativos.

Coortes mais recentes possuem menos colunas porque ainda não existe histórico suficiente.

---

# Estágios da Startup

O sistema acompanha a evolução da empresa usando estágios comuns do ciclo de startups.

A classificação inicial pode ser alterada conforme a empresa atinge os critérios necessários.

---

## Pre-seed

Fase inicial da startup.

Objetivo principal:

- Validar problema e solução.
- Criar primeira versão do produto.
- Encontrar os primeiros clientes.
- Validar se existe demanda real.

Critérios usados pelo sistema para avançar:

- MRR ≥ R$ 20.000
- Retenção ≥ 80%
- Pelo menos 100 clientes ativos
- CAC Payback ≤ 18 meses

---

## Seed

Empresa encontrou sinais de mercado e começa a buscar escala.

Objetivo:

- Melhorar produto.
- Aumentar aquisição de clientes.
- Criar processos comerciais repetíveis.
- Crescer receita.

Critérios:

- MRR ≥ R$ 80.000
- Retenção ≥ 85%
- Pelo menos 300 clientes ativos
- CAC Payback ≤ 15 meses

---

## Series A

Empresa já possui validação de mercado e busca crescimento acelerado.

Objetivo:

- Escalar aquisição.
- Expandir equipe.
- Aumentar participação de mercado.

Critérios:

- MRR ≥ R$ 300.000
- Retenção ≥ 90%
- Pelo menos 800 clientes ativos
- CAC Payback ≤ 12 meses

---

## Series B

Empresa está em fase de expansão.

Objetivo:

- Escalar operações.
- Expandir mercados.
- Aumentar eficiência operacional.

Critérios:

- MRR ≥ R$ 800.000
- Retenção ≥ 92%
- Pelo menos 2.000 clientes ativos
- CAC Payback ≤ 10 meses

---

## Series C+

Empresas maduras em expansão.

Objetivo:

- Liderança de mercado.
- Expansão internacional.
- Consolidação operacional.

Nesta fase o foco passa de validação para crescimento sustentável e eficiência.

---

O Stage Advisor acompanha automaticamente o progresso da empresa e mostra quais requisitos ainda faltam para alcançar o próximo estágio.