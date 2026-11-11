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
| Katyane dos Santos | Coautoria da Parte C com Vênisson e consolidação editorial do PDF, checklist e links de apresentação/vídeo |
| Giulian Fábio Bastos Amorim Lima | Parte D: montagem somente leitura e menor privilégio |

Os registros individuais e o uso crítico de IA estão em [contribuicoes_ia.md](contribuicoes_ia.md).

## Parte C — Vênisson e Katyane

Os scripts, registros, CSV, gráficos e relatório da Parte C estão integrados à `main`. As estatísticas abaixo usam somente o lote WSL2 vigente; o lote VirtualBox permanece identificado no histórico.

- [Relatório e metodologia](relatorio/parte_c_experimentos_venisson.md).
- [Dados brutos, inventário, CSV e gráficos](evidencias/parte_c_venisson/).
- [Carga, coletor e executor](scripts/parte_c_venisson/).

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

## Preparação e versões de referência

Executar os comandos em Bash no Linux ou Ubuntu/WSL2, com Git, Python 3, Docker com daemon Linux e cgroups v2. No Windows, iniciar o Docker Desktop e habilitar a integração com a distribuição WSL2. Não executar o roteiro Bash diretamente no PowerShell.

| Material | Referência imutável |
| --- | --- |
| Base documental da main antes desta complementação | `bd88856487b7f1ff8af2a8ffdf1c4d4e3fd8be46` |
| Código e evidências WSL2 da Parte C | `98b62a0f8433a018d918c502a6e12fe7bac80b7b` |
| Histórico VirtualBox, separado do WSL2 | `8f47ee56cc49394418865cb2ffb286e807c6415c` |

A consolidação original de Katyane está no commit `b0f9728`, preservado no histórico da integração. O commit final da entrega corresponde ao commit de integração visível no histórico da `main`. Para registrar o SHA exato de qualquer checkout, usar `git rev-parse HEAD`. As referências imutáveis acima permitem reproduzir os códigos e dados originais.

```bash
git clone https://github.com/fagnerjunqueira/SO_2026_2_AV3_Costa_Enzo_Jesus_Rauany__Godoy_Felipe_Lima_Giulian_Junqueira_Jos-_Santos_Katyane.git gemma-av3
cd gemma-av3
git fetch origin
# Checkout separado e imutável para reproduzir a Parte C.
git worktree add --detach ../gemma-av3-parte-c 98b62a0f8433a018d918c502a6e12fe7bac80b7b
cd ../gemma-av3-parte-c
git rev-parse HEAD
uname -a
cat /etc/os-release
nproc
free -h
docker version
docker compose version
docker info --format 'Cgroup={{.CgroupVersion}} Driver={{.CgroupDriver}} CPUs={{.NCPU}} MemoriaBytes={{.MemTotal}}'
```

Registrar separadamente o sistema hospedeiro e o ambiente real do daemon. Em Docker Desktop, o kernel usado pelos contêineres pertence ao backend Linux, não ao Windows. Limitações de controladores e de inspeção dos limites ancestrais devem acompanhar a análise.

### Origem e digest da imagem

Origem: imagem oficial Python no Docker Hub (`docker.io/library/python`). O executor da Parte C usa exatamente:

```bash
export IMAGEM_LAB='python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b'
docker pull "$IMAGEM_LAB"
docker image inspect --format '{{json .RepoDigests}} {{.Os}}/{{.Architecture}}' "$IMAGEM_LAB"
```

O lote publicado usa linux/amd64. Não substituir pelo conteúdo atual de uma tag mutável para reproduzir esse lote. O pull requer internet inicialmente; a Parte C executa com `--network none`. Revisar dados pessoais e caminhos antes de publicar saídas completas de inspect/info.

## Reprodução e coleta da Parte C

A partir de `gemma-av3-parte-c`, criado acima:

```bash
bash scripts/parte_c_venisson/run_experimentos.sh
```

O script fixa 20.000.000 de iterações internamente, alterna C1_R1, C2_R1, C1_R2, C2_R2, C1_R3, C2_R3 e não lê `ITERACOES` do ambiente. C1 usa 0,5 CPU e C2 usa 1 CPU. Ambas usam 256 MiB, RAM+swap total de 256 MiB e 64 tarefas. Os timeouts são 60 s no coletor e 90 s no host quando GNU timeout está disponível.

Cada execução cria `scripts/parte_c_venisson/resultados/<LOTE>/`, sem sobrescrever os registros publicados. A pasta contém seis JSON, seis arquivos stderr, `manifesto.csv` com ordem/códigos de saída, `imagem.txt` e `iteracoes.txt`. Preservar inclusive tentativas com falha; não trocar o lote de origem silenciosamente.

Para conferir as evidências já publicadas e gerar outro CSV sem executar Docker:

