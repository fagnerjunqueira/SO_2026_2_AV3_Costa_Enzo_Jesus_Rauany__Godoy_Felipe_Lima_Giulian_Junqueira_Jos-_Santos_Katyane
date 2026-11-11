# Atividade 3 — Virtualização, Contêineres, Namespaces e Cgroups
**Sistemas Operacionais — UFS 2026.2**

Repositório da equipe para a Atividade 3.

## Estrutura do Repositório

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


## Preparação do ambiente

Os experimentos da Atividade 3 utilizam Linux, Docker e Python 3 para investigar virtualização, namespaces, cgroups e restrições de acesso.

### Pré-requisitos

- Ambiente Linux com Docker Engine disponível.
- Python 3 para execução dos scripts experimentais.
- Permissão para executar comandos Docker.
- Imagem Docker utilizada no laboratório, identificada por digest.

### Verificação do ambiente

Execute os seguintes comandos no ambiente utilizado para os experimentos:

```bash
uname -a
cat /etc/os-release
nproc
docker version
docker info --format 'Cgroup={{.CgroupVersion}} Driver={{.CgroupDriver}}'
```

A distribuição Linux, o kernel, os recursos disponíveis, a versão do Docker e o ambiente real do daemon devem ser registrados na seção de ambiente do relatório.

### Imagem Docker

O laboratório prevê a imagem `python:3.12-slim`, fixada por digest para garantir a reprodutibilidade.

```bash
docker pull python:3.12-slim
export IMAGEM_LAB="$(docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim)"
printf '%s\n' "$IMAGEM_LAB"
```

O digest efetivamente utilizado deverá ser registrado após a conferência das evidências da equipe.


## Reprodução dos experimentos

Os experimentos devem ser executados no mesmo ambiente Linux/Docker documentado na Parte A, mantendo a imagem e os parâmetros definidos pela equipe.

### Parte B — Namespaces e Parte D — Mount read-only

O repositório contém o script `scripts/evidencia_ns_mount.sh`, utilizado para coletar evidências de isolamento e montagem somente leitura.

No terminal Linux, a partir da raiz do repositório:

```bash
bash scripts/evidencia_ns_mount.sh
```

O script deve ser inspecionado antes da execução. As evidências já registradas pela equipe estão no diretório `evidencias/`.

### Parte C — Cgroups

A comparação experimental utiliza duas condições:

- C1: quota de 0,5 CPU.
- C2: quota de 1,0 CPU.

Ambas devem utilizar os mesmos limites de memória e tarefas, a mesma imagem e a mesma quantidade de trabalho.

São necessárias três repetições por condição, totalizando seis execuções principais. Os resultados devem ser coletados no ambiente definido pela equipe.

O repositório contém `scripts/verifica_limites.py`, relacionado à verificação dos limites de recursos. Os comandos específicos de execução da carga de CPU serão documentados após a integração dos scripts experimentais.

## Coleta e organização das evidências

Os registros experimentais devem ser preservados em `evidencias/`, incluindo:

- Ambiente Linux e Docker utilizado.
- Handles dos namespaces PID, mount e network.
- Demonstração de leitura e negação de escrita no mount read-only.
- Seis registros brutos da comparação C1/C2.
- Limites efetivos de CPU, memória e tarefas.
- Métricas de tempo, consumo de CPU, throttling e memória.
- Tabela consolidada e gráfico comparativo.

As medições devem ser provenientes das execuções reais. Tentativas com erro também devem ser preservadas e identificadas.

Não devem ser utilizados valores gerados por IA como substitutos de resultados experimentais.


## Limpeza do ambiente

Após os experimentos, verificar os contêineres criados:

```bash
docker ps -a
```

Identificar os contêineres utilizados no laboratório e, caso ainda estejam em execução, encerrá-los:

```bash
docker stop NOME_DO_CONTAINER
```

Remover somente os contêineres identificados como pertencentes ao laboratório:

```bash
docker rm NOME_DO_CONTAINER
```

Não remover contêineres, volumes ou imagens de outros projetos.

## Rastreabilidade e entrega

Para permitir a reprodução dos resultados, a entrega deve registrar:

- Ambiente Linux/Docker utilizado pela equipe.
- Imagem Docker e digest efetivamente utilizados.
- Parâmetros e quantidade de trabalho dos experimentos.
- Registros brutos, tabela consolidada e gráfico.
- Commit Git correspondente à versão entregue.
- Relatório final em PDF e apresentação.
- Declaração de uso crítico de IA e contribuições individuais.
- Link do vídeo com participação de todos os integrantes.

### Identificação da versão

- Imagem Docker (digest): pendente de confirmação.
- Commit da entrega: pendente de confirmação.
- Vídeo da equipe: pendente de inclusão.

Os identificadores definitivos serão preenchidos após a conferência dos materiais finais.

