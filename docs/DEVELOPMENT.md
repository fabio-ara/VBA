# Fluxo de desenvolvimento por Issues

GitHub Issues é o backlog oficial. Este documento define como discussão, planejamento, implementação, validação e bugfix se relacionam.

## 1. Ciclo principal

`discussão → decisões aprovadas → documentação canônica → plano/Issues → implementação → validação → fechamento`

O usuário pode permanecer em discussão pelo tempo necessário. Implementação só começa com autorização clara.

## 2. Tipos de Issue

### `[PLAN]`

Coordena uma entrega composta por várias unidades. Deve listar a ordem e as dependências das Issues filhas, mas não duplicar seus critérios de aceitação.

### `[FEATURE]`

Representa uma mudança funcional implementável e verificável.

### `[BUG]`

Representa defeito ou regressão. Deve conter reprodução e comportamento esperado sempre que possível.

### `[TOOLING]`

Representa melhoria do próprio fluxo: Git/GitHub, sincronização, importação VBE, COM, testes, logs, diagnósticos, migrações ou outras ferramentas de desenvolvimento.

## 3. Estados

O corpo da Issue deve conter um estado textual, independente de labels:

- `DISCUSSION`: decisão ainda aberta; não implementar;
- `READY`: especificação suficiente e autorizada para implementação;
- `IN_PROGRESS`: implementação em curso;
- `BLOCKED`: depende de informação, decisão ou outra Issue;
- `VALIDATION`: implementação materializada, mas depende de validação local/usuário.

Issue fechada significa critérios satisfeitos ou trabalho explicitamente descartado.

## 4. Planejamento sequencial

Ao consolidar um conjunto de decisões:

1. criar uma Issue `[PLAN]` para a entrega quando houver múltiplas unidades;
2. criar Issues `[P01]`, `[P02]`, ... em ordem de execução;
3. declarar `Depende de: #N` quando houver dependência real;
4. evitar dependências artificiais apenas porque a numeração é sequencial;
5. manter critérios de aceitação na Issue executável, não apenas no plano.

Uma nova Issue de bug não precisa ser encaixada na numeração original do plano.

## 5. Granularidade

Uma boa Issue deve:

- produzir resultado observável;
- ser auditável em uma sessão razoável;
- evitar misturar decisões independentes;
- conter contexto suficiente para outro agente continuar sem recuperar a conversa original.

Não fragmentar mudanças triviais em micro-Issues sem ganho de rastreabilidade.

## 6. Implementação

Antes de editar:

- reler a Issue;
- verificar o estado `READY`;
- conferir dependências;
- ler documentação e código afetados;
- identificar call sites e contratos.

Durante a execução, manter a Issue coerente com descobertas relevantes. Mudança de escopo substancial exige decisão do usuário ou nova Issue.

## 7. Validação

Verificações podem incluir:

- análise estática;
- busca de call sites;
- validador do repositório;
- testes automatizados existentes;
- execução VBA/Excel via ferramentas locais;
- validação manual pelo usuário.

Quando o agente não controla o Excel local, registrar explicitamente a validação pendente em vez de presumir sucesso.

## 8. Bugfix e regressão

Após uma funcionalidade concluída, bug novo gera Issue própria `[BUG]`. Referenciar a Issue original e registrar teste de regressão quando viável.

Isso preserva a sequência histórica: decisão → implementação → defeito observado → correção.

## 9. Commits

Relacionar commits à Issue por número. Se a validação local ainda estiver pendente, não encerrar automaticamente a Issue pelo commit.

## 10. Labels

Labels são auxiliares. O gerenciador do template tenta criar:

- `type:feature`, `type:bug`, `type:tooling`, `type:plan`;
- `status:discussion`, `status:ready`, `status:blocked`, `status:validation`.

Como diferentes agentes e conectores podem não expor criação/edição de labels, o estado textual no corpo permanece canônico.
