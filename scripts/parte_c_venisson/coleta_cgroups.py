import json
import subprocess
import sys
import time
from pathlib import Path

# ============================================================
# UFS — SISTEMAS OPERACIONAIS 2026.2
# ATIVIDADE 3 — EXPERIMENTO DE CGROUPS
# ============================================================

CGROUP = Path("/sys/fs/cgroup")
TEMPO_LIMITE = 60
INTERVALO_RSS = 0.05


def ler_arquivo(nome):
    try:
        return (CGROUP / nome).read_text().strip()
    except OSError:
        return None


def ler_cpu_stat():
    dados = {}
    conteudo = ler_arquivo("cpu.stat")

    if conteudo:
        for linha in conteudo.splitlines():
            partes = linha.split()

            if len(partes) == 2:
                try:
                    dados[partes[0]] = int(partes[1])
                except ValueError:
                    pass

    return dados


def ler_rss(pid):
    try:
        conteudo = Path(f"/proc/{pid}/status").read_text()

        for linha in conteudo.splitlines():
            if linha.startswith("VmRSS:"):
                return int(linha.split()[1])

    except (OSError, ValueError, IndexError):
        pass

    return None


def calcular_deltas(antes, depois):
    chaves = [
        "usage_usec",
        "nr_periods",
        "nr_throttled",
        "throttled_usec",
    ]

    return {
        f"{chave}_delta": (
            depois[chave] - antes[chave]
            if chave in antes and chave in depois
            else None
        )
        for chave in chaves
    }


def executar_carga(iteracoes):
    processo = subprocess.Popen(
        [
            sys.executable,
            "/app/carga_cpu.py",
            "--iteracoes",
            str(iteracoes),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    inicio = time.monotonic()
    amostras_rss = []
    timeout_ocorreu = False

    while True:
        rss = ler_rss(processo.pid)

        if rss is not None:
            amostras_rss.append(rss)

        if processo.poll() is not None:
            break

        if time.monotonic() - inicio >= TEMPO_LIMITE:
            timeout_ocorreu = True
            processo.kill()
            break

        time.sleep(INTERVALO_RSS)

    stdout, stderr = processo.communicate()

    return {
        "pid_interno": processo.pid,
        "exit_code": processo.returncode,
        "timeout": timeout_ocorreu,
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "rss_max_observado_kb": (
            max(amostras_rss) if amostras_rss else None
        ),
        "quantidade_amostras": len(amostras_rss),
        "tempo_monitoramento_s": round(
            time.monotonic() - inicio, 6
        ),
    }


def main():
    if len(sys.argv) != 2:
        print(
            "Uso: python coleta_cgroups.py ITERACOES",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        iteracoes = int(sys.argv[1])

        if iteracoes <= 0:
            raise ValueError

    except ValueError:
        print(
            "ITERACOES deve ser um inteiro positivo.",
            file=sys.stderr,
        )
        sys.exit(1)

    limites = {
        "cpu_max": ler_arquivo("cpu.max"),
        "memory_max": ler_arquivo("memory.max"),
        "pids_max": ler_arquivo("pids.max"),
    }

    cpu_antes = ler_cpu_stat()

    memoria_antes = {
        "memory_current": ler_arquivo("memory.current"),
        "memory_peak": ler_arquivo("memory.peak"),
    }

    inicio_coleta = time.perf_counter()

    try:
        execucao = executar_carga(iteracoes)

    except Exception as erro:
        execucao = {
            "pid_interno": None,
            "exit_code": 1,
            "timeout": False,
            "stdout": "",
            "stderr": str(erro),
            "rss_max_observado_kb": None,
            "quantidade_amostras": 0,
            "tempo_monitoramento_s": None,
        }

    tempo_total = time.perf_counter() - inicio_coleta

    cpu_depois = ler_cpu_stat()

    memoria_depois = {
        "memory_current": ler_arquivo("memory.current"),
        "memory_peak": ler_arquivo("memory.peak"),
    }

    resultado_carga = None

    try:
        resultado_carga = json.loads(execucao["stdout"])
    except (json.JSONDecodeError, TypeError):
        pass

    resultado = {
        "experimento": "Atividade 3 - Cgroups",
        "iteracoes": iteracoes,
        "limites": limites,
        "cpu_stat_antes": cpu_antes,
        "cpu_stat_depois": cpu_depois,
        "deltas_cpu": calcular_deltas(
            cpu_antes,
            cpu_depois,
        ),
        "memoria_antes": memoria_antes,
        "memoria_depois": memoria_depois,
        "rss": {
            "pid_interno": execucao["pid_interno"],
            "rss_max_observado_kb": (
                execucao["rss_max_observado_kb"]
            ),
            "quantidade_amostras": (
                execucao["quantidade_amostras"]
            ),
            "intervalo_amostragem_s": INTERVALO_RSS,
        },
        "execucao": {
            "exit_code": execucao["exit_code"],
            "timeout": execucao["timeout"],
            "tempo_monitoramento_s": (
                execucao["tempo_monitoramento_s"]
            ),
            "tempo_total_coleta_s": round(
                tempo_total, 6
            ),
            "resultado_carga": resultado_carga,
            "stdout_bruto": execucao["stdout"],
            "stderr_bruto": execucao["stderr"],
        },
    }

    print(json.dumps(
        resultado,
        indent=2,
        ensure_ascii=False,
    ))

    if execucao["timeout"]:
        sys.exit(124)

    sys.exit(execucao["exit_code"])


if __name__ == "__main__":
    main()