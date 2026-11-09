#!/usr/bin/env bash
# evidencia_ns_mount.sh
# Coleta compartilhada para Parte B (Namespaces - Fagner) e Parte D (Mount e menor privilégio - Giulian)
# Sistemas Operacionais - Atividade 3 | UFS 2026.2

set -euo pipefail

TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
OUT_DIR="$(dirname "$0")/../evidencias"
mkdir -p "$OUT_DIR"
LOG_FILE="$OUT_DIR/evidencia_ns_mount_${TIMESTAMP}.log"

echo "=== INICIANDO COLETA COMPARTILHADA (PARTE B & PARTE D) ===" | tee "$LOG_FILE"
echo "Data/Hora: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" | tee -a "$LOG_FILE"
echo "Executado por: Fagner Junqueira (compartilhado com Giulian)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. Registro do Ambiente
echo "=== 1. REGISTRO DO AMBIENTE ===" | tee -a "$LOG_FILE"
echo "Host Kernel / OS: $(uname -s -r -v -m)" | tee -a "$LOG_FILE"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Linux Distro: $PRETTY_NAME" | tee -a "$LOG_FILE"
fi
echo "CPUs lógicas: $(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 'N/A')" | tee -a "$LOG_FILE"
echo "Docker Client/Server Version:" | tee -a "$LOG_FILE"
docker version --format 'Client Version: {{.Client.Version}} | Server Version: {{.Server.Version}} (OS/Arch: {{.Server.Os}}/{{.Server.Arch}})' | tee -a "$LOG_FILE"
docker info --format 'CgroupVersion={{.CgroupVersion}} CgroupDriver={{.CgroupDriver}} OperatingSystem={{.OperatingSystem}} KernelVersion={{.KernelVersion}}' | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 2. Definição da Imagem Fixada por Digest
IMAGEM_REPO="python:3.12-slim"
IMAGEM_LAB="$(docker image inspect --format '{{index .RepoDigests 0}}' "$IMAGEM_REPO" 2>/dev/null || echo '')"
if [ -z "$IMAGEM_LAB" ]; then
    echo "ERRO: Imagem $IMAGEM_REPO nao encontrada localmente. Execute docker pull $IMAGEM_REPO" | tee -a "$LOG_FILE"
    exit 1
fi
echo "=== 2. IMAGEM FIXADA POR DIGEST ===" | tee -a "$LOG_FILE"
echo "IMAGEM_LAB: $IMAGEM_LAB" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Nomes dos contêineres
CONT_A="so_av3_fagner_cntA"
CONT_B="so_av3_fagner_cntB"

# Função de limpeza estrita (limpa apenas o que foi criado por este script)
cleanup() {
    echo "" | tee -a "$LOG_FILE"
    echo "=== LIMPANDO CONTÊINERES DO TESTE ===" | tee -a "$LOG_FILE"
    docker rm -f "$CONT_A" "$CONT_B" >/dev/null 2>&1 || true
    rm -rf dados_demo >/dev/null 2>&1 || true
    echo "Limpeza concluida." | tee -a "$LOG_FILE"
}
trap cleanup EXIT INT TERM

# Garante que não existem resquícios anteriores
docker rm -f "$CONT_A" "$CONT_B" >/dev/null 2>&1 || true

# Preparação para Parte D: diretório sintético para teste de mount ro
mkdir -p dados_demo
printf '%s\n' 'Documento sintetico' > dados_demo/texto.txt

echo "=== 3. INICIANDO CONTÊINERES ===" | tee -a "$LOG_FILE"
# Contêiner A: contêiner independente para Parte B
docker run -d --name "$CONT_A" "$IMAGEM_LAB" sleep 60 | tee -a "$LOG_FILE"
# Contêiner B: contêiner independente com montagem read-only para Parte B e D
docker run -d --name "$CONT_B" -v "$PWD/dados_demo:/dados:ro" "$IMAGEM_LAB" sleep 60 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "=== 4. PARTE B: COLETA DE NAMESPACES (FAGNER JUNQUEIRA) ===" | tee -a "$LOG_FILE"
for CNT in "$CONT_A" "$CONT_B"; do
    echo "--- CONTÊINER: $CNT ---" | tee -a "$LOG_FILE"
    PID_HOST="$(docker inspect --format 'PID_host={{.State.Pid}}' "$CNT")"
    echo "$PID_HOST" | tee -a "$LOG_FILE"
    
    COMM_1="$(docker exec "$CNT" sh -c 'cat /proc/1/comm')"
    echo "PID_1_comm=$COMM_1" | tee -a "$LOG_FILE"
    
    NS_PID="$(docker exec "$CNT" readlink /proc/1/ns/pid)"
    NS_MNT="$(docker exec "$CNT" readlink /proc/1/ns/mnt)"
    NS_NET="$(docker exec "$CNT" readlink /proc/1/ns/net)"
    
    echo "ns/pid=$NS_PID" | tee -a "$LOG_FILE"
    echo "ns/mnt=$NS_MNT" | tee -a "$LOG_FILE"
    echo "ns/net=$NS_NET" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
done

echo "=== 5. PARTE D: TESTE DE MOUNT E MENOR PRIVILÉGIO (GIULIAN LIMA) ===" | tee -a "$LOG_FILE"
echo "[Teste D.1] Leitura do volume somente leitura (/dados/texto.txt):" | tee -a "$LOG_FILE"
docker exec "$CONT_B" sh -c "cat /dados/texto.txt" | tee -a "$LOG_FILE" || echo "Falha na leitura" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "[Teste D.2] Tentativa de escrita no volume somente leitura (/dados/novo.txt):" | tee -a "$LOG_FILE"
if docker exec "$CONT_B" sh -c "touch /dados/novo.txt" 2>>"$LOG_FILE"; then
    echo "INADVERTIDO: Escrita permitida!" | tee -a "$LOG_FILE"
else
    echo "SUCESSO NO CONTROLE: Escrita negada com Read-only file system." | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "=== COLETA COMPARTILHADA FINALIZADA COM SUCESSO ===" | tee -a "$LOG_FILE"
echo "Log gerado em: $LOG_FILE"

