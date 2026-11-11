# Seção do Relatório — Parte A: Ambiente e Diagrama de Camadas
**Responsável:** Enzo Costa
**Atividade:** Sistemas Operacionais — UFS 2026.2

> **Registro da coleta e assistência:** Enzo informa que executou os comandos da Parte A independentemente e obteve os mesmos resultados aqui apresentados. O assistente também repetiu os comandos no ambiente conectado para conferência e auxiliou na organização do registro, na redação e no diagrama. A medição é atribuída à execução independente de Enzo; a execução do assistente foi somente conferência.

## 1. Ambiente observado

A coleta foi feita em 10/11/2026, no Windows 10 Home Single Language (build 19045), usando a distribuição Ubuntu 24.04.1 LTS no WSL2 e o contexto Docker `desktop-linux`. O daemon é o Docker Engine fornecido pelo Docker Desktop, não um daemon Linux nativo do Windows nem um serviço executado diretamente na distribuição Ubuntu.

| Componente | Resultado observado |
|---|---|
| Host físico/Windows | Windows 10 Home Single Language, 64 bits, build 19045 |
| Processadores lógicos do host | 8 |
| Memória física reportada pelo Windows | 8.438.841.344 bytes |
| Distribuição WSL usada para os comandos Linux | Ubuntu 24.04.1 LTS |
| Kernel Linux | `6.18.58.1-microsoft-standard-WSL2` (x86_64) |
| `nproc` na distribuição WSL | 8 |
| Plataforma do daemon | Docker Desktop 4.95.0; Docker Engine 29.8.2, `linux/amd64` |
| Nome/OS reportado pelo daemon | `docker-desktop` / Docker Desktop |
| CPU e memória reportadas pelo daemon | 8 CPUs; 3.754 GiB |
| Cgroups do daemon | v2, driver `cgroupfs` |
| Imagem do laboratório | `python:3.12-slim`, Linux/amd64 |
| Digest da imagem | `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b` |

O digest completo usado como `IMAGEM_LAB` é:

```text
python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
```

Os comandos e saídas relevantes desta coleta estão registrados em [`../evidencias/parte_a_ambiente_enzo.md`](../evidencias/parte_a_ambiente_enzo.md).

## 2. Diagrama de camadas

```text
+---------------------------------------------------------------+
| Hardware x86_64                                               |
| 8 CPUs lógicas; 8.438.841.344 bytes de RAM reportados          |
+---------------------------------------------------------------+
                              |
+---------------------------------------------------------------+
| Host: Windows 10 Home Single Language (build 19045)            |
+---------------------------------------------------------------+
                              |
| Hyper-V / virtualização leve gerenciada pelo WSL2              |
| (há uma camada Linux virtualizada intermediária)               |
|                                                               |
|  +----------------------------------------------------------+ |
|  | VM utilitária WSL2                                       | |
|  | Kernel Linux 6.18.58.1-microsoft-standard-WSL2            | |
|  |                                                          | |
|  |  +---------------------+  +-----------------------------+| |
|  |  | Distro Ubuntu       |  | Distro/ambiente              || |
|  |  | 24.04.1 LTS         |  | Docker Desktop               || |
|  |  | shell Linux         |  | daemon: Engine 29.8.2        || |
|  |  +---------------------+  +--------------+--------------+| |
|  |                                          |               | |
|  |                              +-----------+-----------+   | |
|  |                              | Contêineres Linux     |   | |
|  |                              | namespaces/cgroups    |   | |
|  |                              +-----------------------+   | |
|  +----------------------------------------------------------+ |
+---------------------------------------------------------------+
```

O desenho representa a arquitetura observada pelo contexto `desktop-linux`: o Windows é o host, o Docker Desktop fornece o daemon Linux e o backend WSL2 fornece o kernel Linux. A distribuição Ubuntu é o ambiente de shell usado para `uname`, `/etc/os-release` e `nproc`; ela não é, por si só, o daemon. Os contêineres Linux compartilham o kernel Linux do backend, enquanto namespaces e cgroups controlam visões e recursos.

## 3. Questão 1 — Onde está o kernel compartilhado? Há uma VM intermediária?

O kernel compartilhado pelos contêineres Linux está no backend WSL2 do Docker Desktop: `6.18.58.1-microsoft-standard-WSL2`. Os contêineres não executam cada um seu próprio kernel e não usam o kernel do Windows; compartilham esse kernel Linux, com isolamento de processos e recursos provido pelo kernel.

Sim, há uma camada virtualizada intermediária entre o Windows e o daemon/contêineres Linux: a VM utilitária leve gerenciada pelo WSL2 (baseada em Hyper-V). Não é uma VM tradicional criada e administrada separadamente pelo usuário. O Ubuntu WSL e o ambiente Docker Desktop são distribuições/ambientes Linux associados ao backend WSL2.

## 4. Limite de consistência entre as evidências do repositório

O log já existente da Parte B registra Docker Engine 29.7.2 e kernel `6.18.33.2-microsoft-standard-WSL2`; a seção de relatório da Parte B também menciona Docker Desktop 4.87.0. Esta coleta da Parte A registrou Engine 29.8.2, Docker Desktop 4.95.0 e kernel `6.18.58.1-microsoft-standard-WSL2`. Portanto, os dados atuais de A e as evidências B/D já versionadas não são da mesma configuração observada e não devem ser apresentados como uma única rodada experimental. Para cumprir a regra de ambiente único, a equipe deve combinar e identificar uma execução comum ou repetir as coletas pertinentes no ambiente escolhido. O digest da imagem registrado no log antigo coincide com o digest obtido nesta coleta, mas isso não elimina a diferença de ambiente.

Na consulta inicial ao daemon foram reportados contêineres já em execução. Eles não foram iniciados, interrompidos ou removidos durante esta Parte A.
