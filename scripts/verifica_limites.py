#!/usr/bin/env python3
"""
Atividade 3 — Parte C — Confirmação de limites e métricas de cgroup
UFS | Sistemas Operacionais 2026.2 | Equipe Gemma
Responsável: Filipe de Carvalho Godoy

Verifica, a partir dos registros brutos das seis execuções, se os limites
pedidos na linha de comando foram de fato aplicados pelo kernel, e consolida
as métricas de CPU e memória do cgroup.

A flag --cpus do Docker é uma solicitação ao runtime. A prova de que o limite
existe é a leitura de /sys/fs/cgroup/cpu.max de dentro do próprio contêiner,
que é o que os registros contêm.

Uso:
    python3 verifica_limites.py RESULTADOS/
    python3 verifica_limites.py RESULTADOS/ --csv limites_cgroup.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

PERIODO_US = 100_000          # 100 ms — período padrão do cpu.max
MIB = 1024 * 1024

# Valores que o enunciado exige, por condição
ESPERADO = {
    "C1": {"cpu_max": "50000 100000", "quota_cpu": 0.5},
    "C2": {"cpu_max": "100000 100000", "quota_cpu": 1.0},
}
MEMORY_MAX_ESPERADO = 256 * MIB   # 268435456 bytes
PIDS_MAX_ESPERADO = "64"
INTERVALO_AMOSTRAGEM_S = 0.05     # declarado em coleta_cgroups.py


def carregar(diretorio: Path) -> list[dict]:
    """Lê os JSONs das execuções, em ordem de nome."""
    registros = []
    for caminho in sorted(diretorio.glob("C*_R*.json")):
        with caminho.open(encoding="utf-8") as f:
            dados = json.load(f)
        dados["_arquivo"] = caminho.name
        dados["_nome"] = caminho.stem
        dados["_condicao"] = caminho.stem.split("_")[0]
        registros.append(dados)
    return registros


def conferir_limites(reg: dict) -> dict:
    """Compara os limites lidos do cgroup com os valores exigidos."""
    lim = reg["limites"]
    cond = reg["_condicao"]
    esperado = ESPERADO.get(cond, {})

    cpu_ok = lim.get("cpu_max") == esperado.get("cpu_max")
    mem_ok = int(lim.get("memory_max", -1)) == MEMORY_MAX_ESPERADO
    pids_ok = lim.get("pids_max") == PIDS_MAX_ESPERADO

    # quota derivada do próprio cpu.max, não da flag
    partes = (lim.get("cpu_max") or "").split()
    quota_lida = (
        int(partes[0]) / int(partes[1])
        if len(partes) == 2 and partes[0] != "max"
        else None
    )

    return {
        "cpu_max": lim.get("cpu_max"),
        "cpu_max_ok": cpu_ok,
        "quota_derivada": quota_lida,
        "memory_max_b": int(lim.get("memory_max", 0)),
        "memory_max_mib": int(lim.get("memory_max", 0)) / MIB,
        "memory_max_ok": mem_ok,
        "pids_max": lim.get("pids_max"),
        "pids_max_ok": pids_ok,
        "todos_ok": cpu_ok and mem_ok and pids_ok,
    }


def metricas_cpu(reg: dict) -> dict:
    """Deltas de cpu.stat e indicadores derivados."""
    d = reg["deltas_cpu"]
    periodos = d["nr_periods_delta"]
    throttled = d["nr_throttled_delta"]
    usage = d["usage_usec_delta"]

    # janela coberta pelos períodos observados
    janela_us = periodos * PERIODO_US

    return {
        "usage_usec_delta": usage,
        "usage_s": usage / 1e6,
        "nr_periods_delta": periodos,
        "nr_throttled_delta": throttled,
        "pct_periodos_throttled": 100 * throttled / periodos if periodos else 0,
        "throttled_usec_delta": d["throttled_usec_delta"],
        "throttled_s": d["throttled_usec_delta"] / 1e6,
        "janela_s": janela_us / 1e6,
        # fração média da CPU efetivamente consumida na janela observada
        "uso_medio_cpu": usage / janela_us if janela_us else 0,
    }


def metricas_memoria(reg: dict) -> dict:
    """As três métricas de memória, mantidas distintas.

    O enunciado pede explicitamente que não sejam tratadas como a mesma coisa:
      - RSS         : memória residente do processo da carga
      - memory.current : uso do cgroup inteiro no instante da leitura
      - memory.peak    : maior uso do cgroup desde a criação
    """
    dep = reg["memoria_depois"]
    ant = reg["memoria_antes"]
    rss = reg["rss"]

    return {
        "rss_max_kb": rss["rss_max_observado_kb"],
        "rss_max_mib": (rss["rss_max_observado_kb"] or 0) / 1024,
        "memory_current_antes_mib": int(ant["memory_current"]) / MIB,
        "memory_current_depois_mib": int(dep["memory_current"]) / MIB,
        "memory_peak_mib": int(dep["memory_peak"]) / MIB,
        "ocupacao_do_teto_pct": 100 * int(dep["memory_peak"]) / MEMORY_MAX_ESPERADO,
        "amostras_rss": rss["quantidade_amostras"],
    }


def integridade_amostragem(reg: dict, mem: dict) -> dict:
    """Avalia se o coletor conseguiu amostrar no ritmo que ele mesmo declara.

    O coletor roda DENTRO do mesmo cgroup da carga e dorme 50 ms entre
    amostras. Se o cgroup é throttled, o coletor também é — e o intervalo
    efetivo entre amostras cresce. A razão entre o intervalo observado e os
    50 ms declarados mede o quanto a própria medição foi afetada.
    """
    mon = reg["execucao"]["tempo_monitoramento_s"]
    amostras = mem["amostras_rss"] or 1

    intervalo_efetivo = mon / amostras
    esperadas = int(mon / INTERVALO_AMOSTRAGEM_S)

    return {
        "tempo_monitoramento_s": mon,
        "amostras_esperadas": esperadas,
        "intervalo_efetivo_s": intervalo_efetivo,
        "fator_atraso": intervalo_efetivo / INTERVALO_AMOSTRAGEM_S,
        "coletor_degradado": intervalo_efetivo > 2 * INTERVALO_AMOSTRAGEM_S,
    }


def analisar(registros: list[dict]) -> list[dict]:
    linhas = []
    for reg in registros:
        lim = conferir_limites(reg)
        cpu = metricas_cpu(reg)
        mem = metricas_memoria(reg)
        amo = integridade_amostragem(reg, mem)
        carga = reg["execucao"]["resultado_carga"] or {}

        linhas.append({
            "execucao": reg["_nome"],
            "condicao": reg["_condicao"],
            **lim,
            **cpu,
            **mem,
            **amo,
            "wall_carga_s": carga.get("wall_time_s"),
            "cpu_processo_s": carga.get("cpu_time_s"),
            "checksum": carga.get("checksum"),
            "status": carga.get("status"),
            "exit_code": reg["execucao"]["exit_code"],
            "timeout": reg["execucao"]["timeout"],
        })
    return linhas


# ----------------------------------------------------------------------
# Relatório em texto
# ----------------------------------------------------------------------
def imprimir(linhas: list[dict]) -> None:
    sep = "=" * 78

    print(sep)
    print("1. CONFIRMAÇÃO DOS LIMITES — lidos de /sys/fs/cgroup dentro do contêiner")
    print(sep)
    print(f"{'exec':8} {'cpu.max':17} {'quota':>6} {'memory.max':>13} "
          f"{'pids.max':>9} {'ok'}")
    for l in linhas:
        marca = "sim" if l["todos_ok"] else "NAO"
        print(f"{l['execucao']:8} {l['cpu_max']:17} {l['quota_derivada']:6.2f} "
              f"{l['memory_max_mib']:10.0f} MiB {l['pids_max']:>9} {marca:>5}")

    todos = all(l["todos_ok"] for l in linhas)
    print(f"\n  -> {'Todos os limites conferem' if todos else 'HÁ DIVERGÊNCIA'} "
          f"nas {len(linhas)} execuções.")

    print()
    print(sep)
    print("2. CPU — deltas de cpu.stat")
    print(sep)
    print(f"{'exec':8} {'usage_s':>8} {'janela_s':>9} {'uso_med':>8} "
          f"{'periodos':>9} {'throttled':>10} {'%thr':>6} {'thr_s':>8}")
    for l in linhas:
        print(f"{l['execucao']:8} {l['usage_s']:8.3f} {l['janela_s']:9.2f} "
              f"{l['uso_medio_cpu']:8.1%} {l['nr_periods_delta']:9d} "
              f"{l['nr_throttled_delta']:10d} {l['pct_periodos_throttled']:5.0f}% "
              f"{l['throttled_s']:8.3f}")

    print()
    print(sep)
    print("3. MEMÓRIA — três métricas distintas")
    print(sep)
    print(f"{'exec':8} {'RSS proc':>10} {'current fim':>12} {'peak':>10} "
          f"{'teto':>8} {'% do teto':>10}")
    for l in linhas:
        print(f"{l['execucao']:8} {l['rss_max_mib']:7.2f} MiB "
              f"{l['memory_current_depois_mib']:9.2f} MiB "
              f"{l['memory_peak_mib']:7.2f} MiB {l['memory_max_mib']:5.0f} MiB "
              f"{l['ocupacao_do_teto_pct']:9.1f}%")

    print()
    print(sep)
    print("4. INTEGRIDADE DA AMOSTRAGEM — o coletor compartilha a quota da carga")
    print(sep)
    print(f"{'exec':8} {'%thr':>6} {'amostras':>9} {'esperadas':>10} "
          f"{'interv.':>9} {'atraso':>8}  situação")
    for l in linhas:
        sit = "degradado" if l["coletor_degradado"] else "normal"
        print(f"{l['execucao']:8} {l['pct_periodos_throttled']:5.0f}% "
              f"{l['amostras_rss']:9d} {l['amostras_esperadas']:10d} "
              f"{l['intervalo_efetivo_s']:8.3f}s {l['fator_atraso']:7.1f}x  {sit}")

    degradados = [l for l in linhas if l["coletor_degradado"]]
    print(f"\n  -> {len(degradados)} de {len(linhas)} execuções com coletor "
          f"degradado.")

    print()
    print(sep)
    print("5. VALIDAÇÃO FUNCIONAL")
    print(sep)
    checksums = {l["checksum"] for l in linhas}
    exits = {l["exit_code"] for l in linhas}
    print(f"  checksums distintos : {checksums}")
    print(f"  exit codes          : {exits}")
    print(f"  timeouts            : {sum(1 for l in linhas if l['timeout'])}")
    print(f"  -> trabalho idêntico e correto em todas as execuções"
          if len(checksums) == 1 and exits == {0}
          else "  -> ATENÇÃO: divergência funcional")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Confirma limites e consolida métricas de cgroup (Parte C)")
    ap.add_argument("diretorio", type=Path,
                    help="diretório com os JSONs das execuções")
    ap.add_argument("--csv", type=Path, default=None,
                    help="grava a tabela consolidada neste caminho")
    args = ap.parse_args()

    if not args.diretorio.is_dir():
        print(f"Diretório não encontrado: {args.diretorio}", file=sys.stderr)
        sys.exit(1)

    registros = carregar(args.diretorio)
    if not registros:
        print(f"Nenhum JSON C*_R*.json em {args.diretorio}", file=sys.stderr)
        sys.exit(1)

    linhas = analisar(registros)
    imprimir(linhas)

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)
        print(f"\nCSV gravado em: {args.csv}")


if __name__ == "__main__":
    main()