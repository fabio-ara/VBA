# Protocolo de operação para agentes

Este arquivo define o protocolo obrigatório para qualquer agente que leia ou modifique um repositório criado a partir deste modelo. As regras são independentes de ChatGPT, Copilot Studio, Codex, MCP ou outra plataforma.

## 1. Autoridade e fontes de verdade

A ordem de autoridade é:

1. instrução explícita e corrente do usuário;
2. Issue aprovada que define a mudança a implementar;
3. documentação canônica pertinente;
4. código e histórico do repositório como evidência do estado implementado.

Quando uma Issue aprovada alterar deliberadamente uma regra documentada, a Issue define o estado-alvo e a documentação deve ser atualizada como parte da mesma unidade de trabalho.

Não inferir regras de negócio, nomes de componentes do Excel ou decisões ausentes. Quando houver conflito não resolvível entre fontes, interromper a implementação e registrar a divergência.

## 2. Início de sessão

Antes de propor ou executar mudanças:

1. leia integralmente este `AGENTS.md`;
2. identifique a solicitação e, se houver, a Issue ativa;
3. leia somente as seções pertinentes de `docs/SPEC.md`, `docs/WORKBOOK.md`, `docs/ARCHITECTURE.md` e `docs/DEVELOPMENT.md`;
4. leia o código afetado e localize dependências e call sites;
5. amplie a inspeção somente quando necessário.

Não é obrigatório reler documentação não relacionada a cada tarefa.

## 3. Discussão não é implementação

O usuário pode discutir regras, UX, alternativas e arquitetura por várias mensagens antes de decidir.

Durante discussão:

- não implementar código sem autorização clara;
- distinguir hipótese, proposta e decisão aprovada;
- fazer perguntas somente quando uma lacuna impedir decisão ou implementação segura.

Quando o usuário pedir para **consolidar**, **fixar**, **registrar** ou **montar o plano**:

1. materialize as decisões duráveis na documentação canônica pertinente;
2. crie uma Issue de plano quando houver várias unidades de trabalho;
3. crie Issues executáveis, pequenas o suficiente para serem auditáveis e grandes o suficiente para produzir resultado útil;
4. explicite ordem e dependências;
5. marque cada Issue como `READY`, `DISCUSSION` ou `BLOCKED` no próprio corpo.

Não iniciar a implementação nessa etapa, salvo se o usuário também autorizar explicitamente a execução.

## 4. GitHub Issues é o backlog oficial

Não manter `BACKLOG.md` paralelo. GitHub Issues é a única fonte canônica de trabalho pendente, bugs, tooling e histórico das unidades de execução.

Tipos principais:

- `[PLAN]`: coordena um conjunto sequencial de Issues;
- `[FEATURE]`: funcionalidade ou alteração de regra/comportamento;
- `[BUG]`: defeito ou regressão observada;
- `[TOOLING]`: infraestrutura de desenvolvimento, sincronização, COM, testes ou diagnóstico.

Para planos sequenciais, usar títulos como `[P01][FEATURE] ...`, `[P02][FEATURE] ...`. A numeração representa a ordem dentro daquele plano, não prioridade global.

Toda Issue executável deve conter, quando aplicável:

- estado;
- objetivo;
- contexto e regras relevantes;
- escopo;
- fora de escopo;
- dependências;
- critérios de aceitação;
- verificação/testes;
- documentação a atualizar.

O estado textual no corpo é obrigatório porque labels podem variar entre ferramentas. Labels, quando disponíveis, espelham o estado e o tipo, mas não substituem o corpo.

Estados aceitos: `DISCUSSION`, `READY`, `IN_PROGRESS`, `BLOCKED`, `VALIDATION`.

## 5. Regra de autorização para código

Para mudanças não triviais de código, deve existir uma Issue correspondente antes da implementação.

Só implementar quando:

- a Issue estiver `READY`; ou
- o usuário ordenar explicitamente a implementação e autorizar a criação/ajuste da Issue necessária.

Ao começar, atualizar a Issue para `IN_PROGRESS` quando a ferramenta permitir.

Trabalhar em uma Issue por vez, salvo quando duas unidades forem tecnicamente inseparáveis e isso estiver documentado.

## 6. Conclusão de uma Issue

Antes de encerrar:

1. confira todos os critérios de aceitação;
2. faça análise estática e verificações automatizáveis disponíveis;
3. atualize documentação canônica afetada;
4. registre commit coerente relacionado à Issue;
5. se a aceitação depender de Excel/VBE local, mova para `VALIDATION` e aguarde evidência do usuário ou ferramenta local;
6. feche somente quando os critérios estiverem satisfeitos.

