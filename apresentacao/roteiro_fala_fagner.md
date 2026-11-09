# Roteiro da Fala — Parte B: Evidências de Namespaces
**Apresentador:** Fagner Junqueira  
**Duração estimada:** 75 segundos (adequado à faixa de 60 a 90 segundos)  
**Uso:** Apresentação ao vivo da equipe e gravação individual para o vídeo.

---

### Roteiro Falado (Com Marcações de Tempo e Gestos de Tela)

**[00s - 15s] Abertura e Metodologia**  
> *"Olá a todos, sou Fagner Junqueira e fiquei responsável pela Parte B do nosso trabalho, onde investigamos as evidências empíricas de isolamento por namespaces no kernel Linux.*  
> *Para isso, nós instanciamos dois contêineres independentes a partir da mesma imagem fixada por digest: o Contêiner A e o Contêiner B."*

**[15s - 35s] Apresentação da Tabela e dos Dados Brutos**  
*(Apontando para a tabela no slide ou alternando rapidamente para o log bruto em `evidencia_ns_mount_20261109_203438.log`)*  
> *"Como vocês podem observar na tabela e no trecho do log bruto, consultamos os links simbólicos em `/proc/1/ns/` para os três recursos centrais: PID, Mount e Network.*  
> *Vejam que os números dos inodos retornados pelo kernel foram estritamente diferentes entre os dois contêineres: para PID tivemos `4026532869` contra `4026532945`; em Mount, `4026532401` contra `4026532942`; e na pilha de rede, `4026532871` contra `4026532947`. Isso comprova que o kernel alocou instâncias estruturais de tabelas separadas para cada processo."*

**[35s - 55s] Explicação do Fenômeno do PID 1 Interno**  
*(Destaque para o bloco central do slide)*  
> *"Um ponto fascinante da arquitetura do Linux que comprovamos na prática: internamente, ambos os contêineres executam o comando `sleep` identificado como PID 1. Porém, no host do daemon, o Contêiner A é o processo `6633` e o Contêiner B é o `6679`.*  
> *Isso acontece porque o PID namespace cria uma hierarquia virtual: o primeiro processo daquele namespace torna-se o 'init' local e recebe o número 1, enquanto o kernel mantém seu identificador unívoco na tabela global de tarefas (`task_struct`)."*

**[55s - 75s] Limitação do Teste e Conexão com os Próximos Colegas**  
> *"Para finalizar, é essencial destacar uma limitação crítica: constatar inodos de namespaces diferentes prova o particionamento da VISÃO do sistema operacional, mas NÃO garante limites de consumo nem impede ataques.*  
> *O namespace não restringe uso de CPU ou RAM — isso é papel exclusivo dos cgroups, que o Felipe e a Rauany vão demonstrar a seguir na Parte C — e também não impede escritas não autorizadas, que o Giulian testou na Parte D com montagem read-only.*  
> *Passo a palavra agora para a Parte C. Obrigado!"*

