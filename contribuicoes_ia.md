# Contribuições Individuais e Declaração de Uso de IA Generativa
**Atividade 3 — Sistemas Operacionais (2026.2) | UFS**

Este documento centraliza as contribuições de cada membro da equipe e o registro crítico de uso de ferramentas de IA generativa, conforme exigido pelas Seções 10 e 12 do enunciado da atividade.

---

## 1. Tabela de Contribuições Individuais

| Integrante | Responsabilidade Principal | Contribuição Efetiva Entregue | Arquivos / Evidências Associadas |
| :--- | :--- | :--- | :--- |
| **Enzo Emanuel Maia Costa** | Parte A — Ambiente e Diagrama | Executou independentemente, conforme seu relato, os comandos de ambiente e Docker da Parte A e informou que os resultados coincidiram com a execução de conferência; definiu e revisou o escopo da seção, do diagrama e do slide com assistência de IA; identificou a necessidade de registrar a divergência entre ambientes das partes. | `evidencias/parte_a_ambiente_enzo.md`, `relatorio/parte_a_ambiente_enzo.md`, `apresentacao/slide_enzo_parte_a.md`, Google Docs do relatório da equipe |
| **Fagner Junqueira** | **Parte B — Evidências de Namespaces (Questões 2 e 3)** | Criação e execução compartilhada do script `evidencia_ns_mount.sh`, coleta empírica de handles `/proc/1/ns/*` e PIDs, tabela comparativa, seção do relatório com respostas às questões 2 e 3, slide e roteiro de apresentação. | `scripts/evidencia_ns_mount.sh`, `evidencias/evidencia_ns_mount_20261109_203438.log`, `evidencias/parte_b_namespaces_bruto.md`, `relatorio/parte_b_relatorio_fagner.md`, `apresentacao/slide_fagner_parte_b.md`, `apresentacao/roteiro_fala_fagner.md` |
| **Rauany Jesus** | Parte C — Experimento de cgroups | Planejamento, repetições de carga CPU determinística e métricas. | Análise histórica da Parte C; contribuição ao lote vigente a confirmar pela autora |
| **Filipe de Carvalho Godoy** | **Parte C — Confirmação dos limites e métricas de cgroup (Questão 4)** | Verificação de que `cpu.max`, `memory.max` e `pids.max` foram aplicados pelo kernel nas seis execuções, por leitura do cgroup e não pela flag; consolidação dos deltas de `cpu.stat` e das três métricas de memória (RSS, `memory.current`, `memory.peak`); identificação e documentação da contaminação do coletor; seção do relatório com resposta à questão 4. | `scripts/verifica_limites.py`, `evidencias/limites_cgroup.csv`, `relatorio/parte_c_limites_filipe.md` |
| **Giulian Lima** | Parte D — Mount e menor privilégio | Coleta compartilhada com Fagner (Parte D em `evidencia_ns_mount.sh`), testes de leitura e negação de escrita em volume `:ro`. | `evidencias/evidencia_ns_mount_20261109_203438.log` |
| **Vênisson Cardoso dos Santos** | Parte C — Experimento de cgroups em coautoria com Katyane | Execução local do lote WSL2 `20261110T144547Z_2382`, coleta e disponibilização dos registros, CSV, gráficos e relatório. | `scripts/parte_c_venisson/`, `evidencias/parte_c_venisson/`, `relatorio/parte_c_experimentos_venisson.md` |
| **Katyane dos Santos** | Parte C — Coautoria do experimento; integração documental | Coautoria do experimento com Vênisson, preparação documental e consolidação editorial dos relatórios em Markdown/PDF, com gráficos, checklist e organização dos links da apresentação e do vídeo. | `relatorio/relatorio_final_consolidado.md`, `relatorio/relatorio_final_consolidado.pdf`, `CHECKLIST_ENTREGA.md`, `VIDEO.md` e materiais compartilhados da Parte C |

---

## 2. Declaração Crítica de Uso de IA Generativa

### Linha de Declaração de Enzo Costa

- **Ferramenta e Modelo:** Assistente de IA integrado ao Copilot SDK no VS Code; o modelo não foi informado nesta sessão.
- **Finalidade:** Ajudar a conferir os comandos da Parte A em relação à execução independente relatada por Enzo; redigir e organizar sua seção do relatório, o diagrama de camadas e o slide; e inserir a seção no Google Docs do relatório a pedido de Enzo.

#### Prompts Relevantes Utilizados (até três):
1. *"Rodar os comandos da Parte A: uname -a, os-release, nproc, docker version, docker info (cgroup v1/v2 e driver), pull e digest da imagem (IMAGEM_LAB). Dizer qual é o ambiente real do daemon: nativo, VM, WSL2 ou Docker Desktop. Desenhar o diagrama de camadas (hardware/host, VM se houver, kernel Linux, contêineres). Responder à questão 1: onde está o kernel compartilhado e se há VM intermediária."*
2. *"Veja o que os meninos fizeram até agora e faça minha parte do relatório com base neles."*
3. *"Preencha no Google Docs a seção da Parte A logo abaixo do título e do meu nome."*

#### Registro Crítico: Sugestões Adotadas, Corrigidas ou Rejeitadas