Nunca afirmar que algo foi testado no Excel local se o agente não recebeu evidência de execução local.

## 7. Bugs e regressões

Um bug descoberto após a conclusão de uma funcionalidade gera nova Issue `[BUG]`; não reescrever a história da Issue original.

A Issue de bug deve referenciar a funcionalidade/Issue relacionada quando conhecida e registrar:

- situação observada;
- situação esperada;
- reprodução mínima;
- causa, quando identificada;
- correção proposta;
- teste de regressão, quando viável.

Se o problema apenas mostrar que a Issue original ainda não cumpriu critérios de aceitação e ela não foi concluída, a mesma Issue pode continuar aberta.

## 8. Commits e branches

O branch `main` é a linha corrente por padrão. Alterações comuns podem ser gravadas diretamente em `main` para reduzir atrito.

Preferir um commit coerente por Issue quando isso não prejudicar o trabalho. Mensagens recomendadas:

- `feat(#123): descrição`;
- `fix(#123): descrição`;
- `chore(#123): descrição`;
- `docs(#123): descrição`.

Não usar fechamento automático da Issue antes de validações locais obrigatórias.

Branches e Pull Requests são opcionais e devem ser usados para mudanças grandes, arriscadas, experimentais ou quando o usuário solicitar revisão separada.

## 9. Documentação canônica

- `docs/SPEC.md`: regras de negócio e comportamento normativo aprovado; pode descrever estado-alvo ainda pendente de implementação, desde que a Issue correspondente torne isso rastreável.
- `docs/WORKBOOK.md`: estrutura material confirmada do XLSM, com origem da evidência; não registrar estrutura presumida.
- `docs/ARCHITECTURE.md`: arquitetura implementada ou contratos técnicos aprovados.
- `docs/DEVELOPMENT.md`: protocolo de desenvolvimento e governança das Issues.
- `docs/decisions/`: decisões arquiteturais de alto impacto que mereçam registro autônomo.

Evitar duplicar status de implementação na documentação: Issues representam o trabalho pendente e concluído.

## 10. Convenções VBA

- fontes canônicos contêm apenas código, sem cabeçalhos/metadados de exportação do VBE;
- começar com `Option Explicit`, salvo exceção técnica documentada;
- módulos padrão usam `.bas`;
- módulos de planilha, `ThisWorkbook` e código de UserForm também usam `.bas` conforme esta convenção;
- módulos de classe VBA verdadeiros podem usar `.cls`;
- não introduzir `Attribute VB_...`, `VERSION`, `BEGIN` ou outros cabeçalhos exportados pelo VBE nos fontes canônicos;
- preservar assinaturas públicas e contratos existentes salvo mudança deliberada;
- localizar dependências antes de renomear procedimentos, módulos, planilhas, tabelas, colunas, nomes definidos ou controles.

## 11. XLSM e estrutura do Excel

O XLSM é artefato local e não deve ser versionado.

Não inventar:

- nomes de planilhas e `CodeName`;
- tabelas (`ListObject`) e colunas;
- nomes definidos;
- UserForms e controles;
- referências VBA;
- Shapes ou outros objetos relevantes.

Obter estrutura a partir do XLSM fornecido, manifesto gerado localmente, código existente ou outra evidência confiável. Registrar em `docs/WORKBOOK.md` somente fatos duráveis confirmados.

## 12. Ferramentas locais, Python e COM

Ferramentas locais podem ser criadas para:

- sincronização GitHub → local;
- injeção de código no VBE;
- inventário do workbook;
- automação Excel COM;
- testes em cópia temporária do XLSM;
- captura de logs e diagnósticos;
- migrações estruturais controladas.

Preferir Python e recursos disponíveis no perfil do usuário, sem exigir administrador. Não construir infraestrutura complexa sem necessidade concreta.

Scripts não devem armazenar tokens, senhas ou dados corporativos sensíveis.

## 13. Portabilidade entre agentes

Nenhuma decisão necessária para continuar o projeto pode existir apenas na memória de uma conversa.

Ao final de uma sessão relevante, o repositório deve conter informação suficiente para que outro agente compatível recupere o estado por `AGENTS.md`, documentação, Issues e código.

Não escrever instruções fundamentais que dependam exclusivamente de uma marca ou produto de agente.

## 14. Relato ao usuário

Ao concluir trabalho de implementação, informar de forma breve:

- Issue executada;
- arquivos/áreas alterados;
- verificações realizadas;
- se há validação local pendente;
- se o usuário deve executar `ATUALIZAR.py` ou outra ferramenta local.
