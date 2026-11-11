# Atualização da Parte C — Confirmação dos limites e métricas de cgroup

**Referência:** relatório original de Filipe de Carvalho Godoy  
**Consolidação:** Katyane dos Santos  
**Lote experimental:** `20261110T144547Z_2382`  
**Responsável pela reexecução:** Vênisson Cardoso dos Santos

## 1. Objetivo

Atualizar a análise dos limites de cgroups com base nas seis execuções realizadas em 10/11/2026, preservando o relatório original e evitando a utilização conjunta de resultados de lotes diferentes.

## 2. Confirmação dos limites

Os valores foram obtidos diretamente dos arquivos de controle do kernel Linux, registrados nos JSONs experimentais.

| Condição | cpu.max | Quota | memory.max | pids.max |
|---|---|---|---|---|
| C1 | 50000 100000 | 0,5 CPU | 256 MiB | 64 |
| C2 | 100000 100000 | 1 CPU | 256 MiB | 64 |

As seis execuções apresentaram valores compatíveis com os limites solicitados.

## 3. Resultados de CPU e throttling

| Execução | CPU do cgroup (s) | Períodos | Períodos throttled | Throttling (%) |
|---|---:|---:|---:|---:|
| C1_R1 | 2,168 | 44 | 44 | 100% |
| C1_R2 | 1,990 | 40 | 40 | 100% |
| C1_R3 | 2,001 | 40 | 40 | 100% |
| C2_R1 | 2,125 | 24 | 0 | 0% |
| C2_R2 | 2,115 | 23 | 0 | 0% |
| C2_R3 | 2,084 | 23 | 0 | 0% |

A condição C1 apresentou throttling em todos os períodos contabilizados, enquanto C2 não apresentou throttling neste lote.

A mediana do consumo de CPU do cgroup foi de 2,001 s em C1 e 2,115 s em C2. A mediana do tempo da carga foi de 3,821 s em C1 e 2,137 s em C2.

Esses resultados indicam que a maior quota de CPU esteve associada à redução do tempo de execução da carga, mantendo-se a quantidade de trabalho constante.

## 4. Memória

O limite configurado foi de 256 MiB em todas as execuções.

O maior valor registrado em `memory.peak` foi de 25,38 MiB, aproximadamente 9,9% do limite.

As métricas RSS, `memory.current` e `memory.peak` possuem escopos diferentes e não devem ser tratadas como equivalentes.

Os resultados confirmam a configuração do limite, mas não demonstram comportamento sob pressão de memória.

## 5. Resposta à Questão 4

A quota de CPU foi confirmada por meio da leitura do arquivo `cpu.max`, e não apenas pelas flags utilizadas no Docker.

Na condição C1, o valor `50000 100000` corresponde a uma quota de 0,5 CPU. Na condição C2, `100000 100000` corresponde a 1 CPU.

O kernel registrou throttling em 100% dos períodos contabilizados nas três execuções de C1 e em nenhum período nas três execuções de C2.

As seis execuções realizaram 20 milhões de iterações, produziram o mesmo checksum e terminaram com código de saída zero.

O tempo da carga foi menor em C2, mas os contadores de CPU incluem o consumo conjunto da aplicação e do coletor. Além disso, os resultados representam apenas três repetições por condição, em um ambiente com outras cargas ativas.

Portanto, os resultados sustentam a confirmação dos limites e a ocorrência de throttling em C1, sem permitir generalizações sobre outros ambientes ou cargas de trabalho.

## 6. Rastreabilidade

Os dados utilizados nesta atualização pertencem exclusivamente ao lote `20261110T144547Z_2382`.

Fontes no repositório:

- `relatorio/parte_c_experimentos_venisson.md`
- `evidencias/parte_c_venisson/resultados_consolidados.csv`
- `evidencias/parte_c_venisson/resumo_mediana.csv`
- `evidencias/parte_c_venisson/validacao_execucoes.csv`
- `evidencias/parte_c_venisson/SHA256SUMS.txt`

Os resultados do lote anterior permanecem documentados no relatório original de Filipe, mas não são utilizados nas conclusões desta atualização.

**Nota de autoria:** esta seção é uma consolidação editorial dos resultados atualizados e não representa uma nova execução experimental por Katyane.