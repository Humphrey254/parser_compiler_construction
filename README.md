# parser_compiler_construction


This project implements a recursive descent parser for a simple arithmetic expression grammar. The parser can handle expressions with addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`) operators, as well as parentheses for grouping.

## Grammar

The grammar for the expressions is defined as follows:

- **expression** ::= **term** ( ( "+" | "-" ) **term** )*
- **term** ::= **factor** ( ( "*" | "/" ) **factor** )*
- **factor** ::= "(" **expression** ")" | **number**
- **number** ::= **digit**+

## Getting Started

### Prerequisites

- Python 

## Example

```text
calc> 3 + 5 * (10 - 4)
BinOp(left=Num(3), op=Token(PLUS, '+'), right=BinOp(left=Num(5), op=Token(MUL, '*'), right=BinOp(left=Num(10), op=Token(MINUS, '-'), right=Num(4))))
