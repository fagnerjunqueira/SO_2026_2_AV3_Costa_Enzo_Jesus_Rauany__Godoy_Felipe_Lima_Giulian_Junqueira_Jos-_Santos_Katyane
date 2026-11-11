# Checklist de entrega - integracao da main

A consolidacao de Katyane e preservada no historico. Este checklist registra apenas o que foi conferido em arquivos.

- [x] PDF consolidado e fonte Markdown integrados a main.
- [x] README com preparacao, reproducao, coleta, limpeza, digest e commits de referencia.
- [x] Seis JSON WSL2 com trabalho/checksum, status, limites e deltas conferidos.
- [x] CSV e graficos da Parte C integrados sem agregar VirtualBox.
- [x] Evidencias de ambiente, tabela de namespaces e log de leitura/negacao de escrita presentes.
- [x] VIDEO.md e README com links do video e da apresentacao; link do video no complemento do PDF e Markdown.
- [x] Coautoria de Venisson/Katyane e declaracoes individuais preservadas.
- [x] Manifesto de integracao disponibilizado para os bytes desta versao.
- [ ] Confirmar contribuicao especifica de Rauany ao lote WSL2 vigente.
- [ ] Conferir todas as restricoes de menor privilegio nas evidencias complementares da Parte D.
- [ ] Conferir visualmente o PPTX atualizado e a participacao de todos no video.
- [ ] Registrar envio do link no Classroom pela equipe.

## Integridade

O manifesto original `evidencias/parte_c_venisson/SHA256SUMS.txt` foi preservado. Sete arquivos copiados pela consolidacao possuem finais de linha LF em vez de CRLF; a comparacao com o commit original confirmou que essa e a unica diferenca. Os seis JSON de execucao mantiveram seus bytes. Para validar o conjunto integrado, a partir da raiz:

```bash
sha256sum -c SHA256SUMS_INTEGRACAO.txt
```

O PDF original de oito paginas e preservado no commit de Katyane `b0f9728bf74be2cfc35f69aee185e8e10584b278`. A versao integrada acrescenta uma pagina com vazao/amplitude, video e ressalvas. As paginas originais nao foram substituidas.
