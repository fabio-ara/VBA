# Integrações com agentes, GitHub e MCP

O repositório foi desenhado para não depender de um único agente.

## Contrato mínimo de uma integração de desenvolvimento

Para executar o fluxo completo, um agente deve idealmente conseguir:

1. ler arquivos do repositório;
2. criar, substituir e excluir arquivos de texto;
3. consultar, criar e atualizar GitHub Issues;
4. relacionar mudanças a commits ou gravar mudanças versionadas;
5. recuperar o estado numa nova conversa.

Capacidades administrativas opcionais:

- criar repositório a partir deste template;
- alterar configurações do repositório;
- excluir repositório;
- administrar labels, branches e Pull Requests.

Ausência de uma capacidade administrativa não impede o desenvolvimento: `GERENCIAR_AUTOMACOES.py` fornece uma ponte local via GitHub CLI para criação e exclusão.

## ChatGPT

Quando o conector GitHub expuser leitura e escrita de arquivos e Issues, o agente pode operar diretamente o projeto. Se a conta/workspace permitir MCP personalizado com escrita, um servidor GitHub/MCP pode ampliar as ações disponíveis.

As regras do projeto devem vir de `AGENTS.md`, não de prompt privado dependente de uma conta específica.

## Copilot Studio

O agente corporativo deve receber GitHub como ferramenta e, quando necessário, um servidor MCP que exponha as operações faltantes.

Uma implantação deve ser validada empiricamente com um repositório descartável. Teste, no mínimo:

- leitura de `AGENTS.md`;
- leitura e edição de `.bas`;
- criação e atualização de Issue;
- alteração de múltiplos arquivos relacionados;
- exclusão de arquivo;
- continuidade em nova conversa;
- respeito ao estado `DISCUSSION`/`READY`.

Políticas de DLP, permissões do tenant e escopos do conector podem limitar ferramentas individualmente. O agente não deve receber acesso a dados ou repositórios além do necessário.

## GitHub MCP

Um MCP adequado funciona como adaptador entre o agente e o GitHub. O protocolo deste repositório não pressupõe nomes específicos de tools; pressupõe apenas as capacidades descritas acima.

Para criação de automações por conversa, a integração deve conseguir criar um repositório a partir de `fabio-ara/VBA` ou criar o repositório e copiar o conteúdo do template de forma equivalente.

Para exclusão por conversa, a ferramenta deve expor uma operação destrutiva explícita e exigir confirmação humana forte.

## Computador local

O agente não precisa acessar diretamente a máquina para o fluxo básico. A ponte é:

`agente → GitHub → ATUALIZAR.py → arquivos locais → importador VBE → Excel`

Quando necessário, scripts Python locais podem expor evidências do Excel por COM, sem alterar o contrato do GitHub.
