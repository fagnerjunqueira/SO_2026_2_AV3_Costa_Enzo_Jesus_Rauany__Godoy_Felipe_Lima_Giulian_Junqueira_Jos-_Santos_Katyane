# 5 - Confirmação dos limites e métricas de cgroup - Filipe de Carvalho Godoy

## 5.1 Escopo

Verificar se os limites solicitados na linha de comando do Docker foram
efetivamente aplicados pelo kernel, consolidar os contadores de CPU e as
métricas de memória do cgroup nas seis execuções, e responder à questão 4
das análises: como a quota foi confirmada e se houve throttling.

A coleta bruta foi produzida na Parte C (item 3 da divisão). Esta seção
trabalha sobre os mesmos registros, sem reexecutar o experimento, e usa o
script `verifica_limites.py` para derivar as tabelas abaixo.

## 5.2 Por que a flag não prova nada

O enunciado adverte que "a flag solicitada não prova que o limite foi
aplicado". `docker run --cpus=0.5` é uma *solicitação* ao runtime: ela
descreve a intenção, não o estado do kernel. Entre a flag e o enforcement há
o runtime (containerd/runc), o driver de cgroup e a disponibilidade dos
controladores no cgroup pai. Qualquer um pode falhar silenciosamente.

A prova está na leitura de `/sys/fs/cgroup/cpu.max`, `memory.max` e
`pids.max` **de dentro do contêiner**, que é o que o coletor fez antes de
cada execução. Como o contêiner tem namespace de cgroup próprio, esses
caminhos expõem o cgroup do próprio contêiner, e o valor lido é o que o
kernel está aplicando.

## 5.3 Confirmação dos limites

| Execução | `cpu.max` | Quota derivada | `memory.max` | `pids.max` | Confere |
|---|---|---:|---:|---:|:---:|
| C1_R1 | `50000 100000` | 0,50 CPU | 256 MiB | 64 | sim |
| C1_R2 | `50000 100000` | 0,50 CPU | 256 MiB | 64 | sim |
| C1_R3 | `50000 100000` | 0,50 CPU | 256 MiB | 64 | sim |
| C2_R1 | `100000 100000` | 1,00 CPU | 256 MiB | 64 | sim |
| C2_R2 | `100000 100000` | 1,00 CPU | 256 MiB | 64 | sim |
| C2_R3 | `100000 100000` | 1,00 CPU | 256 MiB | 64 | sim |

Os seis registros confirmam os três controladores. A quota não foi copiada da
flag: foi derivada do próprio `cpu.max`, dividindo quota por período
(50000/100000 = 0,5 e 100000/100000 = 1,0).

**Interpretação de `cpu.max`.** O par `50000 100000` significa 50 ms de tempo
de CPU agregado a cada período de 100 ms. Não é afinidade de núcleo nem
reserva: o cgroup pode rodar em qualquer CPU disponível, e o que o kernel
contabiliza é a soma do tempo consumido por todas as suas tarefas dentro de
cada janela. Num host com mais de um núcleo, duas tarefas do mesmo cgroup
rodando em paralelo esgotam a quota em metade do tempo de parede — fato que
se mostrou relevante na análise (seção 5.6).

`memory.max` em 268435456 bytes corresponde exatamente a 256 MiB. Com
`--memory-swap=256m` igual à memória, o contêiner fica sem swap adicional.

## 5.4 Contadores de CPU — deltas de `cpu.stat`

Os valores são diferenças entre a leitura feita imediatamente antes e
imediatamente depois da carga, não valores absolutos desde a criação do
cgroup.

