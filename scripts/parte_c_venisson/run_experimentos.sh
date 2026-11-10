#!/usr/bin/env bash

set -u

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTADOS="$BASE/resultados"

IMAGEM="python@sha256:4840d514c583a4d3d8cad3940e68dee6f0f6f3635c12fcd0a3d74c21a5b93a54"

ITERACOES=20000000

mkdir -p "$RESULTADOS"

# Cada execução do script cria um diretório próprio.
LOTE="$(date -u +%Y%m%dT%H%M%SZ)_$$"
DESTINO="$RESULTADOS/$LOTE"
mkdir -p "$DESTINO"

printf '%s\n' "$IMAGEM" > "$DESTINO/imagem.txt"
printf '%s\n' "$ITERACOES" > "$DESTINO/iteracoes.txt"

printf 'ordem,condicao,repeticao,cpu,exit_code,arquivo\n' \
  > "$DESTINO/manifesto.csv"

CONDICOES=(C1 C2 C1 C2 C1 C2)
CPUS=(0.5 1.0 0.5 1.0 0.5 1.0)
REPETICOES=(1 1 2 2 3 3)

for i in "${!CONDICOES[@]}"; do
    CONDICAO="${CONDICOES[$i]}"
    CPU="${CPUS[$i]}"
    REP="${REPETICOES[$i]}"
    ORDEM=$((i + 1))

    NOME="${CONDICAO}_R${REP}"
    ARQUIVO="$DESTINO/${NOME}.json"
    ERRO="$DESTINO/${NOME}.stderr.txt"

    echo "Executando $NOME com quota de $CPU CPU"

    # Preserva stdout e stderr, inclusive em caso de falha.
    if command -v timeout >/dev/null 2>&1; then
        timeout --signal=TERM --kill-after=5s 90s \
          sudo docker run --rm \
          --network none \
          --cpus="$CPU" \
          --memory="256m" \
          --memory-swap="256m" \
          --pids-limit=64 \
          -v "$BASE:/app:ro" \
          -w /app \
          "$IMAGEM" \
          python coleta_cgroups.py "$ITERACOES" \
          > "$ARQUIVO" 2> "$ERRO"
        STATUS=$?
    else
        sudo docker run --rm \
          --network none \
          --cpus="$CPU" \
          --memory="256m" \
          --memory-swap="256m" \
          --pids-limit=64 \
          -v "$BASE:/app:ro" \
          -w /app \
          "$IMAGEM" \
          python coleta_cgroups.py "$ITERACOES" \
          > "$ARQUIVO" 2> "$ERRO"
        STATUS=$?
    fi

    printf '%s,%s,%s,%s,%s,%s\n' \
      "$ORDEM" "$CONDICAO" "$REP" "$CPU" "$STATUS" "$NOME.json" \
      >> "$DESTINO/manifesto.csv"

    echo "$NOME finalizado. Exit code: $STATUS"
done

echo "Registros armazenados em: $DESTINO"