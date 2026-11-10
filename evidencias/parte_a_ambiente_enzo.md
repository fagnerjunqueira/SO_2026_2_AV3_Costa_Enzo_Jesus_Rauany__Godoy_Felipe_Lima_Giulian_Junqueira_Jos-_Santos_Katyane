# Evidências — Parte A (Enzo Costa)

> **Registro da coleta:** Enzo informa que executou os comandos independentemente e obteve os mesmos resultados registrados abaixo. O assistente também executou os comandos no ambiente conectado para conferência e ajudou a transcrever e organizar este arquivo. A execução registrada pelo Enzo é a medição da Parte A; a execução do assistente é somente conferência.

**Coleta independente de Enzo:** 10/11/2026; horário não informado.
**Conferência adicional pelo assistente:** 10/11/2026, 12:16:03 (-03:00)
**Confirmação do daemon/contexto:** 10/11/2026, 12:17:09 (-03:00)
**Contexto Docker:** `desktop-linux`

## Host e WSL2

Informações do host Windows:

```text
Windows 10 Home Single Language
Versão 10.0.19045 / build 19045
Arquitetura: 64 bits
Processadores lógicos: 8
Memória física reportada: 8438841344 bytes
```

Comandos Linux executados:

```text
wsl -d Ubuntu -- uname -a
Linux DESKTOP-BHUFF6Q 6.18.58.1-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Tue Oct 27 00:24:11 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux

wsl -d Ubuntu -- sh -lc 'cat /etc/os-release; printf "nproc="; nproc; cat /proc/sys/kernel/osrelease'
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
UBUNTU_CODENAME=noble
nproc=8
6.18.58.1-microsoft-standard-WSL2
```

Na repetição, o WSL também imprimiu o aviso `Failed to start the systemd user session for 'enzo'`; apesar do aviso, `uname`, `/etc/os-release` e `nproc` foram executados e retornaram os dados acima.

`wsl --list --verbose`:

```text
NAME              STATE     VERSION
Ubuntu            Stopped   2
docker-desktop    Running   2
```

## Docker Engine

`docker version` reportou cliente 29.8.2 (`windows/amd64`) e servidor Docker Desktop 4.95.0, Engine 29.8.2 (`linux/amd64`).

Campos relevantes de `docker info`:

```text
Server Version: 29.8.2
Cgroup Driver: cgroupfs
Cgroup Version: 2
Kernel Version: 6.18.58.1-microsoft-standard-WSL2
Operating System: Docker Desktop
OSType: linux
Architecture: x86_64
CPUs: 8
Total Memory: 3.754GiB
Name: docker-desktop
```

## Imagem

Comandos executados:

```text
docker pull python:3.12-slim
Digest: sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
Status: Image is up to date for python:3.12-slim

docker image inspect --format 'ID={{.Id}} RepoDigests={{json .RepoDigests}} OS={{.Os}} Architecture={{.Architecture}}' python:3.12-slim
ID=sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b RepoDigests=["python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b"] OS=linux Architecture=amd64
```

`IMAGEM_LAB`:

```text
python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
```

Na consulta inicial, o daemon já tinha contêineres ativos; nenhum foi iniciado, parado ou removido para esta coleta. O contexto `desktop-linux` e a distro `docker-desktop` (WSL 2) estavam ativos na confirmação final.