| Execução | `usage_usec` Δ | Janela observada | Uso médio da CPU | Períodos | Throttled | % | `throttled_usec` Δ |
|---|---:|---:|---:|---:|---:|---:|---:|
| C1_R1 | 3,571 s | 10,60 s | 33,7% | 106 | 105 | 99% | 13,855 s |
| C1_R2 | 4,058 s | 11,90 s | 34,1% | 119 | 119 | 100% | 7,877 s |
| C1_R3 | 3,700 s | 10,50 s | 35,2% | 105 | 104 | 99% | 6,888 s |
| C2_R1 | 4,940 s | 5,20 s | 95,0% | 52 | 27 | 52% | 0,383 s |
| C2_R2 | 3,940 s | 7,80 s | 50,5% | 78 | 75 | 96% | 7,437 s |
| C2_R3 | 3,755 s | 7,30 s | 51,4% | 73 | 70 | 96% | 3,509 s |

A janela observada é `nr_periods × 100 ms`, ou seja, o tempo de parede
coberto pelos períodos contabilizados. O uso médio é
`usage_usec / janela`, a fração da CPU efetivamente consumida nesse intervalo.

**Houve throttling, e ele é maior em C1.** Em C1, entre 99% e 100% dos
períodos sofreram throttling, contra 52% a 96% em C2. A direção é a esperada:
quota mais apertada, mais períodos em que a quota se esgota antes do fim do
período.

**Três observações que impedem uma leitura ingênua desses números:**

Primeira: `usage_usec` é praticamente constante entre as condições — mediana
de 3,700 s em C1 e 3,940 s em C2. Isso é coerente, não contraditório: o
trabalho é o mesmo (checksum idêntico, 20 milhões de iterações), então o
*custo em CPU* deve ser o mesmo. O que a quota deveria alterar é o tempo de
*parede*, não o tempo de CPU.

Segunda: `throttled_usec` chega a 13,86 s numa janela de 10,60 s. O valor
excede o tempo de parede porque soma o tempo de espera de todas as tarefas do
cgroup; com duas tarefas bloqueadas simultaneamente, o acumulado cresce mais
rápido que o relógio. Esse contador mede espera agregada, não atraso
percebido.

Terceira: em C1 o uso médio ficou em torno de 34%, **abaixo** da quota de 50%.
Um cgroup throttled em 99% dos períodos que não consegue usar nem dois terços
da própria quota indica que a janela observada inclui tempo em que nenhuma
tarefa estava pronta para executar. A seção 5.6 mostra de onde vem esse tempo.

## 5.5 Memória — três métricas distintas

O enunciado pede que RSS, `memory.current` e `memory.peak` não sejam tratados
como a mesma grandeza. São coisas diferentes:

- **RSS** é a memória residente do processo da carga, lida de
  `/proc/<pid>/status`. Mede um processo.
- **`memory.current`** é o uso do cgroup inteiro no instante da leitura —
  inclui o coletor, o interpretador Python e páginas de cache atribuídas ao
  grupo.
- **`memory.peak`** é o maior valor que `memory.current` atingiu desde a
  criação do cgroup, incluindo a fase de inicialização do contêiner, anterior
  à carga.

| Execução | RSS do processo | `memory.current` (fim) | `memory.peak` | Teto | % do teto |
|---|---:|---:|---:|---:|---:|
| C1_R1 | 15,88 MiB | 12,00 MiB | 21,75 MiB | 256 MiB | 8,5% |
| C1_R2 | 15,75 MiB | 11,99 MiB | 21,74 MiB | 256 MiB | 8,5% |
| C1_R3 | 15,75 MiB | 12,01 MiB | 21,75 MiB | 256 MiB | 8,5% |
| C2_R1 | 15,62 MiB | 11,77 MiB | 21,62 MiB | 256 MiB | 8,4% |
| C2_R2 | 15,85 MiB | 12,00 MiB | 21,75 MiB | 256 MiB | 8,5% |
| C2_R3 | 15,67 MiB | 11,75 MiB | 21,48 MiB | 256 MiB | 8,4% |

A ordenação entre as três métricas é informativa. `memory.peak` (21,7 MiB)
supera o RSS do processo (15,8 MiB) porque o pico ocorre durante a
inicialização do contêiner, quando o interpretador do coletor e o da carga
coexistem. Já `memory.current` ao final (12,0 MiB) é *menor* que o RSS máximo
observado porque a carga já havia terminado e suas páginas foram liberadas
quando a leitura final aconteceu.

