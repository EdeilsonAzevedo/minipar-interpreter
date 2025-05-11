# Gramática BNF da Linguagem Minipar

```text

program         → stmts

/* Sequência de instruções */
stmts           → stmt stmts
                | ε

/* Tipos de instruções */
stmt            → compound_stmt
                | simple_stmt

/* Instruções simples */
simple_stmt     → declaration
                | assignment
                | return_stmt
                | "break"        /* Interrupção de laços */
                | "continue"     /* Continuação de laços */

/* Instruções compostas */
compound_stmt   → function_stmt
                | if_stmt
                | while_stmt
                | seq_stmt
                | par_stmt
                | channel_stmt

/* Atribuição de valores a variáveis */
assignment      → ID "=" expression

/* Declaração de variáveis com tipagem */
declaration     → ID ":" TYPE ["=" expression]

/* Instrução de retorno de funções */
return_stmt     → "return" expression

/* Bloco de código delimitado por chaves */
block           → "{" stmts "}"

/* Definição de funções com tipo de retorno */
function_stmt   → "func" ID "(" parameters ")" "->" TYPE block

/* Parâmetros de funções */
parameters      → params
                | ε

params          → param ["," params]

/* Parâmetro com tipo e valor padrão opcional */
param           → ID ":" TYPE [default]

default         → "=" expression

/* Estrutura condicional com else opcional */
if_stmt         → "if" "(" expression ")" block [else_block]

else_block      → "else" block

/* Estrutura de repetição */
while_stmt      → "while" "(" expression ")" block

/* Blocos de execução sequencial */
seq_stmt        → "seq" block

/* Blocos de execução paralela */
par_stmt        → "par" block

/* Definição de canais de comunicação */
channel_stmt    → s_channel_stmt
                | c_channel_stmt

/* Canal servidor - recebe função, descrição, host e porta */
s_channel_stmt  → "s_channel" ID "{" ID "," STRING "," STRING "," NUMBER "}"

/* Canal cliente - recebe host e porta */
c_channel_stmt  → "c_channel" ID "{" STRING "," NUMBER "}"

/* 
 * Hierarquia de expressões - define a precedência de operadores
 * da menor para a maior precedência
 */

/* Expressões de disjunção (OR lógico) */
expression      → disjunction

disjunction     → conjunction ["||" disjunction]

/* Expressões de conjunção (AND lógico) */
conjunction     → equality ["&&" conjunction]

/* Expressões de igualdade */
equality        → comparison [("==" | "!=") equality]

/* Expressões de comparação */
comparison      → sum [(">" | "<" | ">=" | "<=") comparison]

/* Expressões de soma e subtração */
sum             → term [("+" | "-") sum]

/* Expressões de multiplicação, divisão e módulo */
term            → unary [("*" | "/" | "%") term]

/* Operadores unários */
unary           → ("!" | "-") unary
                | primary

/* Acesso a membros, índices e chamadas de função */
local           → ID [local_tail]

local_tail      → "." ID [local_tail]
                | index [local_tail]
                | "(" arguments ")" [local_tail]

/* Acesso a índice (para strings) */
index           → "[" expression "]"

/* Argumentos de funções */
arguments       → expression ["," arguments]
                | ε

/* Expressões primárias */
primary         → "(" expression ")"
                | local
                | STRING
                | NUMBER
                | "true"
                | "false"

```


