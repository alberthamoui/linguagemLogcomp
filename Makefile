all: barscript

barscript: lexer.l parser.y
	bison -d parser.y
	flex lexer.l
	gcc -o barscript parser.tab.c lex.yy.c main.c -lfl

clean:
	rm -f barscript parser.tab.* lex.yy.c
