# Contribuições Individuais e Declaração de Uso de IA Generativa
**Atividade 3 — Sistemas Operacionais (2026.2) | UFS**

Este documento centraliza as contribuições de cada membro da equipe e o registro crítico de uso de ferramentas de IA generativa, conforme exigido pelas Seções 10 e 12 do enunciado da atividade.

---

## 1. Tabela de Contribuições Individuais

| Integrante | Responsabilidade Principal | Contribuição Efetiva Entregue | Arquivos / Evidências Associadas |
| :--- | :--- | :--- | :--- |
| **Enzo Costa** | Parte A — Ambiente e Diagrama | Documentação do ambiente Linux/daemon, cgroups v2, digest da imagem e diagrama de camadas. | `atividade3/ambiente/` |
| **Fagner Junqueira** | **Parte B — Evidências de Namespaces (Questões 2 e 3)** | Criação e execução compartilhada do script `evidencia_ns_mount.sh`, coleta empírica de handles `/proc/1/ns/*` e PIDs, tabela comparativa, seção do relatório com respostas às questões 2 e 3, slide e roteiro de apresentação. | `atividade3/scripts/evidencia_ns_mount.sh`, `atividade3/evidencias/evidencia_ns_mount_20261109_203438.log`, `atividade3/evidencias/parte_b_namespaces_bruto.md`, `atividade3/relatorio/parte_b_relatorio_fagner.md`, `atividade3/apresentacao/slide_fagner_parte_b.md`, `atividade3/apresentacao/roteiro_fala_fagner.md` |
| **Rauany Jesus** | Parte C — Experimento de cgroups | Planejamento, repetições de carga CPU determinística e métricas. | `atividade3/experimentos/` |
| **Filipe de Carvalho Godoy** | **Parte C — Confirmação dos limites e métricas de cgroup (Questão 4)** | Verificação de que `cpu.max`, `memory.max` e `pids.max` foram aplicados pelo kernel nas seis execuções, por leitura do cgroup e não pela flag; consolidação dos deltas de `cpu.stat` e das três métricas de memória (RSS, `memory.current`, `memory.peak`); identificação e documentação da contaminação do coletor; seção do relatório com resposta à questão 4. | `scripts/verifica_limites.py`, `evidencias/limites_cgroup.csv`, `relatorio/parte_c_limites_filipe.md` |
| **Giulian Lima** | Parte D — Mount e menor privilégio | Coleta compartilhada com Fagner (Parte D em `evidencia_ns_mount.sh`), testes de leitura e negação de escrita em volume `:ro`. | `atividade3/evidencias/evidencia_ns_mount_20261109_203438.log` |
| **Katyane Santos** | Integração, Relatório PDF e Vídeo | Montagem final do relatório PDF, revisão editorial da equipe e consolidação das mídias. | `atividade3/relatorio_final.pdf`, `VIDEO.md` |

---

## 2. Declaração Crítica de Uso de IA Generativa

### Linha de Declaração de Fagner Junqueira

- **Ferramenta e Modelo:** Antigravity AI Assistant (Google DeepMind), motor Gemini 3.8 Flash (Low).
- **Finalidade:** Estruturação da seção da Parte B do relatório técnico, automação do script de coleta concorrente compartilhada com a Parte D (`evidencia_ns_mount.sh`), elaboração da tabela de namespaces e síntese do roteiro de fala para a apresentação em vídeo.

#### Prompts Relevantes Utilizados:
1. *"Localize o kit oficial ou elabore um script reproduzível que instancie dois contêineres independentes com a imagem python:3.12-slim fixada por digest, colete PID do host, comm do PID 1 e os links simbólicos de /proc/1/ns/pid, /proc/1/ns/mnt e /proc/1/ns/net, além do teste de leitura e negação de escrita em /dados:ro da Parte D."*
2. *"Monte uma tabela comparativa com recurso, handle em A, handle em B, relação e interpretação, e redija uma explicação técnica baseada em namespaces(7) sobre como dois contêineres podem ter PID 1 internamente e PIDs distintos no host do daemon."*
3. *"Responda às questões 2 e 3 do enunciado da Atividade 3, diferenciando namespace, cgroup, identidade e política de acesso, e definindo explicitamente o que as evidências observadas provam e quais conclusões demandam testes próprios."*

#### Registro Crítico: Sugestões Adotadas, Corrigidas ou Rejeitadas

- **Adotado:**
  - A estrutura da tabela comparativa contendo as colunas exigidas pelo enunciado e a explicação conceitual sobre o aninhamento e hierarquização de PID namespaces no kernel Linux.
  - O formato do roteiro de fala cronometrado com marcações de slides e conexão direta ao arquivo bruto de log.
- **Corrigido:**
  - A IA inicialmente sugeriu inspecionar `/proc/$PID_host/ns` diretamente a partir do terminal bash do WSL2 da máquina local. Como o Docker Desktop no Windows/WSL2 executa os contêineres dentro de sua própria máquina virtual de infraestrutura (`docker-desktop`), os PIDs retornados por `docker inspect` (PIDs 6633 e 6679) pertencem ao kernel daquela VM interna e não existem no `/proc` da distribuição Ubuntu do WSL2. A abordagem foi corrigida para coletar os inodos a partir do próprio contêiner (`docker exec NOME readlink /proc/1/ns/*`), em estrita conformidade com as instruções do enunciado da Parte B e documentação de suporte.
