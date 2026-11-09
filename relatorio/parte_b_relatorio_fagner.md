# Seção do Relatório — Parte B: Evidências de Namespaces
**Autor:** Fagner Junqueira  
**Integração no Relatório Final:** Esta seção deve ser inserida imediatamente após a **Parte A (Ambiente e Diagrama de Camadas)**, elaborada por Enzo Costa, pois detalha a camada de isolamento do kernel Linux (Namespaces) que operacionaliza os contêineres sobre o hardware/host documentado na Parte A.

---

## 1. Metodologia Reproduzível

Para observar a separação promovida pelo subsistema de namespaces do kernel Linux, foram instanciados dois contêineres independentes e concorrentes a partir da mesma imagem base fixada estritamente pelo seu digest criptográfico (`IMAGEM_LAB`):
- **Imagem:** `python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`
- **Ambiente de Execução:** Docker Desktop 4.87.0 sobre WSL2 (Kernel `Linux 6.18.33.2-microsoft-standard-WSL2`, Cgroup v2 com driver `cgroupfs`).
- **Nomes dos Contêineres:** `so_av3_fagner_cntA` (Contêiner A) e `so_av3_fagner_cntB` (Contêiner B).

O procedimento foi executado pelo script automatizado `atividade3/scripts/evidencia_ns_mount.sh`, que garantiu uma execução compartilhada única com a Parte D (Giulian Lima), assegurando limpeza determinística posterior. Em cada contêiner ativo, foram inspecionados:
1. O PID atribuído ao processo no espaço de endereçamento do host do daemon:
   ```bash
   docker inspect --format 'PID_host={{.State.Pid}}' NOME
   ```
2. O nome do comando em execução como PID 1 interno no contêiner:
   ```bash
   docker exec NOME sh -c 'cat /proc/1/comm'
   ```
3. Os descritores (handles/inodos) dos namespaces de PID, montagem (`mnt`) e rede (`net`) associados ao PID 1:
   ```bash
   docker exec NOME readlink /proc/1/ns/pid
   docker exec NOME readlink /proc/1/ns/mnt
   docker exec NOME readlink /proc/1/ns/net
   ```

---

## 2. Resultados Coletados

Os dados brutos registrados no arquivo de evidência [`atividade3/evidencias/evidencia_ns_mount_20261109_203438.log`](../evidencias/evidencia_ns_mount_20261109_203438.log) são apresentados a seguir:

- **Contêiner A (`so_av3_fagner_cntA`):**
  - PID no Host do Daemon: `6633`
  - Nome do PID 1 interno: `sleep`
  - `/proc/1/ns/pid`: `pid:[4026532869]`
  - `/proc/1/ns/mnt`: `mnt:[4026532401]`
  - `/proc/1/ns/net`: `net:[4026532871]`

- **Contêiner B (`so_av3_fagner_cntB`):**
  - PID no Host do Daemon: `6679`
  - Nome do PID 1 interno: `sleep`
  - `/proc/1/ns/pid`: `pid:[4026532945]`
  - `/proc/1/ns/mnt`: `mnt:[4026532942]`
  - `/proc/1/ns/net`: `net:[4026532947]`

### Tabela Comparativa dos Três Namespaces

| Recurso | Handle em A (`so_av3_fagner_cntA`) | Handle em B (`so_av3_fagner_cntB`) | Iguais ou Diferentes | Interpretação Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **PID (`/proc/1/ns/pid`)** | `pid:[4026532869]` | `pid:[4026532945]` | **Diferentes** | Árvores de numeração de processos completamente dissociadas. Ambos rodam `sleep` como PID 1 em suas visões locais, mas correspondem a processos distintos no kernel do host (`6633` e `6679`). |
| **Mount (`/proc/1/ns/mnt`)** | `mnt:[4026532401]` | `mnt:[4026532942]` | **Diferentes** | Tabelas de montagem de sistemas de arquivos isoladas. Cada contêiner possui sua própria hierarquia de diretórios; o Contêiner B recebeu o ponto de montagem read-only `/dados:ro` sem que este exista no Contêiner A. |
| **Network (`/proc/1/ns/net`)** | `net:[4026532871]` | `net:[4026532947]` | **Diferentes** | Pilhas de rede segregadas. Cada contêiner conta com interfaces virtuais, espaço de endereçamento IP e tabelas de roteamento e portas próprios. |

