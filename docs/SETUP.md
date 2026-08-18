# Configuração e uso

Este guia descreve o fluxo de baixo atrito no Windows, inclusive em máquinas nas quais o usuário só pode instalar ferramentas no próprio perfil.

## Pré-requisitos locais

- Python 3 já funcional para os scripts locais;
- Git disponível no `PATH`;
- GitHub CLI (`gh`) disponível no `PATH`;
- autenticação GitHub concluída no `gh`.

A configuração típica do GitHub CLI é feita uma vez com autenticação web e com o Git configurado para reutilizar essa credencial. A exclusão remota de repositório pode exigir autorização adicional do escopo `delete_repo`.

Nenhum token deve ser escrito em `.py`, `.ps1`, `.cmd` ou arquivos versionados.

## O repositório `fabio-ara/VBA`

O `VBA` é simultaneamente:

1. template público para novas automações;
2. repositório vivo, que pode ser clonado e aperfeiçoado no futuro.

Depois de cloná-lo localmente, `python ATUALIZAR.py` força os arquivos versionados a corresponder ao branch padrão remoto. Arquivos ignorados/não rastreados não são limpos.

## Criar e excluir automações sem comandos

Execute `GERENCIAR_AUTOMACOES.py` na cópia local do repositório `VBA`.

A interface permite:

- escolher nome, descrição, visibilidade e pasta local;
- criar repositório a partir de `fabio-ara/VBA`;
- criar labels auxiliares;
- clonar o novo repositório;
- inicializar README;
- remover o próprio gerenciador do projeto derivado;
- remover a licença MIT do projeto derivado quando desejado;
- excluir repositório remoto com confirmação forte;
- opcionalmente remover o clone local correspondente.

O gerenciador protege `fabio-ara/VBA` contra exclusão por sua própria interface.

## Projeto derivado

Em cada automação:

- GitHub é fonte de verdade;
- `ATUALIZAR.py` sincroniza GitHub → local;
- XLSM permanece local e é ignorado;
- um importador VBE existente pode ser integrado depois;
- ferramentas COM podem ser criadas progressivamente.

## Primeira conversa com um agente

Uma instrução suficiente é:

> Trabalhe neste repositório. Leia `AGENTS.md`, recupere o estado atual pelas Issues e documentação pertinentes e não implemente nada até eu orientar.

A partir daí, o repositório, e não a memória da conversa, sustenta a continuidade.

## Discussão e planejamento

Discuta regras e alternativas normalmente. Quando estiver satisfeito, peça ao agente para consolidar as decisões e criar um plano de Issues sequenciais. Revise o plano e, só então, autorize a implementação.

## Sincronização cotidiana

Depois que o agente gravar mudanças no GitHub, execute `ATUALIZAR.py` no projeto local antes de levar o código ao VBE.

Se um arquivo versionado tiver sido removido no GitHub, o `reset --hard` também o remove localmente. Arquivos ignorados, inclusive XLSM, não são apagados.

## Evolução do fluxo

Melhorias do próprio ambiente devem ser registradas como Issues `[TOOLING]`: integração do importador VBE, manifesto COM, smoke tests, logs, migrações e outros recursos. Assim a infraestrutura evolui com a mesma rastreabilidade do produto.