- **Rejeitado:**
  - A inclusão de dados genéricos/fictícios de namespaces ou saídas de exemplo. Apenas a saída real obtida da execução local via Docker Engine foi adotada e documentada nos arquivos de evidência.

#### Verificação por Documentação / Teste:
- Verificado contra a documentação do kernel Linux `namespaces(7)` ([NS](https://man7.org/linux/man-pages/man7/namespaces.7.html)) e testado via terminal local e logs reais gerados pelo script `atividade3/scripts/evidencia_ns_mount.sh`.

#### Pontos Dependentes da Minha Revisão (Fagner) ou do Grupo:
- [ ] Revisar se os IDs e caminhos descritos no relatório combinam perfeitamente com a descrição do hardware/host no diagrama da Parte A que o Enzo está desenhando.
- [ ] Confirmar com o Giulian a absorção da saída da Parte D já presente em `evidencia_ns_mount_20261109_203438.log`.
- [ ] Gravação pessoal do áudio/vídeo da Parte B seguindo o roteiro de fala e disponibilização do trecho para Katyane consolidar no vídeo final.

### Linha de Declaração de Filipe de Carvalho Godoy

- **Ferramenta e Modelo:** Claude (Anthropic), modelo Claude Opus 5.
- **Finalidade:** Análise dos registros brutos das seis execuções da Parte C, construção do script de verificação dos limites e redação da seção do relatório.

#### Prompts Relevantes Utilizados:
1. *"Os tempos de C1 e C2 ficaram praticamente iguais, e C2 (1,0 CPU) também apresenta throttling apesar de a carga ser single-thread. Isso é esperado?"*
2. *"Monte um script que leia os JSONs e confirme cpu.max, memory.max e pids.max, separando RSS, memory.current e memory.peak como métricas distintas, conforme o enunciado exige."*

#### Registro Crítico: Sugestões Adotadas, Corrigidas ou Rejeitadas

- **Adotado:** a distinção entre a flag `--cpus` (solicitação ao runtime) e a leitura de `/sys/fs/cgroup/cpu.max` de dentro do contêiner (estado aplicado pelo kernel), que é o centro da questão 4; e a separação das três métricas de memória em colunas independentes.
- **Corrigido:** a primeira leitura tratava o throttling de C2 como ruído. Ao cruzar os contadores do kernel com o número de amostras de RSS, verificou-se causa sistemática — o coletor roda no mesmo cgroup da carga e é throttled junto. A evidência é C2_R1: única com throttling moderado (52%) e única em que o intervalo de amostragem correspondeu aos 50 ms programados. Nas outras cinco, o intervalo cresceu de 16 a 47 vezes.
- **Rejeitado:** atribuir a discrepância entre `wall_time` e `cpu_time` a uma causa única. Com seis amostras e os *soft lockups* registrados na VM, não há base para isso; a divergência foi registrada como anomalia não resolvida. Também foi rejeitada a sugestão de reexecutar o experimento para melhorar os números, já que o enunciado determina preservar tentativas com problemas.

#### Verificação por Documentação / Teste:
- Semântica de `cpu.max` e `cpu.stat` conferida contra a documentação do kernel ([CG](https://docs.kernel.org/admin-guide/cgroup-v2.html)) e [RES](https://docs.docker.com/engine/containers/resource_constraints/).
- O script recalcula todas as tabelas da seção a partir dos JSONs originais, de modo que nenhum valor apresentado depende de texto gerado.

#### Pontos Dependentes da Minha Revisão (Filipe) ou do Grupo:
- [ ] Os JSONs das seis execuções precisam estar no repositório para o comando de reprodução funcionar. Caminho assumido: `evidencias/cgroups_lote1/`.
- [ ] A limitação da seção 5.6 é insumo para a questão 5 (ameaça à validade), da Rauany.

## Atualização da parte de Vênisson — 10/11/2026

Por solicitação de Vênisson, o relatório de Fagner foi usado como referência, sem presumir a configuração não publicada de Enzo. A assistência de IA preparou cópias do executor com a imagem `python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`, executou seis repetições alternadas no WSL2, validou JSON/checksum/limites e gerou CSV, gráficos e o relatório de Vênisson. A carga e o coletor permaneceram idênticos byte a byte.

Lote publicado: `20261110T144547Z_2382`. Mesma imagem e plataforma não significam hosts idênticos: versões, CPUs e serviços concorrentes estão documentados. Monitoramento/amostras é tratado como densidade aproximada, sem atribuir causalmente atrasos a um único mecanismo. Os arquivos de evidência antigos da pasta de Vênisson foram substituídos pelos novos, preservando o histórico do Git.

Esta publicação altera somente a parte de Vênisson e suas evidências. As seções anteriores dos colegas, o relatório de Filipe, sua tabela `evidencias/limites_cgroup.csv` e o Google Docs não são atualizados por este commit. Os dados antigos mencionados na análise do Filipe precisam de revisão pelo responsável antes de serem relacionados ao novo lote.