**O teto de memória foi configurado mas não exercitado.** Nenhuma execução
passou de 8,5% dos 256 MiB. O limite está comprovadamente aplicado — e é
isso que a tabela da seção 5.3 demonstra —, mas o experimento não produz
evidência sobre o comportamento do cgroup sob pressão de memória, porque
nunca chegou perto dela. O mesmo vale para `pids.max`: confirmado em 64 nas
seis execuções, nunca saturado.

## 5.6 Limitação identificada: o coletor compartilha a quota da carga

Esta seção documenta a causa das inconsistências de tempo registradas na
Parte C, que haviam sido observadas mas não atribuídas.

### O mecanismo

`coleta_cgroups.py` executa dentro do mesmo contêiner — portanto, dentro do
mesmo cgroup — da carga que ele mede. Enquanto a carga roda, o coletor
permanece num laço que lê `/proc/<pid>/status` e dorme 50 ms entre leituras.

Isso tem três consequências:

1. O coletor é uma **segunda tarefa** competindo pela mesma quota. Num host
   com dois núcleos, coletor e carga podem executar em paralelo e consumir
   até 2 CPUs de tempo agregado — o que esgota a quota de 1,0 CPU de C2 e
   explica por que C2 apresenta throttling apesar de a carga ser
   single-thread.
2. Os contadores de `cpu.stat` medem **coletor + carga**, não a carga
   isolada.
3. Quando o cgroup é throttled, o coletor também para. O laço demora mais
   para perceber que a carga terminou, e `tempo_monitoramento_s` infla.

### A evidência

O coletor declara amostrar a cada 50 ms. O intervalo efetivo entre amostras
mede o quanto ele próprio foi afetado:

| Execução | % períodos throttled | Amostras | Esperadas | Intervalo efetivo | Atraso | Situação |
|---|---:|---:|---:|---:|---:|---|
| C1_R1 | 99% | 6 | 212 | 1,768 s | 35,4× | degradado |
| C1_R2 | 100% | 7 | 238 | 1,702 s | 34,0× | degradado |
| C1_R3 | 99% | 13 | 205 | 0,789 s | 15,8× | degradado |
| **C2_R1** | **52%** | **87** | **94** | **0,054 s** | **1,1×** | **normal** |
| C2_R2 | 96% | 6 | 155 | 1,296 s | 25,9× | degradado |
| C2_R3 | 96% | 3 | 140 | 2,346 s | 46,9× | degradado |

A correlação é direta e tem um ponto de controle: **C2_R1 é a única execução
com throttling moderado (52%) e a única em que o coletor funcionou como
projetado** — 0,054 s por iteração, contra os 0,05 s programados, com 87 das
94 amostras esperadas. Nas outras cinco execuções, com throttling entre 96% e
100%, o intervalo efetivo cresceu de 16 a 47 vezes.

Isso também explica a terceira observação da seção 5.4: em C1, a carga
terminou em cerca de 3,4 s, mas o coletor levou 10,6 s para detectar o
encerramento. Os ~7 s restantes entram em `nr_periods` e `nr_throttled` sem
consumir `usage_usec`, deprimindo o uso médio para 34%.

### O que isso compromete e o que não compromete

**Não compromete** a confirmação dos limites (seção 5.3), que é leitura
direta de estado do kernel, nem a validação funcional: as seis execuções
produziram o mesmo checksum (4.864.000), código de saída zero e nenhum
timeout.

**Compromete** o uso de `tempo_monitoramento_s` como medida de desempenho da
carga, e torna os contadores de `cpu.stat` atribuíveis ao par
coletor + carga, não à carga sozinha.

### Anomalia não resolvida

Permanece uma discordância que estes dados não explicam: a carga reporta
`wall_time ≈ cpu_time` em todas as execuções (por exemplo, 3,391 s e 3,393 s
em C1_R1). Sob throttling sustentado a 0,5 CPU, o tempo de parede deveria
aproximar-se do dobro do tempo de CPU, já que o processo fica bloqueado sem
acumular tempo de processador.

