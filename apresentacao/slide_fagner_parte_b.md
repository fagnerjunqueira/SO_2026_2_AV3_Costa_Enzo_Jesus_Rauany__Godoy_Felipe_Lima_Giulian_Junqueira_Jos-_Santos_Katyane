# Slide — Parte B: Evidências de Namespaces
**Apresentador:** Fagner Junqueira  
**Tempo estimado de fala:** 60 a 90 segundos  

---

## Estrutura Visual do Slide (Sugestão de Layout)

```
+------------------------------------------------------------------------------------------+
|  PARTE B — EVIDÊNCIAS DE NAMESPACES: ISOLAMENTO DE PROCESSOS, MOUNT E REDE              |
|  Fagner Junqueira | Sistemas Operacionais 2026.2                                         |
+------------------------------------------------------------------------------------------+
|                                                                                          |
| [ TABELA COMPARATIVA DOS NAMESPACES ]                                                    |
| +----------+--------------------+--------------------+------------+--------------------+ |
| | Recurso  | Handle em Cont. A  | Handle em Cont. B  | Relação    | Interpretação      | |
| +----------+--------------------+--------------------+------------+--------------------+ |
| | PID      | pid:[4026532869]   | pid:[4026532945]   | DIFERENTES | Árvores isoladas   | |
| | Mount    | mnt:[4026532401]   | mnt:[4026532942]   | DIFERENTES | VFS independente   | |
| | Network  | net:[4026532871]   | net:[4026532947]   | DIFERENTES | Pilha IP segregada | |
| +----------+--------------------+--------------------+------------+--------------------+ |
|                                                                                          |
| [ O FENÔMENO DO PID 1 INTERNO vs. HOST ]                                                 |
|                                                                                          |
|  * Contêiner A: /proc/1/comm = sleep  <--->  Host do Daemon: PID = 6633                 |
|  * Contêiner B: /proc/1/comm = sleep  <--->  Host do Daemon: PID = 6679                 |
|                                                                                          |
|  -> Mapeamento Hierárquico no Linux (namespaces(7)):                                     |
|     O kernel virtualiza a tabela de processos: o processo 'init' de cada namespace      |
|     recebe o número 1 localmente, mas mantém seu PID global único na tabela do kernel.    |
|                                                                                          |
| [ DESTAQUE DO LOG BRUTO PARA A APRESENTAÇÃO ]                                           |
|  Arquivo: atividade3/evidencias/evidencia_ns_mount_20261109_203438.log                     |
|  Trecho:                                                                                 |
|    --- CONTÊINER: so_av3_fagner_cntA ---      --- CONTÊINER: so_av3_fagner_cntB ---     |
|    PID_host=6633                              PID_host=6679                              |
|    ns/pid=pid:[4026532869]                    ns/pid=pid:[4026532945]                    |
|    ns/mnt=mnt:[4026532401]                    ns/mnt=mnt:[4026532942]                    |
|    ns/net=net:[4026532871]                    ns/net=net:[4026532947]                    |
|                                                                                          |
| [ LIMITAÇÃO CRÍTICA ]                                                                    |
|  * Namespace isola VISÃO, mas compartilha o mesmo kernel e não impõe limite de recursos  |
|    (função dos cgroups) nem impede comunicação de rede sem regras ativas.                |
+------------------------------------------------------------------------------------------+
```

---

## Trecho do Log Selecionado para Projeção / Demonstração Rápida

Se for solicitado durante a apresentação ou perguntas a exibição do terminal/arquivo bruto, abra diretamente o arquivo [`atividade3/evidencias/evidencia_ns_mount_20261109_203438.log`](../evidencias/evidencia_ns_mount_20261109_203438.log) entre as linhas 20 e 34:

```text
=== 4. PARTE B: COLETA DE NAMESPACES (FAGNER JUNQUEIRA) ===
--- CONTÊINER: so_av3_fagner_cntA ---
PID_host=6633
PID_1_comm=sleep
ns/pid=pid:[4026532869]
ns/mnt=mnt:[4026532401]
ns/net=net:[4026532871]

--- CONTÊINER: so_av3_fagner_cntB ---
PID_host=6679
PID_1_comm=sleep
ns/pid=pid:[4026532945]
ns/mnt=mnt:[4026532942]
ns/net=net:[4026532947]
```

