# VBA

Repositório-modelo público para desenvolvimento disciplinado de automações VBA com GitHub como fonte de verdade, agentes conversacionais como ambiente de autoria e Excel/VBE como ambiente local de execução.

O objetivo é permitir que uma automação seja desenvolvida sem depender de uma IDE específica: o agente lê o repositório, discute requisitos com o usuário, materializa decisões, organiza o trabalho em GitHub Issues, altera os fontes VBA e registra commits; a máquina local apenas sincroniza o `main`, injeta o código no VBE e executa o XLSM.

## Princípios

- GitHub é a fonte de verdade do código e da documentação.
- GitHub Issues é o backlog executável e o registro das unidades de trabalho.
- O XLSM permanece local e não é versionado.
- O fluxo é agnóstico ao agente: ChatGPT, Copilot Studio, MCP ou outra ferramenta podem operar o mesmo repositório.
- Arquivos VBA canônicos contêm somente código, sem cabeçalhos de exportação do VBE.
- Automação local usa ferramentas instaláveis no perfil do usuário e deve evitar privilégios administrativos.
- Infraestrutura adicional, inclusive Excel COM, testes e diagnósticos, é adicionada incrementalmente quando houver benefício concreto.

## Estrutura

- `AGENTS.md`: protocolo obrigatório para qualquer agente que trabalhe no repositório.
- `docs/SPEC.md`: regras de negócio e comportamento normativo.
- `docs/WORKBOOK.md`: estrutura material confirmada da pasta de trabalho.
- `docs/ARCHITECTURE.md`: arquitetura, módulos, contratos e integrações.
- `docs/DEVELOPMENT.md`: fluxo de discussão, planejamento, Issues, implementação e bugfix.
- `docs/SETUP.md`: tutorial de configuração e uso local.
- `docs/INTEGRACOES.md`: contrato mínimo para ChatGPT, Copilot Studio e MCP.
- `.github/ISSUE_TEMPLATE/`: formulários para plano, funcionalidade, bug e tooling.
- `ATUALIZAR.py`: sincroniza a cópia local com o `main` remoto.
- `GERENCIAR_AUTOMACOES.py`: interface gráfica para criar e excluir repositórios sem digitar comandos; existe no repositório-modelo e é removida automaticamente dos projetos criados por ela.
- `tools/`: ferramentas genéricas de validação e espaço para utilitários futuros.

## Uso como template

Este repositório deve ser marcado como **Template repository** no GitHub. O gerenciador local também consegue fazer essa configuração automaticamente pela API do GitHub usando o `gh` já autenticado.

Novos projetos normalmente são privados e são criados a partir deste template. O gerenciador pode remover a licença MIT do projeto privado durante a inicialização; a licença deste repositório público não implica que toda automação derivada deva ser distribuída sob MIT.

## Uso local do próprio VBA

O próprio `fabio-ara/VBA` pode ser clonado e mantido localmente como qualquer outro projeto. Depois do clone, execute `python ATUALIZAR.py` para materializar localmente o último `main`.

## Segurança

Não versione XLSM corporativo, dados pessoais, exportações de produção, credenciais, tokens ou logs contendo informações sensíveis. O repositório-modelo é público; exemplos e documentação devem ser genéricos.

## Licença

O conteúdo deste repositório é disponibilizado sob a licença MIT indicada em `LICENSE`.
