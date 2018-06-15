# Compiler Design Mini Project
A mini compiler which takes a C program as input and produces as output optimized intermediate/assembly code

## How To ##
1. Type input C code into input.c
2. Run comments.py on input.c to generate the C code without comments.Stored in nocomments.c
3. Now run lex.py on nocomments.c to get output

## Features ##
1. lex.py generates tokens for the input in nocomments.c
2. Tokens are stored in symbol table and passed as input to the parser
3. Parser now works for extern declarations,pre processor directives,declaration statements,for type checking,do while loop and expression statements
4. Genreates syntax tree and intermediate code

