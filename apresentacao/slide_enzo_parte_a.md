# Slide — Parte A: Ambiente e Camadas
**Responsável/apresentador:** Enzo Costa

> **Registro:** Enzo informa que executou os comandos e obteve estes resultados. O assistente repetiu a coleta para conferência e ajudou a preparar o slide.

```text
+-----------------------------------------------------------+
| PARTE A — AMBIENTE DO EXPERIMENTO                         |
| Windows 10 x64 | Docker Desktop 4.95.0 | Engine 29.8.2    |
+-----------------------------------------------------------+
| Hardware: 8 CPUs lógicas, ~7,86 GiB de RAM                |
|                         |                                 |
| Host Windows 10         |                                 |
|                         v                                 |
| VM leve WSL2 / Hyper-V (camada Linux intermediária)       |
| Kernel compartilhado: 6.18.58.1-microsoft-standard-WSL2   |
|       | Ubuntu 24.04.1          | Docker Desktop          |
|       | shell/CLI               | daemon Linux            |
|       |                         | cgroups v2 / cgroupfs    |
|       |                         v                         |
|       |                  Contêineres Linux                |
|       |                  (mesmo kernel Linux)              |
+-----------------------------------------------------------+
| IMAGEM: python:3.12-slim                                   |
| Digest: 5e2bdb1b0d54...13a4fa5b (ver completo no relatório) |
+-----------------------------------------------------------+
| Q1: contêineres compartilham o kernel WSL2, NÃO o Windows. |
| Há VM intermediária leve do WSL2; não é VM tradicional.   |
+-----------------------------------------------------------+
```

**Notas para fala (aprox. 45–60 s):**
“O host físico executa Windows 10. Para executar contêineres Linux, o Docker Desktop usa o backend WSL2: o daemon Linux e os contêineres ficam sobre o kernel Linux da VM utilitária, versão 6.18.58.1. A distribuição Ubuntu 24.04 é o shell usado para coletar `uname`, `os-release` e `nproc`, mas não é o daemon. O Docker reportou cgroups v2 com driver `cgroupfs`. A imagem foi baixada e fixada pelo digest mostrado no slide, para que as próximas execuções possam referenciar o mesmo conteúdo. Portanto, os contêineres compartilham o kernel Linux do WSL2 — não o kernel Windows — e há uma camada virtualizada leve intermediária.”

**Ressalva de integração:** o log de namespaces versionado no repositório registra outra versão do Docker Desktop/Engine e outro kernel. Confira [`../relatorio/parte_a_ambiente_enzo.md`](../relatorio/parte_a_ambiente_enzo.md) antes de afirmar que todas as medições vieram do mesmo ambiente.
