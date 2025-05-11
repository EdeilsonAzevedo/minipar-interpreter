# Tabela de Tokens na Linguagem MINIPAR

| Categoria | Tag | Expressão Regular | Exemplo | Descrição |
|-----------|-----|------------------|---------|-----------|
| **Identificadores** | `NAME` | `[A-Za-z_][A-Za-z0-9_]*` | `contador`, `total_soma` | Identificadores e palavras-chave |
| **Literais** | `NUMBER` | `\b\d+\.\d+\|\.\d+\|\d+\b` | `42`, `3.14`, `.5` | Constantes numéricas (inteiros ou decimais) |
| **Literais** | `STRING` | `"([^"]*)"` | `"hello world"` | Literais de texto entre aspas duplas |
| **Operadores** | `RARROW` | `->` | `func calc() -> number` | Indicador de tipo de retorno de função |
| **Operadores** | `OR` | `\|\|` | `a \|\| b` | Operador lógico OR |
| **Operadores** | `AND` | `&&` | `a && b` | Operador lógico AND |
| **Operadores** | `EQ` | `==` | `a == b` | Operador de igualdade |
| **Operadores** | `NEQ` | `!=` | `a != b` | Operador de diferença |
| **Operadores** | `LTE` | `<=` | `a <= b` | Operador menor ou igual que |
| **Operadores** | `GTE` | `>=` | `a >= b` | Operador maior ou igual que |
| **Comentários** | `SCOMMENT` | `#.*` | `# isso é um comentário` | Comentário de linha única |
| **Comentários** | `MCOMMENT` | `/\*[\s\S]*?\*/` | `/* comentário de múltiplas linhas */` | Comentário de bloco |
| **Formatação** | `NEWLINE` | `\n` | | Quebra de linha |
| **Formatação** | `WHITESPACE` | `\s+` | espaços, tabs | Caracteres de espaço em branco |
| **Diversos** | `OTHER` | `.` | `,` `;` `{` `}` | Qualquer outro caractere não especificado |

## Características dos Tokens
- Os tokens `NAME` representam identificadores que podem ser variáveis, funções ou palavras reservadas
- Os tokens `NUMBER` suportam diferentes formatos de números (inteiros e decimais)
- Os tokens de comentários (`SCOMMENT` e `MCOMMENT`) são ignorados pelo analisador léxico
- Os tokens de formatação (`WHITESPACE` e `NEWLINE`) ajudam na estruturação do código
- Os operadores relacionais e lógicos são utilizados em expressões condicionais
- O token `OTHER` captura símbolos de pontuação e delimitadores como parênteses, chaves e vírgulas