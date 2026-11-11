# Atividade 3 — Virtualização, Contêineres, Namespaces e Cgroups
**Sistemas Operacionais — UFS 2026.2**

Repositório da equipe para a Atividade 3.

## Estrutura do repositório

- `scripts/`: Scripts executáveis de automação e reprodução do laboratório.
  - `evidencia_ns_mount.sh`: Coleta compartilhada das evidências da Parte B (Namespaces) e Parte D (Mount e menor privilégio).
- `evidencias/`: Registros brutos das execuções e coletas.
  - `parte_a_ambiente_enzo.md`: Evidências dos comandos e identificação do ambiente da Parte A.
  - `evidencia_ns_mount_20261109_203438.log`: Log bruto da execução de namespaces e verificação de mount read-only.
  - `parte_b_namespaces_bruto.md`: Registro detalhado e tabela comparativa dos namespaces (Parte B).
- `relatorio/`: Seções e textos para compilação do relatório final em PDF.
  - `parte_a_ambiente_enzo.md`: Seção da Parte A, diagrama de camadas e resposta à Questão 1.
  - `parte_b_relatorio_fagner.md`: Seção completa da Parte B e respostas às Questões 2 e 3 (Fagner Junqueira).
- `apresentacao/`: Slides, roteiros de fala e materiais para apresentação e vídeo.
  - `slide_enzo_parte_a.md`: Conteúdo visual e notas de fala da Parte A.
  - `slide_fagner_parte_b.md`: Conteúdo e layout do slide da Parte B.
  - `roteiro_fala_fagner.md`: Roteiro de fala cronometrado (60–90 segundos).
- `contribuicoes_ia.md`: Tabela de contribuições individuais e declaração crítica de uso de IA generativa.

## Equipe e contribuições

| Integrante | Participação |
| --- | --- |
| Enzo Emanuel Maia Costa | Parte A: inventário do ambiente e diagrama de camadas |
| José Fagner Silva Junqueira | Parte B: namespaces, evidências e roteiro |
| Filipe de Carvalho Godoy | Parte C: verificação dos limites e análise dos contadores |
| Rauany Ingrid Santos de Jesus | Parte C: análise comparativa de resultados |
| Vênisson Cardoso dos Santos | Parte C, em coautoria com Katyane: execução local, coleta e organização dos resultados |
| Katyane dos Santos | Coautoria da Parte C com Vênisson e preparação documental; integração de PDF e vídeo prevista |
| Giulian Fábio Bastos Amorim Lima | Parte D: montagem somente leitura e menor privilégio |

Os registros individuais e o uso crítico de IA estão em [contribuicoes_ia.md](contribuicoes_ia.md).

## Parte C — Vênisson e Katyane

Os arquivos desta parte estão na [branch `feature/parte-c-venisson`](https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane/blob/feature/parte-c-venisson), ainda separados da `main`. Esta atualização modifica somente o README e a declaração de contribuições.

- [Relatório e metodologia](https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane/blob/feature/parte-c-venisson/relatorio/parte_c_experimentos_venisson.md).
- [Dados brutos, inventário, CSV e gráficos](https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane/tree/feature/parte-c-venisson/evidencias/parte_c_venisson/).
- [Carga, coletor e executor](https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane/tree/feature/parte-c-venisson/scripts/parte_c_venisson/).

Lote WSL2 vigente: `20261110T144547Z_2382`. São três repetições por condição, com 20.000.000 de iterações e checksum 4.864.000 em cada execução. Os seis registros terminaram com sucesso.

| Condição | Quota | Wall mediano (s) | Amplitude do wall (s) | Vazão mediana (iterações/s) |
| --- | --- | --- | --- | --- |
| C1 | 0,5 CPU | 3,820625 | 0,083601 | 5.234.746 |
| C2 | 1 CPU | 2,136695 | 0,084754 | 9.360.250 |

A razão das vazões medianas é 1,788 neste lote. A carga é sintética, sem execução de modelo de linguagem ou GPU.

### Ambientes e limites de interpretação

O lote acima foi executado no Docker Desktop/WSL2 de Vênisson, com inventário próprio na branch da Parte C. O ambiente de Enzo na Parte A e o de Fagner na Parte B pertencem a outros computadores.

Os resultados VirtualBox anteriores permanecem no [histórico original](https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane/tree/8f47ee56cc49394418865cb2ffb286e807c6415c/evidencias/parte_c_venisson). Não entram nas estatísticas WSL2. O relatório de Filipe e sua tabela na `main` descrevem o lote anterior e devem ser lidos com essa identificação.

O coletor compartilha a quota da carga e o host manteve serviços concorrentes. Há apenas três repetições por condição. RSS do processo, `memory.current` e `memory.peak` têm escopos diferentes. A razão duração de monitoramento/amostras é aproximada e não mede intervalos individuais nem prova a causa de atrasos.

### Reprodução da Parte C

Em um checkout da branch da Parte C, com Docker Linux e cgroups v2:

```bash
bash scripts/parte_c_venisson/run_experimentos.sh
```

O executor fixa a imagem por digest, alterna C1/C2 e cria um diretório de lote próprio. Preservar stdout, stderr e tentativas com problemas. Os contêineres da Parte C usam `--rm`; evitar limpeza global do Docker.

## Materiais finais

O PDF consolidado e a URL final do vídeo não foram localizados no conjunto auditado. Os slides recebidos ainda contêm valores do lote anterior e precisam de revisão antes de representar os resultados WSL2.
