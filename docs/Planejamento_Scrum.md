# Planejamento Scrum – Interpretador da Linguagem Minipar

## Visão Geral
Este projeto tem como objetivo desenvolver um **interpretador para a linguagem Minipar**, uma linguagem de programação didática com suporte a execução sequencial, paralela (com threads), comunicação entre processos (via canais) e definição de funções. O desenvolvimento seguirá a **metodologia ágil Scrum**, organizada e executada com o suporte das ferramentas nativas do GitHub.

## Ferramentas do GitHub utilizadas
O GitHub (perfil privado do desenvolvedor: `github/edeilsonazevedo`) será a plataforma central de versionamento e organização do projeto, com recursos que se alinham perfeitamente com a filosofia Scrum:

- **Issues**: utilizadas para representar cada funcionalidade, tarefa ou correção necessária. Cada história de usuário (User Story) terá sua própria Issue.
- **Projects (Board)**: quadro Kanban para visualizar e organizar o progresso das tarefas. As colunas seguirão o fluxo: `Product Backlog` → `To Do` → `In Progress` → `Review` → `Done`.
- **Milestones**: representam as Sprints. Cada Sprint terá um conjunto de Issues associadas e prazo definido.
- **Labels**: marcarão prioridade, tipo de tarefa e status.

> 🔍 *O GitHub é uma excelente ferramenta para equipes que adotam Scrum, pois centraliza código, documentação, tarefas, progresso visual e automações, promovendo colaboração e rastreabilidade em tempo real.*

---

## Papéis Scrum
- **Product Owner**: responsável por priorizar o backlog e definir funcionalidades (github/edeilsonazevedo).
- **Scrum Master**: facilita os rituais e remoção de impedimentos (github/edeilsonazevedo).
- **Equipe de Desenvolvimento**: responsável por entregar as funcionalidades (github/edeilsonazevedo).

---

## Product Backlog (Histórias e Tarefas)

| ID  | Tarefa Técnica                                                  | História do Usuário                                                                   | Prioridade |
|-----|------------------------------------------------------------------|----------------------------------------------------------------------------------------|------------|
| US0 | Definir a gramática BNF da linguagem Minipar                    | Como desenvolvedor, quero definir a gramática BNF da linguagem Minipar                | Alta       |
| US1 | Implementar analisador léxico                                   | Como desenvolvedor, quero implementar o analisador léxico para identificar tokens     | Alta       |
| US2 | Implementar parser baseado na BNF e construir AST               | Como desenvolvedor, quero gerar a AST com base na gramática                          | Alta       |
| US3 | Interpretar blocos SEQ e PAR                                     | Como usuário, quero que blocos SEQ e PAR sejam executados corretamente                | Alta       |
| US4 | Implementar send/receive entre processos (canais)               | Como usuário, quero comunicar processos via canais usando send/receive                | Alta       |
| US5 | Verificar semântica: escopo, tipos, declarações                 | Como desenvolvedor, quero validar a semântica (escopo, tipos, declarações)            | Média      |
| US6 | Suportar definição e execução de funções com recursão          | Como usuário, quero poder definir e chamar funções com suporte à recursão             | Média      |
| US7 | Criar relatório final com testes e diagramas UML                | Como professor, quero um relatório final com testes, exemplos e diagramas UML         | Alta       |
| US8 | Automatizar testes com scripts Python                           | Como desenvolvedor, quero testar automaticamente os programas Minipar com scripts     | Média      |


---

## Sprints Planejadas

### 🟠 Sprint 1 – Léxico e Parser
**Objetivo**: Estruturar a base do interpretador.

- [ ] US0 - Definir gramática BNF (sem recursão à esquerda)
- [ ] US1 - Implementar analisador léxico
- [ ] US2 - Iniciar construção do parser LL(1)

### 🟠 Sprint 2 – Execução de Blocos e Canais
**Objetivo**: Interpretar código Minipar com SEQ, PAR e canais.

- [ ] US2 - Finalizar AST
- [ ] US3 - Executar blocos SEQ e PAR com threads
- [ ] US4 - Enviar e receber dados via canais (simulação com sockets)

### 🟠 Sprint 3 – Funções e Semântica
**Objetivo**: Adicionar semântica e suporte a funções.

- [ ] US5 - Verificação semântica
- [ ] US6 - Execução de funções e recursão

### 🟠 Sprint 4 – Refino e Entrega Final
**Objetivo**: Finalizar e entregar produto funcional e bem documentado.

- [ ] US7 - Criar relatório com diagramas UML
- [ ] US8 - Automatizar testes com scripts
- [ ] Documentar tudo no GitHub

---

## Rituais Scrum Adaptados
| Ritual              | Frequência    | Adaptação Solo                        |
|---------------------|---------------|---------------------------------------|
| Planejamento Sprint | Semanal       | Escolher tarefas da Sprint atual      |
| Daily Scrum         | Diário        | Revisar progresso (individualmente)   |
| Sprint Review       | Final Sprint  | Demonstrar funcionalidades completas  |
| Retrospectiva       | Final Sprint  | Registrar aprendizados e melhorias    |

---

## Definition of Done (DoD)
Uma tarefa só está "pronta" quando:
- Foi implementada e testada
- Nenhum erro crítico identificado
- Documentação associada está atualizada
- Integra-se ao interpretador e é validada por um dos programas de teste

---

## Conclusão
Com base nesse planejamento e usando o GitHub como plataforma de gestão, o projeto seguirá as práticas da metodologia Scrum de forma clara, rastreável e adaptada ao contexto acadêmico. Isso não apenas garante uma execução organizada, mas também oferece transparência e facilidade de avaliação para professores, colegas e colaboradores.