---

## 3. Análise dos Resultados: Como Ambos Podem Ter PID 1 Interno?

No Contêiner A e no Contêiner B, a consulta a `/proc/1/comm` retornou idêntico resultado (`sleep`), indicando que o primeiro processo criado em cada espaço possui localmente o identificador `PID 1`. No entanto, a inspeção pelo daemon Docker revelou que no host do daemon esses mesmos processos possuem identificadores distintos: `PID 6633` e `PID 6679`.

Essa dualidade decorre diretamente da arquitetura hierárquica e aninhada do **PID namespace** do Linux, descrita formalmente na documentação `namespaces(7)` [NS]:
1. **Virtualização da Visão de Processos:** Um PID namespace cria um conjunto isolado de números de identificação de processos. O primeiro processo instanciado em um novo PID namespace recebe obrigatoriamente o valor 1 e atua como o processo "init" daquele namespace, herdando processos órfãos locais.
2. **Mapeamento Multinível:** Cada processo no Linux possui múltiplos PIDs dependendo de qual nível hierárquico ele é observado:
   - Na visão do *namespace filho* (interior do contêiner), o processo enxerga a si mesmo como `1`.
   - Na visão do *namespace pai/raiz* (o host do daemon), esse mesmo processo é indexado de forma global unívoca na tabela de processos do kernel (`task_struct`), onde recebeu `6633` (Contêiner A) e `6679` (Contêiner B).
3. **Identidade Distinta:** O fato de ambos apresentarem internamente `PID 1` não indica identidade compartilhada, e sim visões virtuais homônimas em árvores separadas. A diferença incontestável entre os handles `pid:[4026532869]` e `pid:[4026532945]` comprova que o kernel alocou duas instâncias estruturais de PID namespace distintas.

---

## 4. Respostas às Questões de Análise

### Questão 2. Quais handles observados sustentam a separação de PID, mount e network? O que essa comparação permite concluir sobre a associação dos processos aos namespaces? Quais conclusões exigiriam testes próprios, como verificar alcance de rede, permissões de escrita, limites de recursos ou proteção contra fuga?

**Resposta:**
- **Handles que sustentam a separação:**
  - Separação de PID: sustentada pela discrepância entre `pid:[4026532869]` (Contêiner A) e `pid:[4026532945]` (Contêiner B).
  - Separação de Mount: sustentada pela discrepância entre `mnt:[4026532401]` (Contêiner A) e `mnt:[4026532942]` (Contêiner B).
  - Separação de Network: sustentada pela discrepância entre `net:[4026532871]` (Contêiner A) e `net:[4026532947]` (Contêiner B).
- **O que a comparação permite concluir:**  
  Conforme define `namespaces(7)`, os links simbólicos em `/proc/[pid]/ns/*` expõem o número do inodo do namespace do kernel correspondente. A diferença nos números comprova inequivocamente que os processos dos dois contêineres estão associados a instâncias distintas de estruturas de controle no kernel Linux. Conclui-se, portanto, que as visões de lista de processos, pontos de montagem e pilha de rede são isoladas no nível estrutural das tabelas do kernel.
