# Atividade 3 — Virtualização, Contêineres, Namespaces e Cgroups
**Sistemas Operacionais — UFS 2026.2**

Repositório da equipe para a Atividade 3.

## Estrutura da Pasta `atividade3/`

- `scripts/`: Scripts executáveis de automação e reprodução do laboratório.
  - `evidencia_ns_mount.sh`: Coleta compartilhada das evidências da Parte B (Namespaces) e Parte D (Mount e menor privilégio).
- `evidencias/`: Registros brutos das execuções e coletas.
  - `evidencia_ns_mount_20261109_203438.log`: Log bruto da execução de namespaces e verificação de mount read-only.
  - `parte_b_namespaces_bruto.md`: Registro detalhado e tabela comparativa dos namespaces (Parte B).
- `relatorio/`: Seções e textos para compilação do relatório final em PDF.
  - `parte_b_relatorio_fagner.md`: Seção completa da Parte B e respostas às Questões 2 e 3 (Fagner Junqueira).
- `apresentacao/`: Slides, roteiros de fala e materiais para apresentação e vídeo.
  - `slide_fagner_parte_b.md`: Conteúdo e layout do slide da Parte B.
  - `roteiro_fala_fagner.md`: Roteiro de fala cronometrado (60–90 segundos).
- `contribuicoes_ia.md`: Tabela de contribuições individuais e declaração crítica de uso de IA generativa.


## Parte C — lote vigente (10/11/2026)

O lote `20261110T144547Z_2382` substitui o lote VirtualBox e o primeiro teste WSL2 na análise principal. Adota a mesma imagem por digest da Parte B de Fagner, com Docker Desktop/WSL2 e cgroups v2/cgroupfs. A padronização é parcial: versões do kernel/Engine, distribuição, CPUs e hardware diferem da referência; isso está documentado nos relatórios. O ambiente do Enzo não foi publicado e não é presumido como idêntico.

- Execução: `scripts/parte_c_venisson/run_experimentos.sh` (sem sudo, digest fixado).
- Brutos: `evidencias/parte_c_venisson/resultados/20261110T144547Z_2382/`.
- Consolidação e validação: `evidencias/parte_c_venisson/` (inclui `resultados_consolidados.csv`, `resumo_mediana.csv` e `validacao_execucoes.csv`).
- Relatório atualizado: `relatorio/parte_c_experimentos_venisson.md`.
- Relatório compartilhado: https://docs.google.com/document/d/1MaZRUQI5yHYMexa8F3mkOm6dmpE4qBVHiCkkYb2SuyQ/edit?tab=t.0 . O documento compartilhado foi preservado; a análise do novo lote está no relatório de Vênisson nesta branch.

Os resultados anteriores foram retirados dos arquivos vigentes; continuam auditáveis no commit `8f47ee56cc49394418865cb2ffb286e807c6415c` e em cópias locais arquivadas. Não houve reescrita do histórico do Git.

Esta atualização publica somente a parte de Vênisson. O relatório de Filipe e `evidencias/limites_cgroup.csv` permanecem como estavam e descrevem o lote anterior; a adaptação desses materiais ao novo lote fica a cargo do responsável.
