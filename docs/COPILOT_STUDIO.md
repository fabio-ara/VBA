# Copilot Studio como agente de desenvolvimento

Este roteiro serve para testar o Copilot Studio como substituto corporativo de outros agentes sem alterar o protocolo do repositório.

## Objetivo

O Copilot Studio deve operar o mesmo contrato:

`conversa → GitHub → Issues/docs/fontes → commit → ATUALIZAR.py → Excel local`

A continuidade vem do repositório. O agente não precisa ter memória privada entre sessões para recuperar o projeto.

## 1. Criar um agente de teste

Comece com um agente dedicado a desenvolvimento VBA e use um repositório descartável criado a partir de `fabio-ara/VBA`.

As instruções do agente devem ser curtas: sempre ler `AGENTS.md` antes de atuar e tratar o repositório como fonte de contexto permanente. Não replique todo o conteúdo do `AGENTS.md` no prompt do Copilot Studio.

## 2. Adicionar GitHub como ferramenta

No Copilot Studio, adicione o conector GitHub disponível no seu ambiente e autentique com uma conta que tenha somente o acesso necessário aos repositórios de automação.

Teste quais operações o tenant efetivamente permite. O conector pode ser suficiente para Issues e operações administrativas, mas o fluxo de desenvolvimento exige também leitura e gravação dos arquivos `.bas` e `.md`.

## 3. Adicionar GitHub MCP quando necessário

O Copilot Studio atual permite adicionar um servidor MCP pelo assistente em **Tools → Add a tool → New tool → Model Context Protocol**, usando transporte Streamable HTTP.

O GitHub mantém um servidor MCP remoto hospedado. A URL pública corrente é:

`https://api.githubcopilot.com/mcp/`

Configure autenticação conforme o método aceito pelo seu tenant e pela conexão. Prefira OAuth quando disponível; não grave PAT em documentação, prompts ou repositórios.

Políticas de dados/DLP do Power Platform podem permitir o servidor e ainda bloquear ferramentas ou combinações específicas. Isso precisa ser validado no ambiente corporativo.

## 4. Teste de aceitação do agente

Use um repositório descartável e verifique, nesta ordem:

1. pedir para ler `AGENTS.md` e resumir o protocolo sem modificar nada;
2. pedir para ler `docs/SPEC.md` e um `.bas` de teste;
3. discutir uma mudança e confirmar que o agente não implementa enquanto estiver `DISCUSSION`;
4. pedir para criar uma Issue `READY`;
5. pedir para alterar um arquivo `.bas` e um `.md` de forma coerente;
6. verificar o commit resultante;
7. pedir para atualizar a Issue para `VALIDATION`;
8. iniciar nova conversa e pedir recuperação do estado somente pelo repositório;
9. testar exclusão de arquivo;
10. só depois testar criação de repositório a partir do template.

Não teste exclusão de repositório em um projeto real.

## 5. Ferramentas mínimas desejadas

O conjunto ideal para desenvolvimento contém equivalentes a:

- leitura de arquivo;
- criação/atualização de arquivo;
- exclusão de arquivo;
- consulta/criação/atualização de Issue;
- commit ou gravação versionada;
- criação de repositório a partir do template.

Exclusão de repositório é opcional e deve exigir confirmação forte. Se o MCP/conector não a expuser, use o gerenciador Python local.

## 6. Instrução inicial recomendada

Use uma instrução equivalente a:

> Trabalhe no repositório indicado. Antes de agir, leia `AGENTS.md` e recupere o estado pelas Issues e documentação pertinentes. Não implemente uma Issue em `DISCUSSION` ou `BLOCKED`. Registre decisões e mudanças segundo o protocolo do próprio repositório.

## 7. Critério para substituir outro agente

Considere o Copilot Studio apto quando ele conseguir repetir de forma confiável o ciclo de leitura, planejamento por Issues, escrita de múltiplos arquivos, commits e continuidade entre conversas sem depender de instruções externas ao repositório.