- **Limites das conclusões e testes adicionais necessários:**  
  Ter handles diferentes em `/proc/1/ns/*` **não prova**:
  1. *Alcance de rede:* Não garante que um contêiner não possa se comunicar com o outro ou com a internet; para verificar conectividade, são necessários testes próprios de roteamento, ping/curl e regras de firewall/iptables.
  2. *Permissões de escrita e integridade:* Ter um mount namespace isolado não impede que ambos montem o mesmo diretório compartilhado do host com permissão de escrita. A garantia de integridade requer a aplicação de montagens somente leitura (`:ro`), como demonstrado no teste da Parte D (`touch: Read-only file system`).
  3. *Limites e contenção de recursos:* Namespaces não controlam quanta CPU ou RAM um processo pode consumir. O isolamento de recursos exige testes próprios de **cgroups v2** (avaliados na Parte C).
  4. *Proteção contra fuga (container breakout):* Namespaces isolam visões, mas compartilham o mesmo kernel; vulnerabilidades de kernel, exposição excessiva de capabilities (`CAP_SYS_ADMIN`), acesso desprotegido a `/sys` ou uso de `--privileged` permitiriam escape do isolamento. A segurança exige LSM (AppArmor/SELinux), seccomp e menor privilégio.

---

### Questão 3. Diferencie namespace, cgroup, identidade e política de acesso. Dê um exemplo curto de cada um no contexto do laboratório e deixe claro quais mecanismos foram verificados na Parte B.

**Resposta:**
Os quatro conceitos representam pilhas ortogonais e complementares da segurança e governança de processos no kernel Linux:

1. **Namespace (Visão de Recursos):**
   - *Definição:* Mecanismo do kernel que particiona e virtualiza recursos globais do sistema, determinando **o que o processo enxerga**.
   - *Exemplo no laboratório:* O PID namespace faz o processo `sleep` enxergar apenas a sua própria árvore local, onde aparece como PID 1, ocultando os processos do host e de outros contêineres.
2. **Cgroup — Control Group (Contabilização e Limite de Recursos):**
   - *Definição:* Mecanismo do kernel que agrupa processos para monitorar, contabilizar e restringir **quanto de recurso físico** eles podem consumir (CPU, memória, I/O, número de PIDs).
   - *Exemplo no laboratório:* O arquivo `cpu.max` (na Parte C) limitando uma carga a 0,5 CPU (50 ms por período de 100 ms) ou o teto de 256 MiB de RAM.
3. **Identidade (Credenciais de Sujeito):**
   - *Definição:* Propriedade associada ao processo que define **quem o processo é** perante o sistema operacional, tipicamente expressa por UID (User ID), GID (Group ID) e capabilities do Linux.
   - *Exemplo no laboratório:* Um contêiner executando como usuário não-root (ex.: UID 1000) e com remoção de privilégios (`--security-opt no-new-privileges:true`).
4. **Política de Acesso (Regras de Autorização e Controle):**
   - *Definição:* Conjunto de regras formais aplicadas pelo kernel (via permissões POSIX tradicionais, flags de montagem ou módulos de segurança como AppArmor/SELinux/seccomp) que determinam **o que o processo tem permissão de fazer**.
   - *Exemplo no laboratório:* A flag de montagem read-only `:ro` aplicada a `/dados` (Parte D), que instrui o VFS do kernel a rejeitar chamadas de sistema modificadoras como `open(O_WRONLY)` ou `unlink()`.

**Mecanismos efetivamente verificados na Parte B:**
Na Parte B, verificou-se **exclusivamente o mecanismo de Namespaces** (especificamente os namespaces de PID, Mount e Network, por meio da consulta aos inodos de `/proc/1/ns/*` e à tabela de processos). Os limites de cgroups pertencem à investigação da Parte C, enquanto identidade e política de acesso são avaliados no contexto da Parte D.

---

## 5. Referências Bibliográficas

- **[NS]** Linux man-pages. *namespaces(7) — overview of Linux namespaces*. Disponível em: <https://man7.org/linux/man-pages/man7/namespaces.7.html>. Acesso em: 09 nov. 2026.
- **[CG]** Linux Kernel Documentation. *Control Group v2*. Disponível em: <https://docs.kernel.org/admin-guide/cgroup-v2.html>.
- **[RES]** Docker Documentation. *Resource constraints*. Disponível em: <https://docs.docker.com/engine/containers/resource_constraints/>.

