\# Atividade 3 — Sistemas Operacionais

\## Parte C — Controle de recursos com cgroups v2



\*\*Equipe:\*\* Gemma  

\*\*Ambiente:\*\* Ubuntu 24.04.5 LTS em máquina virtual Oracle VirtualBox  

\*\*Tecnologia:\*\* Docker Engine com cgroups v2  

\*\*Data das execuções originais:\*\* 7 de novembro de 2026



\## 1. Objetivo



Avaliar o funcionamento dos mecanismos de controle de recursos do Linux por meio de cgroups v2, comparando o comportamento de uma carga computacional executada em contêineres Docker com diferentes quotas de CPU.



O experimento também verifica a aplicação dos limites de memória e de quantidade de processos.



\## 2. Ambiente experimental



Os experimentos foram realizados em uma máquina virtual Ubuntu, configurada com dois processadores virtuais e aproximadamente 3,8 GiB de memória RAM.



Foi utilizado o Docker Engine 29.1.3, com o controlador cgroups v2.



Para garantir consistência, as execuções utilizaram a mesma imagem Python, identificada por seu digest SHA-256.



\## 3. Configurações experimentais



Foram definidas duas condições:



| Parâmetro | C1 | C2 |

|---|---|---|

| Quota de CPU | 0,5 CPU | 1 CPU |

| `cpu.max` | `50000 100000` | `100000 100000` |

| Memória RAM | 256 MiB | 256 MiB |

| Limite de processos | 64 | 64 |

| Repetições | 3 | 3 |



Ambas as condições utilizaram a configuração Docker `--memory=256m --memory-swap=256m`.



Em verificação complementar, `memory.swap.max` apresentou valor zero, indicando ausência de capacidade adicional de swap no contêiner de diagnóstico. Esse parâmetro não foi armazenado nos resultados originais.



\## 4. Metodologia



Foi desenvolvido um programa Python responsável pela execução de uma carga determinística composta por 20 milhões de iterações.



O programa calculou um checksum e registrou métricas internas de duração e tempo de CPU.



Um coletor independente acompanhou a execução do subprocesso e registrou:



\- Duração do monitoramento;

\- Consumo de CPU do cgroup;

\- Quantidade de períodos de controle e de throttling;

\- Tempo de throttling contabilizado pelo kernel;

\- Utilização de memória e RSS;

\- Limites efetivos dos controladores;

\- Código de saída, timeout e resultado funcional.



Foram realizadas três repetições de C1 e três de C2, alternando as condições.



Os seis arquivos JSON originais foram preservados para permitir auditoria dos resultados.



\## 5. Validação funcional



Todas as seis execuções apresentaram:



\- 20.000.000 de iterações;

\- Checksum igual a 4.864.000;

\- Status de sucesso;

\- Código de saída zero;

\- Ausência de timeout;

\- Arquivos externos de erro vazios.



Assim, não foram identificadas falhas funcionais nas execuções registradas.



\## 6. Resultados experimentais



\### 6.1. Duração do monitoramento



| Execução | C1 — 0,5 CPU | C2 — 1 CPU |

|---|---:|---:|

| R1 | 10,607014 s | 4,708670 s |

| R2 | 11,911186 s | 7,777698 s |

| R3 | 10,254488 s | 7,036787 s |

| \*\*Mediana\*\* | \*\*10,607014 s\*\* | \*\*7,036787 s\*\* |



A duração mediana do monitoramento foi aproximadamente 50,7% maior em C1.



Esse resultado é compatível com o comportamento esperado para uma condição com quota de CPU mais restritiva.



Entretanto, o tempo de monitoramento inclui atividades do coletor e não representa exclusivamente a duração computacional da carga.



\### 6.2. Consumo de CPU contabilizado pelo cgroup



| Execução | C1 — 0,5 CPU | C2 — 1 CPU |

|---|---:|---:|

| R1 | 3,570837 s | 4,940140 s |

| R2 | 4,058353 s | 3,940385 s |

| R3 | 3,699788 s | 3,754950 s |



Os valores representam o consumo de CPU registrado pelo controlador do kernel.