- **Adotado:** o diagrama separa Windows host, backend WSL2/kernel Linux, distribuição Ubuntu usada como shell e daemon Docker Desktop; a resposta distingue o kernel dos contêineres do kernel Windows. Também foi incluída a resposta direta sobre a VM intermediária e os dados de cgroups e digest solicitados.
- **Corrigido:** a primeira tentativa de consultar o Docker ocorreu com o daemon parado. O Docker Desktop foi iniciado; depois, Enzo informa que executou os comandos independentemente e obteve os mesmos resultados da conferência feita pelo assistente.
- **Corrigido:** ao comparar os textos das Partes B, C e D com a coleta da Parte A, foram identificadas diferenças de sistema, versão do Docker, kernel e driver cgroup. A divergência foi registrada como ressalva, em vez de afirmar que todas as medições vieram do mesmo ambiente.
- **Rejeitado:** não foram inventadas medições nem omitida a divergência entre os ambientes. A execução do assistente foi registrada como conferência, não como substituta da execução independente relatada por Enzo.

#### Verificação por Execução
- Enzo relata ter executado independentemente os comandos da Parte A e obtido resultados coincidentes com a conferência do assistente no Windows/WSL2 e no daemon Docker local; o digest também foi confirmado por `docker image inspect`. O assistente auxiliou na redação e organização dos arquivos da Parte A e inseriu o texto no Google Docs da equipe a pedido de Enzo. Enzo deve revisar o texto final e confirmar que a integração está de acordo com o grupo.

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
- Verificado contra a documentação do kernel Linux `namespaces(7)` ([NS](https://man7.org/linux/man-pages/man7/namespaces.7.html)) e testado via terminal local e logs reais gerados pelo script `scripts/evidencia_ns_mount.sh`.

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

### Declaração de Vênisson e Katyane — Parte C e revisão documental

- **Ferramenta:** ChatGPT/Codex. A identificação exata do modelo não foi exposta no ambiente desta revisão.
- **Finalidade:** apoio à preparação da carga/coleta, organização de evidências, cálculos, gráficos, redação técnica e revisão de README/contribuições.
- **Solicitação de revisão:** auditar os resultados, separar VirtualBox de WSL2, reconhecer a coautoria e organizar a documentação no padrão da Atividade 2. O escopo final desta atualização se limita a `README.md` e `contribuicoes_ia.md`.
- **Adotado:** calcular vazão por iterações/wall interno, distinguir CPU do processo e do cgroup e manter a origem de cada lote.
- **Corrigido:** tratar monitoramento/amostras como razão aproximada, sem chamar de intervalo real; distinguir responsabilidade prevista de entrega comprovada de PDF/vídeo.
- **Rejeitado:** preencher medições ausentes, agregar VirtualBox e WSL2 ou atribuir causa única às anomalias do lote antigo.
- **Verificação:** seis JSON WSL2, checksum 4.864.000, limites de CPU/memória/PIDs, códigos de saída, deltas dos contadores e estatísticas recalculadas. Nenhuma nova medição nesta revisão documental.

A execução local documentada é de Vênisson; a autoria experimental é compartilhada com Katyane. As estatísticas usam somente o lote WSL2 `20261110T144547Z_2382`, com três repetições por condição. Os dados e o relatório foram incorporados à main na integração da consolidação de Katyane. As declarações dos demais integrantes foram preservadas e se referem aos seus próprios registros e contextos.

### Declaração de Uso de IA — Katyane Santos

**Ferramenta:** ChatGPT (OpenAI).

**Finalidade:** Apoio à organização do repositório, documentação dos procedimentos de reprodução e preparação do checklist de entrega da Atividade 3.

#### Prompts relevantes utilizados

1. "Oriente a execução da minha Parte 7 — Consolidação, considerando o repositório já criado pela equipe e minhas responsabilidades no relatório, README e entrega."

2. "Ajude a organizar o README com preparação do ambiente, reprodução dos experimentos, coleta das evidências, limpeza e rastreabilidade, sem inventar resultados."

3. "Confira a estrutura do repositório e ajude a preparar um checklist para identificar materiais concluídos e pendentes de cada integrante."

#### Registro crítico

**Adotado:**
- Organização do README em seções de preparação, reprodução, coleta, limpeza e rastreabilidade.
- Criação de um checklist para acompanhar os requisitos da entrega.
- Identificação de campos pendentes para digest da imagem, commit final e link do vídeo.

**Corrigido:**
- A documentação inicial mencionava uma pasta `atividade3/`, mas os arquivos existentes estavam organizados diretamente na raiz do repositório. O título do README foi corrigido para refletir a estrutura observada. A decisão sobre reorganizar as pastas permanece pendente de alinhamento com a equipe.
- As contribuições foram descritas distinguindo atividades já realizadas de entregas ainda em preparação.

**Rejeitado ou não adotado:**
- Preenchimento de métricas experimentais sem evidências reais.
- Inclusão de digest, identificador de commit ou link de vídeo ainda não confirmados.
- Execução de comandos de limpeza indiscriminada que poderiam afetar outros projetos.

#### Verificação

As orientações foram conferidas por inspeção da estrutura do repositório e pelos comandos `git status` e `git diff`. Os procedimentos documentados no README ainda precisam ser validados pela equipe no ambiente experimental.

Nenhuma medição de CPU, memória ou namespaces foi produzida pela IA.


### Integração final

ChatGPT/Codex apoiou a resolução dos conflitos de README e contribuições, preservando as declarações individuais e os arquivos da consolidação de Katyane. Scripts e brutos não foram modificados. Os resultados WSL2 foram confrontados com seis JSON, CSV, hashes e relatório. Nenhuma medição nova foi realizada. As verificações ainda pendentes permanecem identificadas no checklist.
