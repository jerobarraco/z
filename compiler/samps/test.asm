section .data
hello:     db 'Hello world!',10    ; 'Hello world!' plus a linefeed character
helloLen:  equ $-hello             ; Length of the 'Hello world!' string
hola:		db 'Hola caretas!',10
holaLen:	equ $-hola
section .text
mayor: db 'es mayor',10,0
mayorLen: dd 15
menor: db 'es menor',10,0
menorLen: dd 15
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
		mov esi, 0
	_forstart_140681210228976:
		cmp DWORD esi, 10
		jnl _forend_140681210228976 ;jump to false, below is 'true'
		cmp DWORD esi, 5
		jng _if_else_140681210230264 ;jump to false, below is 'true'
				push DWORD [mayorLen] ;print param 0
				push DWORD mayor ;print param 1
			call print
			add esp, 8 ;end print
		jmp _if_end_140681210230264
		_if_else_140681210230264:
				push DWORD [menorLen] ;print param 0
				push DWORD menor ;print param 1
			call print
			add esp, 8 ;end print
		_if_end_140681210230264:
		inc esi ;incdec esi
		jmp _forstart_140681210228976
	_forend_140681210228976:
	nop
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

print:
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, 4
	mov ebx, 1
	int 128
	ret ;; end print