Essa métrica não corresponde ao tempo decorrido de execução. Por isso, não deve ser utilizada isoladamente para calcular diferenças de desempenho entre C1 e C2.



\### 6.3. Períodos com throttling



| Execução | C1 — 0,5 CPU | C2 — 1 CPU |

|---|---:|---:|

| R1 | 105 | 27 |

| R2 | 119 | 75 |

| R3 | 104 | 70 |

| \*\*Total\*\* | \*\*328\*\* | \*\*172\*\* |



C1 apresentou mais períodos com throttling nas três repetições correspondentes.



Esse comportamento é compatível com a aplicação de uma quota de CPU mais restritiva.



Os valores acumulados de `throttled\_usec` foram preservados nos resultados originais, mas não foram interpretados como segundos adicionais de execução da carga.



\### 6.4. Utilização de memória



Os valores máximos de memória contabilizados pelo cgroup permaneceram entre aproximadamente 21,48 e 21,75 MiB.



O maior pico observado foi de aproximadamente 21,75 MiB, abaixo do limite configurado de 256 MiB.



O RSS máximo observado do subprocesso variou entre 16.000 e 16.264 KB.



Esses dados indicam que o experimento não se aproximou do limite de memória durante as execuções registradas.



O parâmetro `pids.max` foi confirmado como 64 nos seis resultados, mas o experimento não demonstrou saturação desse limite.



\## 7. Limitações das medições



Durante a análise, foram identificadas diferenças importantes entre os tempos internos registrados pela carga e a duração observada pelo coletor.



Na condição C1, a mediana do tempo interno foi de 3,514819 segundos, enquanto a mediana da duração do monitoramento foi de 10,607014 segundos.



Além disso, algumas medições internas apresentaram valores de tempo de CPU próximos ao tempo decorrido, incompatíveis com o comportamento sustentado esperado para uma quota de 0,5 CPU.



Foram realizados testes complementares para investigar essas discrepâncias.



Em testes controlados, a quota de 0,5 CPU apresentou comportamento coerente com o esperado. Entretanto, a investigação não determinou a causa definitiva das inconsistências registradas no lote original.



Também foram identificados eventos de soft lockup na máquina virtual durante a investigação posterior. Não há evidência suficiente para atribuir a esses eventos a causa das discrepâncias originais.



Consequentemente, os resultados não permitem calcular com segurança uma diferença exata de desempenho computacional entre C1 e C2 com base nos tempos internos.



\## 8. Conclusão



O experimento confirmou a aplicação dos limites configurados para CPU, memória e processos por meio dos controladores de cgroups v2.



As seis execuções produziram resultados funcionais consistentes, sem falhas registradas.



A condição C1 apresentou maior duração de monitoramento e maior quantidade de períodos com throttling do que C2, em concordância qualitativa com o efeito esperado de uma restrição de CPU mais severa.



Contudo, as inconsistências nas medições de tempo exigem cautela na interpretação quantitativa do desempenho.



Os resultados demonstram a importância de utilizar conjuntamente métricas da aplicação, medições externas e contadores do kernel na avaliação experimental de mecanismos de controle de recursos.



\## 9. Arquivos e evidências



Os seguintes materiais acompanham a documentação:



\- `carga\_cpu.py`: implementação da carga determinística.

\- `coleta\_cgroups.py`: coleta das métricas do experimento.

\- `run\_experimentos.sh`: automatização das seis execuções.

\- `resultados/20261107T184710Z\_6139/`: resultados originais.

\- `resultados\_consolidados.csv`: tabela consolidada.

\- `graficos/01\_monitoramento.png`: duração do monitoramento.

\- `graficos/02\_consumo\_cpu.png`: consumo de CPU.

\- `graficos/03\_throttling.png`: períodos com throttling.

\- `resultados\_lote1\_original.tar.gz`: cópia compactada dos resultados originais.

\- `SHA256SUMS.txt`: hashes de integridade dos arquivos anteriormente registrados.



Os arquivos originais foram mantidos sem alterações durante a etapa de consolidação e análise.