Há hipóteses plausíveis — o escalonador pode ter priorizado a carga e
concentrado o throttling no coletor; a Parte C registrou eventos de *soft
lockup* na máquina virtual, que afetariam a confiabilidade do relógio de
espaço de usuário — mas nenhuma pode ser confirmada com as seis amostras
disponíveis, e o enunciado adverte explicitamente contra concluir causa a
partir de amostra única.

Registra-se, portanto, a divergência entre a medição interna (relógio do
processo) e a externa (contadores do kernel), sem atribuição de causa. Os
contadores do kernel são a fonte preferível, por não dependerem do relógio de
espaço de usuário da máquina virtual.

## 5.7 Resposta à questão 4

> **Como a quota foi confirmada? Houve throttling? Relacionar contadores,
> tempo e trabalho, sem concluir a causa por uma única amostra.**

**Confirmação da quota.** Por leitura de `/sys/fs/cgroup/cpu.max` de dentro de
cada contêiner, antes de cada uma das seis execuções, e não pela flag passada
ao Docker. Os valores lidos foram `50000 100000` em C1 e `100000 100000` em
C2, dos quais se deriva a quota real — 0,5 e 1,0 CPU por período de 100 ms.
`memory.max` (268435456 B = 256 MiB) e `pids.max` (64) foram confirmados pelo
mesmo procedimento. Os três controladores conferem nos seis registros.

**Throttling.** Sim, e o kernel o contabilizou em todas as execuções. Em C1,
entre 99% e 100% dos períodos; em C2, entre 52% e 96%. A direção acompanha a
restrição: quota menor, mais períodos esgotados.

**Relação entre contadores, tempo e trabalho.** O trabalho foi idêntico nas
seis execuções — mesmo número de iterações, mesmo checksum, mesmo código de
saída. O custo em CPU medido pelo kernel também foi praticamente constante
(mediana de 3,700 s em C1 e 3,940 s em C2), o que é coerente: a quota limita a
*taxa* de consumo, não a *quantidade* de trabalho a realizar. O que deveria
diferir entre as condições é o tempo de parede, e é justamente aí que as
medições se mostram inconsistentes.

**O que estes dados não permitem afirmar.** Que a quota de 0,5 CPU produziu a
desaceleração proporcional esperada na carga. A medição foi contaminada pela
presença do coletor no mesmo cgroup (seção 5.6), e o tempo interno reportado
pela carga contradiz o throttling contabilizado pelo kernel. A confirmação
dos limites e a ocorrência de throttling estão demonstradas; a magnitude do
efeito sobre o tempo de execução, não.

## 5.8 Correção recomendada para trabalhos futuros

A instrumentação deveria observar o cgroup **de fora** dele. Três ajustes
resolveriam a contaminação:

1. Executar o coletor no host, lendo
   `/sys/fs/cgroup/system.slice/docker-<id>.scope/cpu.stat`, de modo que o
   contêiner contenha apenas a carga.
2. Substituir a amostragem ativa de RSS por leitura única de
   `memory.peak` ao final, eliminando o laço periódico.
3. Medir o tempo de parede no host, com `/usr/bin/time` ou equivalente, em
   vez de depender do relógio interno do processo dentro da máquina virtual.

Nenhum desses ajustes foi aplicado ao lote analisado: os registros originais
foram preservados sem alteração, conforme o enunciado determina para
tentativas que apresentem problemas.

## 5.9 Artefatos desta seção

| Arquivo | Conteúdo |
|---|---|
| `scripts/verifica_limites.py` | Script de confirmação e consolidação |
| `evidencias/limites_cgroup.csv` | Tabela consolidada das seis execuções |
| `evidencias/cgroups_lote1/*.json` | Registros brutos das seis execuções (Parte C) |

Reprodução:

```bash
python3 scripts/verifica_limites.py evidencias/cgroups_lote1 \
    --csv evidencias/limites_cgroup.csv
```