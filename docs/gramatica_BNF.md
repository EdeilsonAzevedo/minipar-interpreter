# Gramática BNF da Linguagem Minipar

```text
program         → stmts

stmts           → stmt stmts_tail
stmts_tail      → stmt stmts_tail
                | ε

stmt            → compound_stmt
                | assignment
                | func_call
                | channel_stmt
                | print_stmt
                | input_stmt
                | comment

compound_stmt   → function_stmt
                | if_stmt
                | while_stmt
                | seq_stmt
                | par_stmt

assignment      → ID "=" expression

block           → stmts  

function_stmt   → "def" ID "(" parameters_opt ")" ":" block "end"

parameters_opt  → ID parameters_tail
                | ε

parameters_tail → "," ID parameters_tail
                | ε

if_stmt         → "if" "(" expression ")" stmt else_opt
else_opt        → "else" stmt
                | ε

while_stmt      → "while" "(" expression ")" stmt

seq_stmt        → "SEQ" stmts
par_stmt        → "PAR" stmts

channel_stmt    → "c_channel" ID ID ID

func_call       → ID "(" arguments_opt ")"

print_stmt      → "print" "(" expression ")"
input_stmt      → ID "=" "input" "(" ")"

arguments_opt   → expression arguments_tail
                | ε

arguments_tail  → "," expression arguments_tail
                | ε

expression      → disjunction

disjunction     → conjunction disjunction_tail
disjunction_tail→ "||" conjunction disjunction_tail
                | ε

conjunction     → equality conjunction_tail
conjunction_tail→ "&&" equality conjunction_tail
                | ε

equality        → comparison equality_tail
equality_tail   → ("==" | "!=") comparison equality_tail
                | ε

comparison      → sum comparison_tail
comparison_tail → (">" | "<" | ">=" | "<=") sum comparison_tail
                | ε

sum             → term sum_tail
sum_tail        → ("+" | "-") term sum_tail
                | ε

term            → factor term_tail
term_tail       → ("*" | "/" | "%") factor term_tail
                | ε

factor          → ("-" | "!") factor
                | primary

primary         → "(" expression ")"
                | ID
                | STRING
                | NUMBER
                | "true"
                | "false"

comment         → "#" texto

```