```bash
python3 scripts/verifica_limites.py   evidencias/parte_c_venisson/resultados/20261110T144547Z_2382   --csv /tmp/gemma-av3-limites.csv
sha256sum -c evidencias/parte_c_venisson/SHA256SUMS.txt
```

Para conferir um lote novo, substituir o diretório de entrada pelo caminho informado ao final do executor. O verificador imprime limites, CPU, memória e validação funcional; o resumo de medianas publicado está em `evidencias/parte_c_venisson/resumo_mediana.csv`.

Cada JSON registra limites, contadores antes/depois, deltas, RSS, memória do grupo, wall/CPU da carga, checksum, status e timeout. Calcular vazão como iterações/wall e comparar mediana e amplitude das três repetições de cada condição. Os campos históricos de intervalo/atraso do verificador representam razão monitoramento/amostras e classificação heurística, sem timestamps individuais ou prova causal.

## Coleta de namespaces e montagem somente leitura

O script `scripts/evidencia_ns_mount.sh` está na main e também na referência da Parte C. Ele consulta a imagem local pela tag `python:3.12-slim`. Em uma repetição, apontar essa tag local para o digest escolhido e registrar o digest efetivamente impresso no log:

```bash
docker tag "$IMAGEM_LAB" python:3.12-slim
# O script remove dados_demo e contêineres com estes nomes.
# Executar apenas em checkout de laboratório, sem dados próprios nesse diretório.
test ! -e dados_demo
docker ps -a --filter name=so_av3_fagner_cnt
# Prosseguir somente se não houver contêineres preexistentes com os nomes do teste.
bash scripts/evidencia_ns_mount.sh
```

O log novo fica em `evidencias/evidencia_ns_mount_<DATA_HORA>.log`. Conferir PID do host do daemon, PID 1 interno, handles pid/mnt/net, leitura e negação de escrita. O script identifica Fagner no cabeçalho por texto fixo: registrar o operador real de uma repetição, sem atribuir a coleta nova ao autor original. Essa repetição pode alterar a tag local, mas não muda o digest fixo do executor da Parte C.

## Limpeza do laboratório

A Parte C usa `docker run --rm`. O script de namespaces possui limpeza por trap para os contêineres `so_av3_fagner_cntA` e `so_av3_fagner_cntB` e o diretório sintético `dados_demo` no diretório corrente. Por isso, verificar previamente que esses nomes não pertencem a outros trabalhos.

Preservar JSON, stderr, manifestos, CSV e logs após a limpeza. Se uma interrupção deixar recursos ativos, identificar os contêineres desta execução com `docker ps -a` e remover apenas seus IDs confirmados, usando `docker rm -f ID_DO_CONTAINER_DO_TESTE`. Não executar `docker system prune`, apagar volumes ou encerrar serviços dos demais projetos. A imagem pode permanecer em cache.

## Materiais finais

- [Vídeo da equipe — AT3](https://drive.google.com/file/d/1OREg4M7iMNTn85Jl9wyk5ezy-Nb6A88Z/view?usp=drive_link).
- [Relatório técnico — Google Docs](https://docs.google.com/document/d/1MaZRUQI5yHYMexa8F3mkOm6dmpE4qBVHiCkkYb2SuyQ/edit?tab=t.0).

O documento Google Docs é uma versão editável da equipe. O [relatório final consolidado em PDF](relatorio/relatorio_final_consolidado.pdf) e sua [fonte Markdown](relatorio/relatorio_final_consolidado.md) estão disponíveis na main. Os links de apresentação e vídeo também constam em [VIDEO.md](VIDEO.md). A confirmação do arquivo de vídeo não substitui a conferência da participação de todos os integrantes. O PPTX atualizado recebido pela equipe ainda requer conferência de consistência com o lote WSL2 vigente.

## Conferência final da integração

O [checklist](CHECKLIST_ENTREGA.md) distingue evidências presentes de validações humanas pendentes. O PDF de consolidação preserva as oito páginas da edição de Katyane e acrescenta uma página de complemento com vídeo, vazão/amplitude e limites de interpretação. Consulte também a atualização de limites em `relatorio/parte_c_limites_atualizacao_20261110.md`: o relatório original de Filipe descreve o lote anterior, sem substituir as estatísticas WSL2. Os gráficos desta comparação estão em `evidencias/parte_c_venisson/graficos/`.

O manifesto original da Parte C foi preservado. Na cópia da consolidação, sete arquivos sofreram apenas normalização CRLF/LF; `SHA256SUMS_INTEGRACAO.txt` verifica os bytes integrados. Os seis JSON de execução são idênticos aos originais.

Para validar os arquivos da main integrada, executar na raiz do checkout da main: `sha256sum -c SHA256SUMS_INTEGRACAO.txt`. O checkout imutável da Parte C usa o manifesto original, conforme o comando de reprodução acima.
