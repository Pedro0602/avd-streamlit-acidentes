# entregas/



## Modelo de `justificativa-metricas.md`

Cada métrica indica **a variável** a que se refere, **o que mede**, **por que foi escolhida** e **o que comunica** a um público que não precisa captar as nuances da variável.

```markdown
# Justificativa das métricas — Dashboard 2

## Métrica 1: <nome>
- **Variável:** 
- **O que mede:** 
- **Por que foi escolhida:** 
- **O que comunica ao público-alvo:** 
```

### Exemplo preenchido

```markdown
## Métrica: Distribuição do colesterol em relação à mediana
- **Variável:** `chol` (colesterol sérico, mg/dl)
- **O que mede:** a proporção de pessoas da amostra abaixo, em torno e acima da mediana de `chol`,
  junto de algumas estatísticas descritivas (média, mediana, mínimo, máximo, desvio padrão).
  "Em torno" = dentro de ±10% da mediana (defina e explicite a faixa que você usar).
- **Por que foi escolhida:** dá uma visão simplificada e direta da variável, sem exigir leitura
  de histograma ou boxplot.
- **O que comunica ao público-alvo:** como está distribuída a amostra de forma resumida
  (ex.: "metade das pessoas está acima de X mg/dl"), para quem não consegue captar as
  nuances da variável.
```
