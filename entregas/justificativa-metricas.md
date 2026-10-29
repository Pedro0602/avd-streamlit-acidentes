# Justificativa das métricas — Dashboard 2

**Tema:** Acidentes em rodovias federais brasileiras (2007–2020).  
**Público-alvo geral:** gestores de segurança viária, analistas de dados e equipes de planejamento.  
**Cuidados:** todos os indicadores respeitam os filtros; a base descreve acidentes registrados e não fornece volume de tráfego ou distância percorrida. Portanto, contagens não são medidas de risco.

## 1. Acidentes registrados
- **Variável:** quantidade de linhas do dataset após filtros.
- **O que mede:** volume de ocorrências registradas no recorte.
- **Por que escolhida:** contextualiza todas as demais métricas.
- **Público-alvo:** gestores e analistas de segurança viária.
- **Decisão apoiada:** priorizar onde aprofundar a investigação de volume de ocorrências.
- **O que comunica:** número absoluto de registros; não mede probabilidade de acidente.

## 2. Pessoas envolvidas
- **Variável:** `pessoas` (soma).
- **O que mede:** total de pessoas envolvidas nos registros analisados.
- **Por que escolhida:** dimensiona a população diretamente envolvida nos eventos.
- **Público-alvo:** planejamento operacional e saúde pública.
- **Decisão apoiada:** discutir demanda potencial de atendimento e resposta.
- **O que comunica:** quantidade registrada, não número de indivíduos únicos.

## 3. Óbitos registrados
- **Variável:** `mortos` (soma).
- **O que mede:** quantidade total de vítimas fatais registradas.
- **Por que escolhida:** mostra gravidade dos acidentes além de sua frequência.
- **Público-alvo:** gestores e órgãos de segurança viária.
- **Decisão apoiada:** direcionar estudos sobre gravidade e prevenção.
- **O que comunica:** total de óbitos dos registros filtrados.

## 4. Feridos registrados
- **Variável:** `feridos` (soma).
- **O que mede:** número total registrado de pessoas feridas.
- **Por que escolhida:** complementa óbitos com consequência não fatal.
- **Público-alvo:** saúde pública, planejamento e segurança viária.
- **Decisão apoiada:** avaliar demanda de atendimento e fatores associados.
- **O que comunica:** total de feridos declarados na base selecionada.

## 5. Proporção de acidentes com óbito
- **Variáveis:** `mortos` e quantidade de acidentes.
- **O que mede:** registros com `mortos > 0` divididos pelo total de registros no recorte.
- **Por que escolhida:** compara a gravidade relativa entre recortes, sem confundir número de mortes com número de acidentes fatais.
- **Público-alvo:** analistas e gestores.
- **Decisão apoiada:** identificar recortes que merecem investigação sobre severidade.
- **O que comunica:** percentual *entre os acidentes registrados*, não o risco de morrer ao viajar.

## Visuais do Dashboard 2 (além das métricas)

Feitos em Altair com **seleção cruzada**: clicar numa UF filtra os outros três gráficos e os 5 KPIs acima deles (Shift + clique seleciona várias; clique duplo limpa). Todos também respeitam os filtros da sidebar (período, UF, classificação e intervalo).

| Visual | Pergunta que responde | Decisão apoiada |
|---|---|---|
| Acidentes por UF (barras horizontais) | Onde se concentram os registros? | Escolher estados para aprofundar a análise |
| Evolução anual dos acidentes (linha) | O volume subiu ou caiu entre 2007 e 2020? | Avaliar tendência e mudanças de registro ao longo do tempo |
| Acidentes por classificação (barras) | Qual a proporção entre sem vítimas, feridos e fatais? | Dimensionar a gravidade do recorte escolhido |
| % de acidentes com óbito por fase do dia (barras) | Acidentes à noite são proporcionalmente mais graves? | Priorizar ações de visibilidade/fiscalização noturna |

**Observação sobre o período:** a queda a partir de 2015 pode refletir mudança na forma de registro da PRF, não apenas redução real de acidentes — por isso o gráfico deve ser lido junto com a EDA.
