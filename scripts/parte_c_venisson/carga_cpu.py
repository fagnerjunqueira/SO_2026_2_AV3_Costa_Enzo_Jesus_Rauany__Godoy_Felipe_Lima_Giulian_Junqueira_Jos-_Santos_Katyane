import argparse
import json
import time
import sys


def executar_carga(iteracoes):
    checksum = 0

    for i in range(iteracoes):
        checksum = (checksum + (i * i) % 1000000007) % 1000000007

    return checksum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteracoes", type=int, required=True)
    args = parser.parse_args()

    if args.iteracoes <= 0:
        print("Erro: quantidade de iteracoes deve ser positiva.", file=sys.stderr)
        sys.exit(1)

    inicio_wall = time.perf_counter()
    inicio_cpu = time.process_time()

    checksum = executar_carga(args.iteracoes)

    tempo_wall = time.perf_counter() - inicio_wall
    tempo_cpu = time.process_time() - inicio_cpu

    resultado = {
        "iteracoes": args.iteracoes,
        "checksum": checksum,
        "wall_time_s": round(tempo_wall, 6),
        "cpu_time_s": round(tempo_cpu, 6),
        "status": "sucesso"
    }

    print(json.dumps(resultado))


if __name__ == "__main__":
    main()