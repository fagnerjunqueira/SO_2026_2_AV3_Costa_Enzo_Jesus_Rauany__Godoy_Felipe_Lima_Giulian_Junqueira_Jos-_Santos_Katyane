# Registros Brutos — Parte B: Evidências de Namespaces
**Responsável:** Fagner Junqueira  
**Referência de log compartilhado:** [`atividade3/evidencias/evidencia_ns_mount_20261109_203438.log`](evidencia_ns_mount_20261109_203438.log)  
**Data/Hora da Coleta:** 2026-11-09T23:34:39Z  

---

## 1. Parâmetros e Contexto de Execução

- **Ambiente Linux / Host do Daemon:** Docker Desktop 4.87.0 sobre WSL2 (Kernel `Linux 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64`, Distro `Ubuntu 26.04 LTS`, 12 CPUs lógicas).
- **Controladores / Cgroup:** CgroupVersion=2, CgroupDriver=cgroupfs.
- **Imagem Fixada por Digest (`IMAGEM_LAB`):**  
  `python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`
- **Contêineres independentes avaliados:**
  1. Contêiner A: `so_av3_fagner_cntA` (ID longo: `963cdfd4693ba03ab51f181e1c93cde73b1c42e20d2ae80e026f4f889601d643`)
  2. Contêiner B: `so_av3_fagner_cntB` (ID longo: `ad0842ed7ad9fef988bf020e0597c69f223045cc394754194555e928bed3fbfa`)

---

## 2. Registro Textual Bruto por Contêiner

### Contêiner A (`so_av3_fagner_cntA`)
```text
PID_host=6633
PID_1_comm=sleep
ns/pid=pid:[4026532869]
ns/mnt=mnt:[4026532401]
ns/net=net:[4026532871]
```

### Contêiner B (`so_av3_fagner_cntB`)
```text
PID_host=6679
PID_1_comm=sleep
ns/pid=pid:[4026532945]
ns/mnt=mnt:[4026532942]
ns/net=net:[4026532947]
```

> **Nota sobre o PID no host:** O PID retornado por `docker inspect` (`6633` e `6679`) pertence à tabela de processos da VM do Docker Desktop / WSL2 (o host do daemon Docker). Em ambientes com Docker Desktop no Windows/WSL2, o `/proc` do terminal do usuário na distribuição Ubuntu WSL2 não compartilha o PID namespace do container runtime se este residir na VM interna gerenciada do Docker Desktop (`docker-desktop`), razão pela qual a inspeção deve ser feita pelas interfaces oficiais e comandos executados via daemon.

---

## 3. Tabela Comparativa dos Namespaces

| Recurso | Handle em A (`so_av3_fagner_cntA`) | Handle em B (`so_av3_fagner_cntB`) | Iguais ou Diferentes | Interpretação |
| :--- | :--- | :--- | :--- | :--- |
| **PID (`/proc/1/ns/pid`)** | `pid:[4026532869]` | `pid:[4026532945]` | **Diferentes** | Cada contêiner possui uma árvore de processos isolada. No contêiner A, o processo raiz é mapeado como PID 1 internamente (PID 6633 no host); no contêiner B, o processo raiz também é visto como PID 1 internamente (PID 6679 no host). Um contêiner não enxerga nem pode enviar sinais aos processos do outro. |
| **Mount (`/proc/1/ns/mnt`)** | `mnt:[4026532401]` | `mnt:[4026532942]` | **Diferentes** | As tabelas de pontos de montagem são independentes. Cada contêiner tem sua própria visão da árvore de arquivos e diretórios (`rootfs`), permitindo, inclusive, pontos de montagem dedicados (como a montagem read-only `/dados:ro` presente exclusivamente no contêiner B) sem afetar a árvore do contêiner A ou do host. |
| **Network (`/proc/1/ns/net`)** | `net:[4026532871]` | `net:[4026532947]` | **Diferentes** | As interfaces de rede, tabelas de roteamento, regras de firewall e portas de escuta são completamente segregadas. Cada contêiner recebe seu próprio par de interface virtual (`veth`), endereço IP e pilha TCP/IP privativa no namespace. |

---

## 4. Compartilhamento da Coleta com a Parte D (Giulian)

A execução conjunta de `evidencia_ns_mount.sh` realizou concomitantemente o teste de menor privilégio e montagem somente leitura no Contêiner B:
- **Leitura do arquivo montado:** Sucesso (`cat /dados/texto.txt` retornou `Documento sintetico`).
- **Tentativa de escrita controlada:** Negação registrada (`touch: cannot touch '/dados/novo.txt': Read-only file system`).
- O log unificado está arquivado e preservado em `atividade3/evidencias/evidencia_ns_mount_20261109_203438.log`.

